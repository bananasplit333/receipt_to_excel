from openai import OpenAI
import os 
from dotenv import load_dotenv, find_dotenv

def load_environment_variables():
    load_dotenv(find_dotenv())
    pass

#initialize instance of openai 
load_environment_variables()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()