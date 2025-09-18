# chatbot_app/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import os
from django.shortcuts import render
# A good practice is to store the API key in an environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAWb4Z5K7FCIPMNneg3tNJvT3dmi8rsnnw")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=" + GEMINI_API_KEY

@csrf_exempt
def chat_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        # Construct the Gemini API payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": user_message}
                    ]
                }
            ]
        }

        try:
            response = requests.post(GEMINI_API_URL, json=payload)
            response.raise_for_status() # Raise an exception for bad status codes
            gemini_response_data = response.json()

            # Extract the text from the API response
            gemini_text = gemini_response_data['candidates'][0]['content']['parts'][0]['text']

            return JsonResponse({'response': gemini_text})

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f'API request failed: {e}'}, status=500)
        except (KeyError, IndexError) as e:
            return JsonResponse({'error': f'Invalid API response format: {e}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def chat_home(request):
    return render(request, 'chatbot_app/index.html')

@csrf_exempt
def summarize_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        chat_history = data.get('history', [])

        if not chat_history:
            return JsonResponse({'error': 'No chat history provided'}, status=400)

        # Join all messages into a single string for summarization
        full_conversation = " ".join([f"{msg['sender']}: {msg['text']}" for msg in chat_history])

        # Create a prompt for Gemini to summarize the conversation
        summarize_prompt = "Summarize the following chat conversation in a single, concise sentence:\n\n" + full_conversation

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": summarize_prompt}
                    ]
                }
            ]
        }

        try:
            response = requests.post(GEMINI_API_URL, json=payload)
            response.raise_for_status()
            gemini_response_data = response.json()

            summary = gemini_response_data['candidates'][0]['content']['parts'][0]['text']

            return JsonResponse({'summary': summary})

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f'API request failed: {e}'}, status=500)
        except (KeyError, IndexError) as e:
            return JsonResponse({'error': f'Invalid API response format: {e}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)