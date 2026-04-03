import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from auth import register_user, login_user
from database import create_tables
from model import train_model, predict

create_tables()

st.set_page_config(layout="wide")

# ================= SESSION STATE =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_register" not in st.session_state:
    st.session_state.show_register = False

# ================= LOGIN / REGISTER =================
if not st.session_state.logged_in:

    st.title("🔐 Login")

    if not st.session_state.show_register:
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Login"):
                if login_user(user, pwd):
                    st.session_state.logged_in = True
                    st.success("Logged in!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        with col2:
            if st.button("Go to Register"):
                st.session_state.show_register = True
                st.rerun()

    else:
        st.title("📝 Register")

        user = st.text_input("New Username")
        pwd = st.text_input("New Password", type="password")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Register"):
                register_user(user, pwd)
                st.success("User created!")
                st.session_state.show_register = False
                st.rerun()

        with col2:
            if st.button("Back to Login"):
                st.session_state.show_register = False
                st.rerun()

# ================= MAIN APP =================
if st.session_state.logged_in:

    st.sidebar.success("Logged in")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.pop("df", None)
        st.rerun()

    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Go to", ["Upload", "Dashboard", "Prediction"])

    # ================= UPLOAD =================
    if option == "Upload":
        st.title("📤 Upload Dataset")

        file = st.file_uploader("Upload CSV", type=["csv"])

        if file:
            df = pd.read_csv(file)
            st.session_state.df = df
            st.success("Data uploaded successfully!")

    # ================= DASHBOARD =================
    elif option == "Dashboard":

        if "df" not in st.session_state:
            st.warning("⚠️ Upload data first!")
            st.stop()

        df = st.session_state.df

        st.title("📊 Advanced Dashboard")

        st.subheader("📄 Data Preview")
        st.dataframe(df)

        st.subheader("📊 Statistics")
        st.write(df.describe())

        subjects = df.columns[2:-1]

        # Average Marks
        st.subheader("📈 Average Marks by Subject")
        avg = df[subjects].mean()

        fig, ax = plt.subplots()
        avg.plot(kind='bar', ax=ax)
        st.pyplot(fig)

        # Distribution
        st.subheader("📊 Marks Distribution")
        fig, ax = plt.subplots()
        df[subjects].plot(kind='hist', bins=10, alpha=0.6, ax=ax)
        st.pyplot(fig)

        # Pass Fail
        st.subheader("🟢 Pass vs Fail Ratio")
        fig, ax = plt.subplots()
        df["Result"].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)

        # Correlation
        st.subheader("🔗 Correlation Heatmap")
        corr = df[subjects].corr()

        fig, ax = plt.subplots()
        cax = ax.matshow(corr)
        fig.colorbar(cax)

        ax.set_xticks(range(len(subjects)))
        ax.set_yticks(range(len(subjects)))
        ax.set_xticklabels(subjects)
        ax.set_yticklabels(subjects)

        st.pyplot(fig)

        # Attendance vs Marks
        st.subheader("📉 Attendance vs Average Marks")
        df["AvgMarks"] = df[subjects].mean(axis=1)

        fig, ax = plt.subplots()
        ax.scatter(df["Attendance"], df["AvgMarks"])
        ax.set_xlabel("Attendance")
        ax.set_ylabel("Average Marks")
        st.pyplot(fig)

        # Top Students
        st.subheader("🏆 Top Performers")
        top = df.sort_values("AvgMarks", ascending=False).head(5)
        st.dataframe(top)

        # Weak Students
        st.subheader("⚠️ Needs Improvement")
        low = df.sort_values("AvgMarks").head(5)
        st.dataframe(low)

        # Insights
        st.subheader("🧠 Insights")
        st.info(f"Best Subject: {avg.idxmax()}")
        st.info(f"Weakest Subject: {avg.idxmin()}")
        st.info(f"Overall Average: {round(df['AvgMarks'].mean(),2)}")

    # ================= PREDICTION =================
    elif option == "Prediction":

        if "df" not in st.session_state:
            st.warning("⚠️ Upload data first!")
            st.stop()

        df = st.session_state.df

        model, acc = train_model(df)

        st.title("🤖 Prediction")

        st.subheader("Model Accuracy")
        st.success(f"{round(acc*100,2)}%")

        st.subheader("Enter Marks")

        math = st.slider("Math", 0, 100, 50)
        science = st.slider("Science", 0, 100, 50)
        english = st.slider("English", 0, 100, 50)

        if st.button("Predict"):
            result = predict(model, [math, science, english])
            st.success(f"Prediction: {result}")