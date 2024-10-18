import streamlit as st
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

st.title("About this App")

# Write the objectives using HTML text using st.markdown
st.subheader("Objectives")

obj_str = """
<p style="text-align: justify;">
    Audit planning and scoping are critical as they set the stage for an effective and efficient audit process. It is essential to carry out a preliminary study and risk assessment during this phase to identify potential areas of concern and tailor the audit strategy accordingly. This ensures that the audit focuses on the most significant areas, enhancing its effectiveness. However, this phase involves gathering a voluminous amount of information from various sources and integrating the information to properly identify all risk areas. This app utilizes LLM, specifically using a multi-agent framework from CrewAI, to assist AGO auditors in the audit planning and scoping phase of an audit project.
</p>
"""

st.markdown(obj_str, unsafe_allow_html=True)


# Write the project scope using HTML text using st.markdown
st.subheader("Project Scope")

scope_str = """
<p style="text-align: justify;">
    Although the app is tailored to Selective audits conducted by AGO, it could reasonably be used for other types of audit projects.
</p>
"""

st.markdown(scope_str, unsafe_allow_html=True)


# Write the data sources using HTML text using st.markdown
st.subheader("Data Sources")

sources_str = """
<p style="text-align: justify;">
    The data used would be from the user and information obtained in the internet through web scrapping.
</p>
"""

st.markdown(sources_str, unsafe_allow_html=True)



# Write the features using HTML text using st.markdown
st.subheader("Features")

features_str = """
<p style="text-align: justify;">
    The app requires the user to provide the audit topic, past audit findings in PDF format, and optional websites for information searches. The app searches the internet and the provided websites for other information related to the audit topic. With all the gathered information, it outputs the risk assessment and proposed audit steps.
</p>
"""

st.markdown(features_str, unsafe_allow_html=True)

