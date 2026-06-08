import streamlit as st
import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

st.set_page_config(
    page_title="Train AQI Model",
    layout="wide"
)

st.title("Train AQI ML Model")

uploaded_file = st.file_uploader(
    "Upload AQI CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    required_columns = [
        "pm25",
        "pm10",
        "no2",
        "temp",
        "humidity",
        "aqi"
    ]

    if all(col in df.columns for col in required_columns):

        X = df[[
            "pm25",
            "pm10",
            "no2",
            "temp",
            "humidity"
        ]]

        y = df["aqi"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        if st.button("Train Model"):

            model = RandomForestRegressor(
                n_estimators=100,
                random_state=42
            )

            model.fit(
                X_train,
                y_train
            )

            y_pred = model.predict(X_test)

            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            os.makedirs("models", exist_ok=True)

            joblib.dump(
                model,
                "models/aqi_model.pkl"
            )

            st.success("AQI ML Model Saved Successfully")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Mean Absolute Error", round(mae, 2))

            with col2:
                st.metric("R² Score", round(r2, 2))

            st.info("Now open Dashboard page to use the trained model.")

    else:

        st.error("Invalid CSV format")

        st.write("Your CSV must contain these columns:")

        st.code("""
pm25,pm10,no2,temp,humidity,aqi
""")