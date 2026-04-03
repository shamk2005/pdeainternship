from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def train_model(df):

    # 🔥 Select ONLY numeric columns
    X = df[["Math", "Science", "English"]]

    # 🔥 Convert labels
    y = df["Result"].map({"Pass": 1, "Fail": 0})

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    return model, acc


def predict(model, values):
    pred = model.predict([values])[0]
    return "Pass" if pred == 1 else "Fail"