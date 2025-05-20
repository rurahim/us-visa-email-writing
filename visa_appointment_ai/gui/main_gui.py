# streamlit_app/gui.py

import streamlit as st
import requests
import json
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="US Visa Appointment Assistant",
    page_icon="🛂",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border: none;
        border-radius: 4px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("US Visa Appointment Assistant")
st.markdown("""
    This application helps you optimize your visa appointment request by analyzing your message
    and providing a priority score based on various factors.
""")

# Create two columns for the form
col1, col2 = st.columns(2)

with col1:
    # Input fields
    full_name = st.text_input("Full Name", placeholder="Enter your full name")
    email = st.text_input("Email", placeholder="Enter your email address")
    
with col2:
    visa_type = st.selectbox(
        "Visa Type",
        ["B1/B2", "F1", "H1B", "J1", "L1", "Other"],
        help="Select your visa type"
    )
    
    message = st.text_area(
        "Message",
        placeholder="Enter your appointment request message",
        height=100
    )

# Process button
if st.button("Process Request", type="primary"):
    if not all([full_name, email, visa_type, message]):
        st.error("Please fill in all fields")
    else:
        try:
            # Show processing status
            with st.spinner("Processing your request..."):
                # Prepare the request data
                data = {
                    "full_name": full_name,
                    "email": email,
                    "visa_type": visa_type,
                    "message": message
                }
                
                # Make API request
                response = requests.post(
                    "http://localhost:8000/api/process/",
                    json=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display results in expandable sections
                    with st.expander("Priority Score", expanded=True):
                        st.metric("Score", f"{result['initial_score']:.2f}")
                        st.progress(result['initial_score'])
                    
                    with st.expander("Analysis Details", expanded=True):
                        st.json(result)
                    
                    with st.expander("Optimized Message", expanded=True):
                        st.text_area("", result['best_email'], height=200)
                    
                    # Show timestamp
                    st.caption(f"Processed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
                else:
                    st.error(f"Error: {response.text}")
                    
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Please make sure the backend is running.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Add footer
st.markdown("---")
st.caption("© 2024 US Visa Appointment Assistant")
