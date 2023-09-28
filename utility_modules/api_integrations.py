import os
import requests
from google.cloud import dialogflow
from google.cloud import language_v1
from google.cloud.language_v1 import enums

# Constants
GOOGLE_API_KEY = os.environ.get("googleapi")
WOLFRAM_ALPHA_APP_ID = "UW5Y4E-56Y3AK853L"
PROJECT_ID = "chatbot-400406"

# Initialize Dialogflow client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("googleapi")
session_client = dialogflow.SessionsClient()

def wolfram_alpha_query(query):
    base_url = "http://api.wolframalpha.com/v1/result?"
    params = {
        "i": query,
        "appid": WOLFRAM_ALPHA_APP_ID,
        "format": "plaintext"
    }
    response = requests.get(base_url, params=params)
    return response.text if response.status_code == 200 else "Sorry, I couldn't fetch the information from Wolfram Alpha."

def analyze_text(text):
    client = language_v1.LanguageServiceClient()
    document = {"content": text, "type": enums.Document.Type.PLAIN_TEXT, "language": "en"}
    analysis = client.analyze_sentiment(document=document)
    sentiment = analysis.document_sentiment
    return sentiment.score, sentiment.magnitude

def get_dialogflow_response(text, language_code="en"):
    session_id = "197458744"  # Consider generating this dynamically
    session = session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text
