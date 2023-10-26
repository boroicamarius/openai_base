import os, openai
from dotenv import load_dotenv

def api_key():
    return os.getenv("API_KEY")

def org_key():
    return os.getenv("ORG_KEY")

load_dotenv()

openai.api_key = api_key()
openai.organization = org_key()
