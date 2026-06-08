from PIL import Image
import streamlit as st
icon = Image.open(r"assets\logo.png")
st.set_page_config(
    page_title="GreekForce AirSense",
    page_icon=icon,
    layout="wide"
)
st.markdown(
    """
    <style>
    .main {
        background-color: #0E1117;
    }

    .hero {
        background: linear-gradient(90deg, #00E5FF, #007CF0);
        padding: 45px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }

    .card {
        background-color: #1E1E1E;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #333;
        box-shadow: 0px 0px 12px rgba(0,229,255,0.2);
        color: white;
        height: 180px;
    }

    h1, h2, h3 {
        color: #00E5FF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero">
        <h1>🌍 GreekForce AirSense</h1>
        <h3>AI-Powered Air Quality Monitoring & Prediction System</h3>
        <p style="font-size:18px;">
            Track live AQI, train ML models, predict pollution levels, and view health recommendations.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("Welcome to AirSense")

st.write(
    """
    AirSense is an intelligent air quality dashboard that uses live AQI data
    and machine learning to predict pollution levels for major Indian cities.
    """
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="card">
            <h3>Train Model</h3>
            <p>Upload your AQI CSV dataset and train a machine learning model.</p>
            <p><b>Go to:</b> Model Page</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="card">
            <h3>Live Dashboard</h3>
            <p>View real-time AQI, pollutant levels, maps, charts, and predictions.</p>
            <p><b>Go to:</b> Dashboard Page</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="card">
            <h3>Health Alerts</h3>
            <p>Get safety recommendations based on predicted air quality.</p>
            <p><b>Included in:</b> Dashboard</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

st.subheader("How to Use")

st.markdown(
    """
    1. Open the **Model** page from the sidebar  
    2. Upload your AQI CSV dataset  
    3. Train and save the ML model  
    4. Open the **Dashboard** page  
    5. View live AQI data and prediction results  
    """
)

st.sidebar.success("Start from the Model page, then open Dashboard.")