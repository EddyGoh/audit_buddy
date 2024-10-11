import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from crewai_tools import PDFSearchTool, SerperDevTool, ScrapeWebsiteTool
from crewai import Agent, Task, Crew

# Load environment variables
load_dotenv('.env')
os.environ['OPENAI_MODEL_NAME'] = "gpt-4o-mini"
API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Initialize OpenAI client and tools
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

# Streamlit app
st.title("Audit Buddy")

# User input for topic
topic = st.text_input("Enter the audit topic:")

# File uploader
uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type="pdf")

if st.button("Let's Go!!!") and topic and uploaded_files:
    # Create a temporary directory to store uploaded files
    os.makedirs("tempdir", exist_ok=True)
    
    # Extract file paths
    file_paths = extract_file_paths(uploaded_files)

    # Define agents and tasks (same as before)
    auditor = Agent(
        role="auditor",
        goal=f"Return the Audit Planning Memo on {topic} based on inputs from researcher and past audit findings from the audit assistant.",
        backstory=f"You are an auditor. You need to consider the inputs from the researcher and audit assistant to determine what to write for the audit planning memo and risk assessment",
        allow_delegation=True,
        max_iter=5,
        verbose=True
    )

    researcher = Agent(
        role="researcher",
        goal=f"From the internet, research and analyse and sieve out information related to {topic} only.",
        backstory=f"As a researcher, navigating and extracting critical information is crucial. You are assisting the auditor to research on topics relevant to {topic}.",
        allow_delegation=False,
        verbose=True,
        max_iter=15
    )

    audit_assistant = Agent(
        role="audit assistant",
        goal=f"From PDF extract the audit findings pertaining to {topic} only.",
        backstory=f"You are an audit assistant. Your job is to extract the past audit findings relating to the {topic}.",
        allow_delegation=False,
        verbose=True,
        max_iter=15
    )

    task_search = Task(
        description=f"Returns a JSON list of top 5 websites that contain the most relevant information, in the context of Singapore, that are related to regulations on {topic} only. Ignore urls that ends with .pdf.",
        expected_output=f"Returns top 5 websites that contain most relevant regulations related information, in the context of Singapore, on {topic} only. The output must be in JSON format with the description as the key and url as value.",
        agent=researcher,
        tools=[tool_search],
    )

    task_websitesearch = Task(
        description=f"Scrape the website for all regulations related to {topic} only",
        expected_output=f"Summarise the website for all regulations related to {topic}.",
        agent=researcher,
        tools=[tool_webscrape],
        context=[task_search]
    )

    task_extract_findings = Task(
        description=f"For each file path in {file_paths}, read the pdf and extract all audit findings pertaining to {topic}. Provide citation",
        expected_output=f"A list of audit findings pertaining to {topic}",
        tools=[tool_pdf],
        agent=audit_assistant
    )

    task_write = Task(
        description=f"""
        1. Use the content to craft an audit planning memo and risk assessment based on {topic}.
        2. Sections are properly named in an engaging manner.
        3. Proofread for grammatical errors and alignment with the common style used in audit planning memos.""",
        expected_output="""
        A well-written audit planning memo and risk assessment in markdown format. Each section should have minimum of 2 and maximum of 5 paragraphs.""",
        agent=auditor,
        context=[task_websitesearch, task_extract_findings],
        output_file="APM.md"
    )

    crew = Crew(
        agents=[auditor, researcher, audit_assistant],
        tasks=[task_search, task_websitesearch, task_extract_findings, task_write],
        verbose=True
    )

    with st.spinner("Generating Audit Planning Memo..."):
        result = crew.kickoff(inputs={"topic": topic, "file_paths": file_paths})

    st.success("Audit Planning Memo generated successfully!")

    # Display results
    st.subheader("Raw Output")
    st.text(result.raw)

    st.subheader("Token Usage")
    st.text(result.token_usage)

    st.subheader("Task 1 Output")
    st.text(result.tasks_output[0])

    st.subheader("Task 2 Output")
    st.text(result.tasks_output[1])

    st.subheader("Task 3 Output")
    st.text(result.tasks_output[2])

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

    # Clean up temporary files
    for file_path in file_paths:
        os.remove(file_path)
    os.rmdir("tempdir")
else:
    st.warning("Please enter an audit topic and upload at least one PDF file.")