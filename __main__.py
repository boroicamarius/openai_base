import json
import requests
import os
from html_to_txt import get_text
from pprint import pprint
from chat import Chat
from necessary.init import *

subscription_key = os.getenv('BING_SEARCH_V7_SUBSCRIPTION_KEY')
endpoint = os.getenv('BING_SEARCH_V7_ENDPOINT') + "/v7.0/search"

chat = Chat()

"""chat.system_message("You are a lawyer giving the best responses to the user, your job is to give a clear and short answer with the information that the user wants,work together with the user to find a resolution, if the user makes a question about something specific always search online if it is the case")"""

chat.system_message("You are a lawyer giving the best responses to the user, your job is to give a clear and short answer with the information that the user wants,work together with the user to find a resolution, if the user makes a question about something specific always search online")

chat.add_function(
    {
      "name": "search_online",
      "description": "Search anything online to find more data about something",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "Keywords or sentences to find the perfect content on google"
          },
        },
        "required": ["query"]
      }
    }
)

while(True):
    user_input =  input("YOU: ");
    msg = chat.send_message(user_input);
    if(msg.finish_reason=="function_call" and msg.message.function_call.name=="search_online"):
        print("AI DECIDED TO MAKE A FUNCTION CALL")
        query = json.loads(msg.message.function_call.arguments)["query"]
        print(query)
        try:
            response = requests.get(
              endpoint, 
              headers={ 'Ocp-Apim-Subscription-Key': subscription_key },
              params={'q':query,'mkt':'en-GB'})
            response.raise_for_status()
            json = response.json()['webPages']['value']
            text = []
            count=0
            for part in json:
              if count==3: break
              try:
                text.append(" ".join(get_text(part['url']).strip().replace("\n",'').replace("\r",'').split()))
                count+=1
              except:
                pass
            
            res = ""
            for item in text:
              res+=openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=[{"role":"system","content":f"summarize the text with only important information that match \"{query}\""},
                          {"role":"assistant","content":item}]           
              ).choices[0].message.content
              
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=[{"role":"system","content":f"summarize all the text with information that match \"{query}\", the text will be maximul 300 characters in length"},
                          {"role":"assistant","content":res}]           
              ).choices[0].message.content
            
            chat.send_function_result(res)
            
        except Exception as ex:
            raise ex
