from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.dummy import DummyClassifier


def evaluate_model(model, X_train, y_train, X_test, y_test):

    predictions = model.predict(X_test)

    print("MODEL RESULTS")
    print("Accuracy:", accuracy_score(y_test, predictions))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, predictions))
    print("\nClassification Report:")
    print(classification_report(y_test, predictions, zero_division=0))

    # Majority-class baseline
    baseline = DummyClassifier(strategy="most_frequent")
    baseline.fit(X_train, y_train)

    baseline_predictions = baseline.predict(X_test)

    print("\nBASELINE ACCURACY:")
    print(accuracy_score(y_test, baseline_predictions))
