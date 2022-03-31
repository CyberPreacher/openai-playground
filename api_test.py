import os
from dotenv import load_dotenv, find_dotenv

#path ="/Users/bryanrandell/PycharmProjects/openai-playground/.env.txt"

#load_dotenv(dotenv_path=path,verbose=True)

load_dotenv()

api = os.getenv("OPENAI_API_KEY")
print(api)