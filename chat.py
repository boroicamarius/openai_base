from necessary.init import *

class Chat:
    def system_message(self,message):
        self.messages.append({"role":"system","content":message})
        
    def send_message(self,message) -> str:
        self.messages.append({"role":"user","content":message})
        return self.run(False)
        
    def send_function_result(self,res):
        self.messages.append({"role":"function","name":"search_online", "content":res})
        return self.run(True)
    
    def add_function(self,function):
        self.functions.append(function)
        
    def run(self, no_fun):
        if(no_fun==False and len(self.functions)!=0):
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613", 
                messages=self.messages,
                functions=self.functions
            )
        else:
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613", 
                messages=self.messages,
            )
        msg = res.choices[0]
        self.messages.append(msg.message)
        if(msg.message.content): print("AI: "+msg.message.content)
        return msg
        
    def __init__(self):
        self.messages = []
        self.functions = []
