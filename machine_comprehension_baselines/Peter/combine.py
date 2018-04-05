import pickle

def combinator(outfile, *args):

    if len(args) < 2:
        print("2 file kell legalább ha kombinálni akarsz lol.")
        return
    print("Combining...")
    with open(args[0], "rb") as f:
        all = pickle.load(f)
        train_x = all[0]
        train_y = all[1]
        test_x = all[2]
        test_y = all[3]

    is_first = True
    for filename in args:

        if is_first:
            is_first = False
            continue

        with open(filename, "rb") as f:
            all = pickle.load(f)

            for i in range(len(train_x)):
                train_x[i].extend(all[0][i])

            for j in range(len(test_x)):
                test_x[j].extend(all[2][j])

    with open(outfile, "wb") as f:
        pickle.dump([train_x, train_y, test_x, test_y], f)
    print("Combining done.")
