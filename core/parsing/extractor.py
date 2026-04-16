from pydantic_ai import Agent

from core.parsing.schema import Resume
from core.llm_model import model1


agent = Agent(
    model=model1,
    system_prompt=(
            'You are an expert resume extractor.'
            'If the context is not a Resume return null and DO NOT infer or hallucinate.'
            'Do NOT infer or hallucinate missing sections.'
            'If a section is not explicitly present, return null or empty list.'
        ),
    output_type=Resume
)


def extract_resume(text: str) -> Resume:
    '''
    Extract data from text using pydantic ai agent. 
    
    Args:
        text (str): Text extracted from resume (using parser eg. Docling)
        
    Returns:
        Resume: Structured schema for resume
    '''
    result = agent.run_sync(text)
    return result.output