from config import AgentState
from tools import read_pdf_submission

def extractor_node(state: AgentState):
    print(f"--- [Extractor Agent] Reading file: {state['filepath']} ---")
    
    # We invoke the tool directly since this step is deterministic (no LLM needed)
    extracted_text = read_pdf_submission.invoke(state["filepath"])
    
    # Update the state with the text
    return {"submission_text": extracted_text}