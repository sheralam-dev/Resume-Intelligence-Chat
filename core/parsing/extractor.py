from pydantic_ai import Agent
from pydantic_ai.models.huggingface import HuggingFaceModel
from pydantic_ai.providers.openai import OpenAIProvider

from core.parsing.schema import Resume

from dotenv import load_dotenv
import os

load_dotenv()
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
            'Do NOT infer or hallucinate missing sections.'
            'If a section is not explicitly present, return null or empty list.'
        ),
    output_type=Resume
)


def extract_resume(text: str) -> Resume:
    result = agent.run_sync(text)
    return result.output