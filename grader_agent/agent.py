from langgraph.graph import StateGraph, END
from config import AgentState
from tools import parse_rubric_xml

# Import the nodes we defined
from sub_agents.extractor_agent import extractor_node
from sub_agents.researcher_agent import researcher_node
from sub_agents.grader_agent import grader_node

# 1. Create the Graph
workflow = StateGraph(AgentState)

# 2. Add Nodes
workflow.add_node("extractor", extractor_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("grader", grader_node)

# 3. Define Edges (The Logic Flow)
workflow.set_entry_point("extractor")
workflow.add_edge("extractor", "researcher")
workflow.add_edge("researcher", "grader")
workflow.add_edge("grader", END)

# 4. Compile
app = workflow.compile()

# --- Main Execution Block ---
if __name__ == "__main__":
    # 1. Setup paths
    pdf_file = "../input/student_submission.pdf"
    xml_file = "../input/rubric.xml"
    
    print(f"Loading rubric from {xml_file}...")
    
    # 2. Parse Rubric (Pre-processing)
    rubric_content = parse_rubric_xml(xml_file)
    
    # 3. Initialize State
    initial_state = {
        "filepath": pdf_file,
        "rubric_path": xml_file,
        "parsed_rubric": rubric_content # Store it in state
    }
    
    # 4. Run the Graph
    print(f"Starting GradeFlow...")
    result = app.invoke(initial_state)
    
    print("\n=== GRADING COMPLETE ===")
    print(f"Score: {result['final_grade']['score']}/100")