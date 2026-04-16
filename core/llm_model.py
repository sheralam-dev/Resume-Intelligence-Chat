
from langchain_openai import ChatOpenAI

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
import os
from dotenv import load_dotenv


load_dotenv() # unnecessary if deployed on huggingface space as HF has secret key.
# api_key = os.environ["HF_TOKEN"]   # raises error if missing
api_key = os.environ["GITHUB_TOKEN"]   # raises error if missing



# 1. Define the GitHub-compatible provider
github_provider = OpenAIProvider(
    base_url="https://models.inference.ai.azure.com", # GitHub Models endpoint
    api_key=api_key                   # Your GitHub PAT
)

# 2. Initialize the model using the GitHub provider
# Use model IDs like 'gpt-4o', 'meta-llama-3.1-70b-instruct', or 'DeepSeek-R1'
model1 = OpenAIChatModel(
    "gpt-4o", 
    provider=github_provider
)




model2 = ChatOpenAI(
    model="gpt-4o", # Or other models like "meta-llama-3.1-70b-instruct"
    openai_api_key=api_key,
    base_url="https://models.github.ai/inference"
)




# from pydantic_ai import Agent
# from pydantic_ai.models.openai import OpenAIChatModel
# from pydantic_ai.providers.openai import OpenAIProvider

# model1 = OpenAIChatModel(
#     # model="qwen2.5:7b-instruct",
#     "qwen2.5-7b-instruct-q4_k_m",
#     provider=OpenAIProvider(
#         base_url="http://localhost:11434/v1",  # 👈 Ollama
#         api_key="ollama"  # dummy
#     )
# )


# from langchain_ollama import ChatOllama

# model2 = ChatOllama(
#     model="Dolphin_SQL"
# )



# from pydantic_ai.models.huggingface import HuggingFaceModel
# from pydantic_ai.providers.openai import OpenAIProvider
# from dotenv import load_dotenv
# import os
# from langchain_openai import ChatOpenAI


# load_dotenv() # unnecessary if deployed on huggingface space.
# api_key = os.environ["HF_TOKEN"]   # raises error if missing


# model1 = HuggingFaceModel(
#     'Qwen/Qwen2.5-7B-Instruct',
#     provider=OpenAIProvider(
#         base_url="https://router.huggingface.co/v1",
#         api_key=api_key
#         )
#     )


# # Initialize using the OpenAI-compatible router
# model2 = ChatOpenAI(
#     model='Qwen/Qwen2.5-7B-Instruct',
#     openai_api_key=api_key,
#     openai_api_base="https://router.huggingface.co/v1"
# )