import xml.etree.ElementTree as ET
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_core.tools import tool

# --- ROBUST IMPORT FOR TAVILY ---
try:
    # Try the new valid path first
    from langchain_tavily import TavilySearchResults
except ImportError:
    # Fallback to the old path (works but gives a warning)
    from langchain_community.tools.tavily_search import TavilySearchResults

def parse_rubric_xml(xml_path: str) -> str:
    """
    Parses the XML Rubric with 6 distinct levels per criterion.
    Returns a formatted string for the LLM System Prompt.
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        rubric_text = "### GRADING RUBRIC INSTRUCTIONS:\n"
        rubric_text += "For each criterion, select the Level (percentage) that best matches the work. Calculate the weighted score based on that percentage.\n\n"
        
        for criterion in root.findall('criterion'):
            name = criterion.find('name').text
            weight = criterion.find('weight').text
            rubric_text += f"#### Criterion: {name} (Max Points: {weight})\n"
            
            # Loop through the 6 levels
            levels = criterion.find('levels')
            if levels is not None:
                for lvl in levels.findall('level'):
                    pct = lvl.get('percentage')
                    desc = lvl.text
                    rubric_text += f"- **{pct}% Level**: {desc}\n"
            rubric_text += "\n"
            
        return rubric_text
    except Exception as e:
        return f"Error reading rubric XML: {str(e)}"

@tool
def read_pdf_submission(file_path: str) -> str:
    """Reads PDF content."""
    try:
        loader = PDFPlumberLoader(file_path)
        docs = loader.load()
        return "\n".join([d.page_content for d in docs])
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# Initialize the tool
search_tool = TavilySearchResults(max_results=1)