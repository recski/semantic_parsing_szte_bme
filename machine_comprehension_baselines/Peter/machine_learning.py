def train_and_test(train_x, train_y, test_x, test_y, clf):

    print("Fitting")
    clf.fit(train_x, train_y)
    print("Fitting Done")
    print("Predicting...")

    predicted = clf.predict(test_x)

    print("Predict Done")
    talalt = 0
    osszes = len(test_y)
    """jó eredmény számolás"""
    for index in range(len(test_y)):
        if predicted[index] == test_y[index]:
            talalt += 1

    print("Jó válaszok: ", str((talalt / osszes) * 100), "%")
