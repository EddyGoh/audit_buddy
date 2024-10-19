# Introduction

This is developed for the ABC project by using CrewAI to generate an Audit Planning Memo and Risk Assessment for auditors to use.

# Members
Eddy
YK
YCH

# How-to-run

1. Set your OPENAI_API_KEY, SERPER_API_KEY and ABC_PASSWORD in an .env file pr enter them in the environment variables.
2. run streamlit.py using streamlit "streamlit run streamlit.py"

# Backlog

- To assess if using PDF toolkit (e.g. PyMuPDF) and LLM will be better than PDFSearchTool
- To assess if using LLM with much larger context window (e.g. Gemini Pro) will improve the quality of response
- To add three lines of defense (3LOD) to further scrutanize the response
- To add in Audit Memo Examples to ground/constraint the writing style