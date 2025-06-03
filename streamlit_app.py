
import streamlit as st
#from langchain.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict

# --- LLM Setup ---
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# --- Prompts ---
READER_PROMPT = """You are an expert BCG consultant. Below is a Word document with updates for several countries. Some text is in paragraphs, some in tables.
Extract and summarize each country’s key updates from the document.
Do not add in any additional text or information.
Only reference and take information from the report and not from your own knowledge.

Document:
----
{document_text}
----

Return format:
Country: <country name>
Summary: <executive summary>
"""

SUMMARY_PROMPT = """You are a strategy analyst from BCG. Based on the following country updates, summarize the key regional themes and strategic takeaways.
Only reference and take information from the report and not from your own knowledge.

Country Updates:
----
{country_updates}
----

Return a 3-paragraph summary with insights across countries.
"""

EMAIL_PROMPT = """You are a senior communications director. Write a professional email regarding news monitoring highlights from our Asia countries, to the Asia President based on the summary below.
The email content is to contain the below two sections:
1.  Key highlights from the news monitoring (indicate the country)
2.  Recommendations to be taken only from the reports, do not add in any additional text or information.
Keep email within 300 words.
Do not need any introduction or summary in the email.
Do not use your own knowledge.

Summary:
----
{regional_summary}
----

Return a polished email in proper format.
"""

# --- State Definition ---
class GraphState(TypedDict):
    document_path: str
    document_text: str
    country_updates: str
    regional_summary: str
    email_draft: str

# --- Agent Functions ---
def reader_agent(state: GraphState) -> GraphState:
    path = state["document_path"]
    loader = Docx2txtLoader(path)
    docs = loader.load()
    text = docs[0].page_content
    prompt = READER_PROMPT.format(document_text=text)
    response = llm.invoke(prompt)
    return {
        "document_path": path,
        "document_text": text,
        "country_updates": response.content,
        "regional_summary": "",
        "email_draft": ""
    }

def summary_agent(state: GraphState) -> GraphState:
    prompt = SUMMARY_PROMPT.format(country_updates=state["country_updates"])
    response = llm.invoke(prompt)
    return {
        **state,
        "regional_summary": response.content
    }

def editor_agent(state: GraphState) -> GraphState:
    prompt = EMAIL_PROMPT.format(regional_summary=state["regional_summary"])
    response = llm.invoke(prompt)
    return {
        **state,
        "email_draft": response.content
    }

# --- Build LangGraph ---
READER, SUMMARIZER, EDITOR = "Reader", "Summarizer", "Editor"

builder = StateGraph(GraphState)
builder.add_node(READER, reader_agent)
builder.add_node(SUMMARIZER, summary_agent)
builder.add_node(EDITOR, editor_agent)
builder.set_entry_point(READER)
builder.add_edge(READER, SUMMARIZER)
builder.add_edge(SUMMARIZER, EDITOR)
builder.add_edge(EDITOR, END)
graph = builder.compile()

# --- Streamlit UI ---
st.set_page_config(page_title="News Monitoring Email Generator", layout="centered")
st.title("📰 AI News Monitoring Email Assistant")

uploaded_file = st.file_uploader("Upload a .docx file with country updates:", type=["docx"])

if uploaded_file:
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    if st.button("Generate Email Summary"):
        with st.spinner("Analyzing document and generating summary..."):
            initial_state = {
                "document_path": temp_path,
                "document_text": "",
                "country_updates": "",
                "regional_summary": "",
                "email_draft": ""
            }
            final_state = graph.invoke(initial_state)
            st.subheader("✉️ Final Email Draft")
            st.text_area("Email to Asia President:", final_state["email_draft"], height=400)

        st.success("Email generation complete.")
