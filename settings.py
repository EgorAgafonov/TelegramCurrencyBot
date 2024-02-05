from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
api_key = os.getenv('API_KEY')

currencies = {
            "RUB": "рубль",
            "CNY": "юань",
            "EUR": "евро",
            "USD": "доллар",
            "BTC": "биткоин"}

