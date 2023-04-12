# from openplayground_api import openplayground
import openplayground
openplayground.user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
auth = openplayground.Auth()

import os
from dotenv import load_dotenv
from tinydb import TinyDB, Query, where
from typing import List, Dict, Callable, Any

#---logging-----------
# import loguru
# from loguru import logger
# import pysnooper
# logger.add("logs/log.txt", rotation="3 MB", encoding="utf8", enqueue=True)

db = TinyDB('token.json')
load_dotenv(verbose=True)
email =  os.environ.get("EMAIL")


class NatdevApi(openplayground.Client):

    def __init__(self, email) -> None:
        token = self.get_token(email=email)
        super().__init__(token, email=email)
        # self.client = openplayground.Client(token, email=email)

    def get_token(self, email):
        tokens = db.search(where('email')==email)
        if (len(tokens) > 0) and ('token' in tokens[0]):
            token = tokens[0]['token']
            return token
        else:
            auth.send_otp_code(email)
            otp_code = input("Enter OTP code: ")
            token = auth.verify_otp_code(otp_code)
            db.upsert({"email": email, "token": token}, where('token')==token)
            return token
        
    def get_otp_to_save(self, email):
        auth.send_otp_code(email)
        otp_code = input("Enter OTP code: ")
        token = auth.verify_otp_code(otp_code)
        db.upsert({"email": email, "token": token}, where('token')==token)
        return token

    def create(self, model="openai:gpt-4", prompt="") -> str:
        message = ""
        # for chunk in self.generate(model, prompt, maximum_length=3900, temperature=0, top_k=50, top_p=0.95):
        for chunk in self.generate(model, prompt, maximum_length=3900):
            if chunk["event"] == "infer":
                message += chunk["message"]
        # logger.debug(message)
        # print(message)
        return message
    

if __name__ == '__main__':


    client = NatdevApi(email)


    print(client.models.keys())
    
    prompt = "You are AGI_Builder_GPT. Your goal is to write code and make actionable suggestions in order to improve an AI called \"Auto-GPT\", so as to broaden the range of tasks it's capable of carrying out."
    msg = client.create(model="openai:gpt-4", prompt=prompt)
    import pdb;pdb.set_trace()
    print(msg)
    
    