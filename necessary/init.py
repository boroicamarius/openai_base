import os, openai
from dotenv import load_dotenv

def api_key():
    return os.getenv("API_KEY");

load_dotenv()

openai.api_key = api_key();
openai.organization = "org-HLov7Si5lOYtlDmNtrYZ5mT2"