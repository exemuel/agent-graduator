from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field 
from langchain_core.prompts import ChatPromptTemplate
from config import AgentState, LLM_MODEL_NAME

# Schema
class GradeSchema(BaseModel):
    score: int = Field(description="Final calculated numerical score out of 100")
    feedback: str = Field(description="Detailed feedback explaining why specific levels were chosen")
    citations_check: str = Field(description="Comment on factual accuracy based on research")

def grader_node(state: AgentState):
    print("--- [Grader Agent] Calculating score (via Gemini 2.0 Flash Experimental) ---")
    
    llm = ChatGoogleGenerativeAI(model=LLM_MODEL_NAME, temperature=0)
    structured_llm = llm.with_structured_output(GradeSchema)
    
    grading_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a strict university professor. 
        You MUST grade based ONLY on the provided Rubric Levels (100%, 80%, 60%, 40%, 20%, 0%).
        For each criterion:
        1. Select the specific level description that matches the student's work.
        2. Calculate the points: (Weight * Level_Percentage / 100).
        3. Sum the points for the final score.
        """),
        ("human", """
        {rubric_content}
        
        ### FACT CHECK REPORT (from Researcher Agent):
        {facts}
        
        ### STUDENT SUBMISSION:
        {submission}
        
        Provide the final output in JSON format.
        """)
    ])
    
    chain = grading_prompt | structured_llm
    
    result = chain.invoke({
        "rubric_content": state["parsed_rubric"],
        "submission": state["submission_text"],
        "facts": state["fact_check_notes"]
    })
    
    return {"final_grade": result.dict()}