# CHANGED: Import Google
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import search_tool
from config import AgentState, LLM_MODEL_NAME

def researcher_node(state: AgentState):
    print("--- [Researcher Agent] Verifying facts (via Gemini) ---")
    
    # CHANGED: Initialize Gemini
    llm = ChatGoogleGenerativeAI(model=LLM_MODEL_NAME, temperature=0)
    
    verify_prompt = f"""
    You are a Fact Checker. Identify the SINGLE most critical factual claim 
    in this student submission that needs verification.
    
    Submission: {state['submission_text'][:3000]}
    
    Return ONLY the query to search for.
    """
    search_query = llm.invoke(verify_prompt).content
    print(f"   Searching for: {search_query}")
    
    try:
        search_results = search_tool.invoke(search_query)
        notes = f"Fact Check Query: {search_query}\nResults: {str(search_results)}"
    except Exception as e:
        notes = f"Fact Check Failed: {str(e)}"
        
    return {"fact_check_notes": notes}