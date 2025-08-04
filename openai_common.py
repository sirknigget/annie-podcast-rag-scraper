from dotenv import load_dotenv
from openai import OpenAI
import os
from ai_common import *

MODEL_GPT_4O_MINI = "gpt-4o-mini"

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"OpenAI API Key exists and begins {api_key[:8]}")
else:
    print("OpenAI API Key not set")

openai = OpenAI()

def chat(model, system, messages):
    messages = add_system_message(system, []) + messages
    response = openai.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content

def run_with_tools(model, messages, tools):
    print(f"run_with_tools {model} {messages} {tools}")
    return openai.chat.completions.create(model=model, messages=messages, tools=tools)

def test_prompt():
    messages = add_user_message("Hello, GPT! This is a test prompt to check that you're working!", [])
    system = "You are a very kind LLM"
    response = chat("gpt-4o-mini", system, messages)
    print(response)
