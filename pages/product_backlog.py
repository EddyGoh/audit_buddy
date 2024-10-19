import streamlit as st
import os
from helper_functions.utility import check_password  
    
# Check if the password is correct.  
if not check_password():  
    st.stop()

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("Product Backlog")

st.write("To assess if using PDF toolkit (e.g. PyMuPDF) and LLM will be better than PDFSearchTool.")

st.write("To assess if using LLM with much larger context window (e.g. Gemini Pro) will improve the quality of response.")

st.write("To add three lines of defense (3LOD) to further scrutanize the response.")

st.write("To add in Audit Memo Examples to ground/constraint the writing style.")


