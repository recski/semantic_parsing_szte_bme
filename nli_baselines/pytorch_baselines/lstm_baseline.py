import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as functional
#import gensim

torch.manual_seed(1)


class LSTMBaseline(nn.Module):

    def __init__(self, vocab_len, embedding_dim, hidden_dim, output_size):
        """
        The LSTM baseline contains an embedding layer, a long-short term memory (lstm) layer and a linear output layer.
        :param vocab_len: size of the vocabulary
        :type vocab_len: int
        :param embedding_dim: the dimension we want each word to translate to
        :type embedding_dim: int
        :param hidden_dim: the lstm layers' output dimension
        :type hidden_dim: int
        :param output_size: the size of the output; the number of classes in the classification problem
        :type output_size: int
        """
        super(LSTMBaseline, self).__init__()
        self.hidden_dim = hidden_dim
        #self.word_embedding = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True, limit=vocab_len*2)
        self.embedding = nn.Embedding(vocab_len, embedding_dim)
        #self.embedding.weight = nn.Parameter(self.word_embedding)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim)
        self.linear = nn.Linear(hidden_dim, output_size)
        self.hidden = (autograd.Variable(torch.zeros(1, 1, self.hidden_dim)),
                       autograd.Variable(torch.zeros(1, 1, self.hidden_dim)))
        self.loss_function = nn.NLLLoss()
        self.optimizer = optim.SGD(self.parameters(), lr=0.1)

    def prepare_sequence(self, sequence, to_ix):
        """
        The function that translates the words in the sequence to the number that it belongs to in the to_ix.
        :param sequence: the sequence we want to translate
        :type sequence: list
        :param to_ix: the lookup table of word to number translations
        :type to_ix: dict
        :return: the vector of the translation
        :rtype autograd Variable
        """
        idxs = [to_ix[w] for w in sequence]
        tensor = torch.LongTensor(idxs)
        return autograd.Variable(tensor)

    def forward(self, sentence_hypothesis, sentence_premise):
        """
        Forward propagation of the input through the network
        :param sentence_hypothesis: the words in the hypothesis sentence
        :type sentence_hypothesis: list
        :param sentence_premise: the words in the premise sentence
        :type sentence_premise: list
        :return: the output of the network with the given input
        :rtype: FloatTensor
        """
        lstm_out, self.hidden = self.lstm(self.embedding(sentence_hypothesis).view(len(sentence_hypothesis), 1, -1),
                                          self.hidden)
        lstm_out2, self.hidden = self.lstm(self.embedding(sentence_premise).view(len(sentence_premise), 1, -1),
                                           self.hidden)
        tag_space = self.linear(torch.add(lstm_out.view(len(sentence_hypothesis), -1)[-1],
                                          lstm_out2.view(len(sentence_premise), -1)[-1]))
        tag_scores = functional.log_softmax(tag_space, dim=0)
        return tag_scores

    def back_propagation(self, epochs, training_data, word_to_ix, tag_to_ix):
        """
        Backward propagation of the data and updating the network
        :param epochs: how many times we want to propagate with the training data
        :type epochs: int
        :param training_data: the sentences and expected tags that we use for training
        :type training_data: list
        :param word_to_ix: the lookup table of the words
        :type word_to_ix: dict
        :param tag_to_ix: the lookup table of the tags
        :type tag_to_ix: dict
        :return: None
        """
        for epoch in range(epochs):
            for sentence_hypothesis, sentence_premise, tag in training_data:
                self.zero_grad()
                self.hidden = (autograd.Variable(torch.zeros(1, 1, self.hidden_dim)),
                               autograd.Variable(torch.zeros(1, 1, self.hidden_dim)))

                # Step 2. Get our inputs ready for the network, that is, turn them into
                # Variables of word indices.
                sentence_h = self.prepare_sequence(sentence_hypothesis, word_to_ix)
                sentence_p = self.prepare_sequence(sentence_premise, word_to_ix)
                target = tag_to_ix[tag]

                # Step 3. Run our forward pass.
                tag_score = self(sentence_h, sentence_p)

                # Step 4. Compute the loss, gradients, and update the parameters by
                #  calling optimizer.step()
                loss = self.loss_function(tag_score.unsqueeze(0), autograd.Variable(torch.LongTensor([target])))
                loss.backward()
                self.optimizer.step()
