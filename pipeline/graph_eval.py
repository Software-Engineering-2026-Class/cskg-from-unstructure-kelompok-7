from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate


def generate_brief(data, date_str):
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        print("[SUMMARY] ERROR: GOOGLE_API_KEY not found.")
        return None

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")

    template = """
    You are a Strategic Cyber Intelligence Analyst. 
    Current Reporting Date: {date}
    
    Your task is to write a 'Comprehensive Threat Landscape Assessment' based on the aggregated knowledge in our graph.
    
    The data below represents the current knowledge in our CSKG named graph. It may contain threat actor capabilities, or fallback graph data focused on vulnerabilities, malware, attack patterns, and indicators when no threat actors are present.
    
    Please analyze this data to provide a strategic summary:
    1. **Key Observations:** Identify the most important entities and patterns in the data.
    2. **Risk Themes:** Discuss vulnerabilities, malware, attack patterns, indicators, or threat actors when available.
    3. **Strategic Assessment:** Provide a high-level summary of the threat environment based on this graph snapshot.
    
    Use a professional, authoritative tone. Do not focus on "today's events"—focus on the "overall state of the threat."

    Aggregated Graph Data:
    {graph_data}
    """

    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    return chain.invoke({"graph_data": data, "date": date_str}).content
