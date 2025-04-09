import requests
import time
from collections import namedtuple
import openai
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_models import ChatPerplexity
from openai import OpenAI

class BaseModel:
    def __init__(self, model, config, system_msg, full_prompt, temperature, top_p, max_tokens):
        self.model = model
        self.config = config
        self.system_msg = system_msg
        self.full_prompt = full_prompt
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

    def query(self):
        raise NotImplementedError("Subclasses should implement this method")

class OpenAIModel(BaseModel):
    def query(self):
        openai.api_key = self.config["openai_api_key"]
        messages = [{"role": "user", "content": self.system_msg + "\n\n" + self.full_prompt}]
        for _ in range(10):
            try:
                client = openai.OpenAI()
                response = client.chat.completions.create(
                    model= self.model,
                    messages= messages,
                    max_completion_tokens= self.max_tokens
                )
    
                # Pricing
                prompt_token_price = 0.00000055  # price per prompt token
                completion_token_price = 0.0000044  # price per completion token

                return namedtuple('Response', ['content'])(content=response.choices[0].message.content), \
                       namedtuple('Callback', ['prompt_tokens', 'resp_tokens', 'total_tokens', 'total_cost', 'completion_tokens'])(
                           prompt_tokens=response.usage.prompt_tokens,
                           resp_tokens=response.usage.completion_tokens,
                           total_tokens=response.usage.total_tokens,
                           total_cost=(response.usage.prompt_tokens * prompt_token_price) + (response.usage.completion_tokens * completion_token_price),
                           completion_tokens=response.usage.completion_tokens
                       )
            except openai.OpenAIError as e:
                print(f"ERROR: LLM query failed with error {e}, retrying in 20 seconds")
                time.sleep(20)
        return None, None

class ClaudeModel(BaseModel):
    def query(self):
        api_key = self.config["anthropic_api_key"]
        chat = ChatAnthropic(
            model=self.model, 
            anthropic_api_key=api_key,
            temperature=self.temperature,
            top_p=self.top_p
        )
        
        for _ in range(10):  # Reduced retries for Claude
            try:
                messages = [ SystemMessage(self.system_msg), HumanMessage(self.full_prompt) ]
                response = chat.invoke(messages)

                if response and hasattr(response, 'content'):
                    # Estimate tokens since metadata isn't available
                    input_text_ = self.system_msg + self.full_prompt    
                    estimated_input_tokens = len(input_text_.encode('utf-8')) // 4
                    estimated_output_tokens = len(response.content.encode('utf-8')) // 4
                    # Claude 3.5 / 3.7 Sonnet pricing
                    input_price = 0.000003
                    output_price = 0.000015
                    total_cost = (estimated_input_tokens * input_price) + (estimated_output_tokens * output_price)

                    # contents = response.content.split("implementation:")
                    # if len(contents)>1:
                    #     response.content = contents[1]
                    
                return namedtuple('Response', ['content'])(content=response.content), \
                       namedtuple('Callback', ['prompt_tokens', 'resp_tokens', 'total_tokens', 'total_cost', 'completion_tokens'])(
                            prompt_tokens=estimated_input_tokens,
                            resp_tokens=estimated_output_tokens,
                            total_tokens=estimated_input_tokens + estimated_output_tokens,
                            total_cost=total_cost,
                            completion_tokens=estimated_output_tokens
                       )
            except Exception as e:
                print(f"ERROR: Claude query failed with error {e}, retrying in 20 seconds")
                time.sleep(20)
        return None, None

class PerplexityModel(BaseModel):
    def query(self):
        client = OpenAI(
            api_key= self.config["perplexity_api_key"], 
            base_url="https://api.perplexity.ai"
        )
        
        for _ in range(10):  # Reduced retries
            try:
                messages = [{"role": "user", "content": self.system_msg + "\n\n" + self.full_prompt}]
                response = client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    max_tokens=self.max_tokens
                )

                if response and hasattr(response, 'choices'):
                    # Perplexity r1-1776 pricing 
                    input_price = 0.000002
                    output_price = 0.000008  

                    content = response.choices[0].message.content
                    # Remove <thinking> tags
                    contents = content.split("</think>")
                    if len(contents)>1:
                        content = contents[1]

                    return namedtuple('Response', ['content'])(content=content
                    ), namedtuple('Callback', ['prompt_tokens', 'resp_tokens', 'total_tokens', 'total_cost', 'completion_tokens'])(
                        prompt_tokens=response.usage.prompt_tokens,
                        resp_tokens=response.usage.completion_tokens,
                        total_tokens=response.usage.total_tokens,
                        total_cost=response.usage.prompt_tokens*input_price + response.usage.completion_tokens*output_price,
                        completion_tokens=response.usage.completion_tokens
                    )
            except Exception as e:
                print(f"ERROR: Perplexity query failed with error {e}, retrying in 20 seconds")
                time.sleep(20)
        return None, None


# Add more model classes as needed...

def get_model_instance(model, config, system_msg, full_prompt, temperature, top_p, max_tokens):
    if model in ["o1-mini"]:
        return OpenAIModel(model, config, system_msg, full_prompt, temperature, top_p, max_tokens)
    elif model in ["claude-3-5-sonnet-20241022","claude-3-7-sonnet-20250219"]:
        return ClaudeModel(model, config, system_msg, full_prompt, temperature, top_p, max_tokens)
    elif model in ["r1-1776"]:
        return PerplexityModel(model, config, system_msg, full_prompt, temperature, top_p, max_tokens)
    return None