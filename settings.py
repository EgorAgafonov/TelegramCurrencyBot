from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

currencies = {
            "RUB": "рубль",
            "CNY": "юань",
            "EUR": "евро",
            "USD": "доллар",
            "BTC": "биткоин"}

