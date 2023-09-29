import requests
import os
from google.cloud import dialogflow
from google.cloud import language_v1

GOOGLE_API_KEY = os.environ.get("googleapi")
WOLFRAM_ALPHA_APP_ID = "UW5Y4E-56Y3AK853L"

# Set up Dialogflow client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("googleapi")
session_client = dialogflow.SessionsClient()
project_id = "chatbot-400406"
session_id = "197458744"

import requests
import os
from google.cloud import dialogflow
from google.cloud import language_v1

GOOGLE_API_KEY = os.environ.get("googleapi")
WOLFRAM_ALPHA_APP_ID = "UW5Y4E-56Y3AK853L"

# Set up Dialogflow client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("googleapi")
session_client = dialogflow.SessionsClient()
project_id = "chatbot-400406"
session_id = "197458744"

def wolfram_alpha_query(query):
    base_url = "http://api.wolframalpha.com/v1/result?"
    params = {
        "i": query,
        "appid": WOLFRAM_ALPHA_APP_ID,
        "format": "plaintext"
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return "Sorry, I couldn't fetch the information from Wolfram Alpha."

client = language_v1.LanguageServiceClient()

def analyze_text(text):
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language="en")
    try:
        analysis = client.analyze_sentiment(request={"document": document})
        sentiment = analysis.document_sentiment
        return sentiment.score, sentiment.magnitude
    except Exception as e:
        return f"Error analyzing text: {str(e)}"

def get_dialogflow_response(text, language_code="en"):
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(request={"session": session, "query_input": query_input})
        return response.query_result.fulfillment_text
    except Exception as e:
        return f"Error fetching response from Dialogflow: {str(e)}"

