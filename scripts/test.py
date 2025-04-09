
import os
import requests
from collections import namedtuple
import requests
import time
from collections import namedtuple
import openai
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_models import ChatPerplexity
from langchain_core.prompts import ChatPromptTemplate

import json

envv = os.environ.get('OPENAI_API_KEY')
api_key = envv

# Load the API key from the configuration file
with open('/home/gcp01/verilog-eval/key_config.json') as config_file:
    config = json.load(config_file)

# url = 'https://api.openai.com/v1/chat/completions'

# headers = {
#     'Authorization': f'Bearer {api_key}',
#     'Content-Type': 'application/json'
# }

# data = {
#     "model": "o1-mini",
#     "messages": [{"role": "user", "content": "Hello, who won the world series in 2020?"}]
# }

# response = requests.post(url, headers=headers, json=data)

# if response.status_code == 200:
#     completion = response.json()
#     print(completion['choices'][0]['message']['content'])
# else:
#     print(f"Request failed with status code {response.status_code}: {response.text}")




prompt_ ='''
You only complete chats with syntax correct Verilog code. End the Verilog module code completion with 'endmodule'. Do not include module, input and output definitions

// Implement the Verilog module based on the following description. Assume that signals are positive clock/clk triggered unless otherwise stated.
// 
// Build a circuit that always outputs a LOW.
// 

module TopModule (
  output zero
);
Using o1-mini model directly via OpenAI API
'''


# url = 'https://api.openai.com/v1/chat/completions'
# headers = {
#     'Authorization': f'Bearer {api_key}',
#     'Content-Type': 'application/json'
# }

# # Correct message format and parameters for o1 models
# data = {
#     "model": "o1-mini",  # Use the actual model name from the variable
#     "messages": [{"role": "user", "content": prompt_}],
#     "max_completion_tokens": 2048
# }

# resp = None
# cb = None

# for _ in range(10):
#     response = requests.post(url, headers=headers, json=data)
#     if response.status_code == 200:
#         response_json = response.json()
#         resp = namedtuple('Response', ['content'])(content=response_json['choices'][0]['message']['content'])
#         print(resp)
#         cb = namedtuple('Callback', ['prompt_tokens', 'resp_tokens', 'total_tokens', 'total_cost', 'completion_tokens'])(
#             prompt_tokens=response_json['usage']['prompt_tokens'], 
#             resp_tokens=response_json['usage']['completion_tokens'], 
#             total_tokens=response_json['usage']['total_tokens'], 
#             total_cost=0, 
#             completion_tokens=response_json['usage']['completion_tokens']
#         )
#         break
#     else:
#         print("")
#         print(f"ERROR: LLM query failed with status {response.status_code}, retrying in 20 seconds")
#         print(f"{response.text}")
#         print("")






# chat = ChatPerplexity(
#             model="r1-1776",
#             pplx_api_key=config["perplexity_api_key"],
#             max_tokens=120,
#             temperature=0.8
#         )
        
# system = "You are a helpful assistant."
# human = "{input}"
# prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

# chain = prompt | chat
# response = chain.invoke({"input": "Why is the Higgs Boson important?"})
# response.content


from openai import OpenAI
import json
from collections import namedtuple
import time

# ...existing code...

YOUR_API_KEY = config["perplexity_api_key"]
messages = [{"role": "user", "content": prompt_}]

client = OpenAI(
    api_key=config["perplexity_api_key"], 
    base_url="https://api.perplexity.ai"
)

for _ in range(3):
    try:
        # Chat completion without streaming
        response = client.chat.completions.create(
            model="r1-1776",
            messages=messages
        )
        
        # Extract content directly from response object
        content = response.choices[0].message.content

        # Remove <thinking> tags
        contents = content.split("</think>")
        if len(contents)>1:
            content = contents[1]
            
        
        # Create response namedtuple
        resp = namedtuple('Response', ['content'])(content=content)
        print(resp.content)
        
        # Create callback namedtuple with usage information
        cb = namedtuple('Callback', ['prompt_tokens', 'resp_tokens', 'total_tokens', 'total_cost', 'completion_tokens'])(
            prompt_tokens=response.usage.prompt_tokens,
            resp_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
            total_cost=0,
            completion_tokens=response.usage.completion_tokens
        )
        break
        
    except Exception as e:
        print(f"\nERROR: Perplexity query failed with error: {str(e)}, retrying in 20 seconds\n")
        time.sleep(20)

