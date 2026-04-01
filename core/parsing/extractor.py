from pydantic_ai import Agent
from pydantic_ai.models.huggingface import HuggingFaceModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv
import os

from core.parsing.schema import Resume


load_dotenv() # unnecessary if deployed on huggingface space.
api_key = os.environ["HF_TOKEN"]   # raises error if missing



model = HuggingFaceModel(
    'Qwen/Qwen2.5-7B-Instruct',
    provider=OpenAIProvider(
        base_url="https://router.huggingface.co/v1",
        api_key=api_key
        )
    )


agent = Agent(
    model=model,
    system_prompt=(
            'You are an expert resume extractor.'
            'If the context is not a Resume return null and DO NOT infer or hallucinate.'
            'Do NOT infer or hallucinate missing sections.'
            'If a section is not explicitly present, return null or empty list.'
        ),
    output_type=Resume
)


def extract_resume(text: str) -> Resume:
    result = agent.run_sync(text)
    return result.output