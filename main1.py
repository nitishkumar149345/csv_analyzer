from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.agents import AgentType
from dotenv import load_dotenv
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import re, os
import base64
import requests

# save your openai api key in .env file or make it as a environment variables 
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')


class CsvAnalyzer():
    def __init__(self) -> None:
        pass
    # Method to analyze a CSV file using an OpenAI language model
    def csv_model(self,file, query):
        agent = create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        file, 
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )
        # Define input for the agent with the provided query
        tool_input = {
            "input": {
            "name": "python",
            "arguments":query
            }
        }

        # Invoke the agent with the input and retrieve the response
        response = agent.invoke(tool_input)
        return response['output']
    
    # Method to process a graph image and generate an explanation
    def process_graph(self,img,df):
        # Read the image file and encode it to base64
        with open(img, 'rb') as image_file:
            image = image_file.read()
            base64_image = base64.b64encode(image).decode('utf-8') 
        
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }

        # Prepare payload with the graph data and image for the OpenAI API
        payload = {
        "model": "gpt-4o",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"Explain the graph of this data:{df}.follow proper structure in generating the output."
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
                }
            ]
            }
        ],
        "max_tokens": 1000
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        ans= response.json()
        return ans['choices'][0]['message']['content']

