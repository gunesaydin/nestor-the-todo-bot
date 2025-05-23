import os

from dotenv import load_dotenv
from http.server import HTTPServer
import requests

from web_request_handler import WebRequestHandler

def main():
    print("Hello, World!")

def setup_webhook():
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    
    webhook_info_response = requests.get(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getWebhookInfo",
    )

    if webhook_info_response.ok == True and webhook_info_response.json().get("result").get("url") == WEBHOOK_URL:
        print("Webhook is already set.")
    else:
        response = requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook",
            params={"url": WEBHOOK_URL},
        )
        print("Setting webhook...")
        if response.ok == True:
            print("Webhook set successfully.")
        else:
            print("Failed to set webhook:", response.ok)
        

if __name__ == "__main__":
    setup_webhook()
    print("Starting server...")
    print("Serving on port 80")
    server = HTTPServer(("0.0.0.0", 80), WebRequestHandler)
    server.serve_forever()

main()