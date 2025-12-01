import os
from typing import TypedDict, Optional

def load_api_keys(filepath="../input/api_keys.txt"):
    """Reads API keys from a simple TXT file and sets them in environment."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Please create '{filepath}' with your API keys.")
    
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()

# Load keys immediately upon import
load_api_keys()

# Configuration
LLM_MODEL_NAME = "gemini-2.0-flash-exp"

# Shared State
class AgentState(TypedDict):
    filepath: str                 
    rubric_path: str              
    parsed_rubric: str            
    submission_text: str          
    fact_check_notes: str         
    final_grade: Optional[dict]