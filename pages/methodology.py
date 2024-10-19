import streamlit as st
from PIL import Image
import os
from helper_functions.utility import check_password  
    
# Check if the password is correct.  
if not check_password():  
    st.stop()

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="wide",
    page_title="My Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About this App")

st.write("This is a Streamlit App that assist AGO auditors in the audit planning and scoping phase of an Selective audit project. Enter the audit topic and upload the past audit observations in pdf format. The app would analyse the past audit observations and search the internet (you can indicate the websites to search too!) for other relevant information and provides a draft of the risk assessment and possible audit steps.")

with st.expander("How to use this App", expanded = True):
    st.write("1. Enter the audit topic.")
    st.write("2. Upload past audit observations in pdf format.")
    st.write("3. Indicate any websites of interest that you want the app to search information for (Some examples are provided).")
    st.write("4. Click the 'Let's go, Buddy!!!' icon.")
    st.write("5. Be patient and wait for the download button to appear to download the result.")

st.write("The app uses Large Language Model, specifically the crewAI multi-agent framework, to produce the output. For more information on the crewAI multi-agent framework, refer to https://docs.crewai.com/introduction. The below flowchart illustrate the process flow of the app.")

flowchart_image = Image.open("./image/flowchart.jpeg")

st.image(flowchart_image, width = 1200)
