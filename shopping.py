import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # The evidence list and label list
    evidence_list, label_list = [], []
    # Mapping months abbreviation to their idx
    month_to_int = {
        'Jan': 0,
        'Feb': 1, 
        'Mar': 2, 
        'Apr': 3, 
        'May': 4, 
        'June': 5, 
        'Jul': 6, 
        "Aug": 7, 
        'Sep': 8, 
        'Oct': 9, 
        'Nov': 10, 
        'Dec': 11
    }
    # Reading the csv file as a dictionary
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Getting the evidence and the label from each row
            evidence = []
            label_list.append(1 if row['Revenue'] == 'TRUE' else 0)
            evidence.append(int(row['Administrative']))
            evidence.append(float(row['Administrative_Duration']))
            evidence.append(int(row['Informational']))
            evidence.append(float(row['Informational_Duration']))
            evidence.append(float(row['Informational_Duration']))
            evidence.append(int(row['ProductRelated']))
            evidence.append(float(row['ProductRelated_Duration']))
            evidence.append(float(row['BounceRates']))
            evidence.append(float(row['ExitRates']))
            evidence.append(float(row['PageValues']))
            evidence.append(float(row['SpecialDay']))
            evidence.append(int(month_to_int[row['Month']]))
            evidence.append(int(row['OperatingSystems']))
            evidence.append(int(row['Browser']))
            evidence.append(int(row['Region']))
            evidence.append(int(row['TrafficType']))
            evidence.append(1 if row['VisitorType'] == 'Returning_Visitor' else 0)
            evidence.append(0 if row['Weekend'] == 'FALSE' else 1)
            evidence_list.append(evidence)

    return (evidence_list, label_list)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)

    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Counting the number of true positive and true negative and returning their ratio to 
    # total no. of positive and total no. of negative
    true_positive, true_negative = 0, 0
    for i in range(len(labels)):
        if labels[i] == 1 and predictions[i] == 1:
            true_positive += 1
        elif labels[i] == 0 and predictions[i] == 0:
            true_negative += 1

    sensitivity = true_positive / labels.count(1)
    specificity = true_negative / labels.count(0)

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
