# app_ui.py
import streamlit as st
import requests
import time

# --- 🌙 Page Config ---
st.set_page_config(page_title="SecureDataGPT", layout="wide")

# --- 🎨 Custom Dark Theme CSS ---
st.markdown("""
    <style>
        /* Background & Font */
        .main {
            background: radial-gradient(circle at top left, #001219 0%, #000814 100%);
            color: white;
            font-family: 'Inter', sans-serif;
        }

        /* Header Container */
        .header-container {
            text-align: center;
            padding: 2.5rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 30px rgba(0, 180, 216, 0.15);
            animation: fadeIn 1.5s ease;
        }

        /* Header Text */
        .header-title {
            font-size: 3rem;
            color: #00B4D8;
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 0.4rem;
        }

        .header-subtitle {
            color: #ADE8F4;
            font-size: 1.3rem;
            margin-bottom: 0.3rem;
        }

        .header-desc {
            color: #90E0EF;
            font-size: 1rem;
        }

        /* File uploader */
        .stFileUploader label {
            color: #00B4D8 !important;
            font-weight: 600;
            font-size: 1.1rem;
        }

        /* Animated spinner color */
        .stSpinner > div > div {
            color: #FFD166;
        }

        /* Result boxes */
        .success-box {
            background: linear-gradient(145deg, #073B4C, #0D2F3F);
            padding: 1rem;
            border-radius: 12px;
            color: #06D6A0;
            font-weight: 500;
            box-shadow: 0 0 12px rgba(6, 214, 160, 0.25);
        }

        .error-box {
            background: linear-gradient(145deg, #6A040F, #800E13);
            padding: 1rem;
            border-radius: 12px;
            color: #FFD6D6;
            box-shadow: 0 0 12px rgba(255, 99, 99, 0.25);
        }

        .recommend-box {
            background: linear-gradient(145deg, #1B263B, #0D1B2A);
            padding: 1.3rem;
            border-radius: 14px;
            color: #ADE8F4;
            font-size: 1.05rem;
            line-height: 1.6;
            box-shadow: 0 0 15px rgba(173, 232, 244, 0.1);
        }

        /* Fade-in animation */
        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(-10px);}
            to {opacity: 1; transform: translateY(0);}
        }
    </style>
""", unsafe_allow_html=True)

# --- 🌐 Header Section ---
st.markdown("""
    <div class="header-container">
        <h1 class="header-title"> SecureDataGPT</h1>
        <p class="header-subtitle">
            Your AI Agent for Data Privacy & Intelligent Analysis
        </p>
        <p class="header-desc">
            Upload your dataset and let SecureDataGPT detect sensitive information,
            summarize insights, and provide AI-driven recommendations — all in one place.
        </p>
    </div>
""", unsafe_allow_html=True)

# --- 🧠 Backend URL ---
backend_url = st.text_input(
    "🌍 FastAPI Backend Endpoint:",
    "http://127.0.0.1:8000/analyze",
    help="Enter your backend API endpoint (default: local server)"
)

# --- 📂 File Upload ---
uploaded_file = st.file_uploader(
    "📊 Upload your dataset (CSV, Excel, JSON)",
    type=["csv", "xlsx", "json"]
)

# --- ⚙️ Analysis Logic ---
if uploaded_file is not None:
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        with st.spinner("SecureDataGPT is analyzing your dataset..."):
            time.sleep(1)
            response = requests.post(backend_url, files=files)

        if response.status_code == 200:
            report = response.json()
            st.divider()

            st.subheader("📈 Summary")
            st.json(report.get("summary", {}))

            st.subheader("🧩 Sensitive Data Detected")
            if report.get("sensitive_data"):
                st.json(report["sensitive_data"])
            else:
                st.markdown('<div class="success-box">✅ No sensitive data detected!</div>', unsafe_allow_html=True)

            st.subheader("💡 AI Recommendations")
            st.markdown(f'<div class="recommend-box">{report.get("ai_recommendations", "No insights available.")}</div>', unsafe_allow_html=True)

        else:
            st.markdown(f'<div class="error-box">❌ Error {response.status_code}: {response.text}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.markdown(f'<div class="error-box">⚠️ Error: {e}</div>', unsafe_allow_html=True)
else:
    st.info("👆 Upload a file above to begin your data analysis.")
