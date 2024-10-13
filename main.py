import os
import streamlit as st
from openai import OpenAI
from crewai_tools import PDFSearchTool, SerperDevTool, ScrapeWebsiteTool
from crewai import Agent, Task, Crew
from PIL import Image

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

API_KEY = os.environ.get("OPENAI_API_KEY")
SERPER_API_KEY  = os.environ.get("SERPER_API_KEY")
OPENAI_MODEL_NAME = os.environ.get('OPENAI_MODEL_NAME')

logo_image = Image.open("./image/logo.png")

client = OpenAI(api_key=API_KEY)
tool_pdf = PDFSearchTool()
tool_search = SerperDevTool(n_results=5, country="sg")
tool_webscrape = ScrapeWebsiteTool()

def extract_file_paths(uploaded_files):
    file_paths = []
    for uploaded_file in uploaded_files:
        with open(os.path.join("tempdir", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_paths.append(os.path.join("tempdir", uploaded_file.name))
    return file_paths

st.image(logo_image, width=200)
topic = st.text_input("Enter Audit Topic [For example: Baby Bonus Scheme]:")
uploaded_files = st.file_uploader("Upload PDF files that may potentially contain past audit findings", accept_multiple_files=True, type="pdf")


if st.button("Let's Go, Buddy!!!") and topic and uploaded_files:
    os.makedirs("tempdir", exist_ok=True)
    file_paths = extract_file_paths(uploaded_files)

    auditor = Agent(
        role="auditor",
        goal=f"Generate Audit Planning Memo on {topic} using inputs from researcher and past audit findings from the audit assistant.",
        backstory=f"You are an auditor. You need to consider the inputs from the researcher and audit assistant to determine what to write for the audit planning memo and risk assessment",
        allow_delegation=True,
        max_iter=5,
    )

    researcher = Agent(
        role="researcher",
        goal=f"From the internet, research and analyse and sieve out all information related to {topic} only.",
        backstory=f"As a researcher, navigating and extracting critical information is crucial. You are assisting the auditor to research on information relevant to {topic}.",
        allow_delegation=False,
        max_iter=15
    )

    audit_assistant = Agent(
        role="audit assistant",
        goal=f"From PDF extract the audit findings pertaining to {topic}.",
        backstory=f"You are an audit assistant. Your job is to extract the past audit findings relating to {topic}.",
        allow_delegation=False,
        max_iter=15
    )

    task_search = Task(
        description=f"Returns a list of 5 websites that contain the most relevant information, in the context of Singapore, that are related to regulations on {topic} only. Ignore urls that ends with .pdf.",
        expected_output=f"a list of 5 websites",
        agent=researcher,
        tools=[tool_search],
    )

    task_websitesearch = Task(
        description=f"""1. Scrape the website for all regulations related to {topic} only
                      2. Summarize the information scraped""",
        expected_output=f"a summary of all regulations related to {topic}.",
        agent=researcher,
        tools=[tool_webscrape],
        context=[task_search]
    )

    task_extract_findings = Task(
        description=f"For each file path in {file_paths}, read the pdf and extract all audit findings pertaining to {topic}. Provide citation",
        expected_output=f"A list of audit findings pertaining to {topic} with citation",
        tools=[tool_pdf],
        agent=audit_assistant
    )

    task_write = Task(
        description=f"""1. Use the content to craft an audit planning memo and risk assessment based on {topic}.
                        2. Use the content to craft an audit risk assessment based on {topic}.
                        3.Write in an engaging manner.
                        4. Use common style used in audit planning memos.""",
        expected_output="""1. Section 1. Professional written audit planning memo
                           2. Section 2. Professional written audit risk assessment 
                           3. Each section should have minimum of 2 and maximum of 5 paragraphs.""",
        agent=auditor,
        context=[task_websitesearch, task_extract_findings],
        output_file="APM.md"
    )

    crew = Crew(
        agents=[auditor, researcher, audit_assistant],
        tasks=[task_search, task_websitesearch, task_extract_findings, task_write],
    )

    with st.spinner("Generating Audit Planning Memo...[It will take a while.]"):
        result = crew.kickoff(inputs={"topic": topic, "file_paths": file_paths})

    st.success("Audit Planning Memo generated successfully!")

    st.subheader("Results:")
    st.text(result.raw)

    st.subheader("List of Websites:")
    st.text(result.tasks_output[0])

    st.subheader("Information extracted from websites:")
    st.text(result.tasks_output[1])

    st.subheader("Information extracted from PDFs:")
    st.text(result.tasks_output[2])

    st.subheader("Token Usage")
    st.text(result.token_usage)

    if os.path.exists("APM.md"):
        with open("APM.md", "r") as f:
            apm_content = f.read()
        st.download_button(
            label="Download Audit Planning Memo",
            data=apm_content,
            file_name="Audit_Planning_Memo.md",
            mime="text/markdown"
        )
    else:
        st.warning("APM.md file not found. The memo might not have been generated successfully.")

    for file_path in file_paths:
        os.remove(file_path)
    os.rmdir("tempdir")
else:
    st.warning("Please enter an audit topic and upload at least one PDF file.")