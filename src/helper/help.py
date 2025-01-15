import requests
import json
from dotenv import load_dotenv, find_dotenv
import os
from wolframalpha import Client
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from pygments import highlight, lexers, formatters
import nest_asyncio
import base64
import math


nest_asyncio.apply()

def load_env():
    _ = load_dotenv(find_dotenv())

def llama32(messages, model_size=11):
    model = f"meta-llama/Llama-3.2-{model_size}B-Vision-Instruct-Turbo"
    url = f"{os.getenv('API_BASE_URL', 'https://api.together.xyz')}/v1/chat/completions"
    payload = {
        "model": model,
        "max_tokens": 4096,
        "temperature": 0.0,
        "stop": ["<|eot_id|>","<|eom_id|>"],
        "messages": messages
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}"
    }
    res = json.loads(requests.request("POST", url, headers=headers, data=json.dumps(payload)).content)

    if 'error' in res:
        raise Exception(res['error'])

    return res['choices'][0]['message']['content']

def get_wolfram_alpha_api_key():
    load_env()
    wolfram_alpha_api_key = os.getenv("WOLFRAM_ALPHA_KEY")
    return wolfram_alpha_api_key

def get_tavily_api_key():
    load_env()
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    return tavily_api_key

def llama31(prompt_or_messages, model_size=8, temperature=0, raw=False, debug=False):
    model = f"meta-llama/Meta-Llama-3.1-{model_size}B-Instruct-Turbo"
    if isinstance(prompt_or_messages, str):
        prompt = prompt_or_messages
        url = f"{os.getenv('API_BASE_URL', 'https://api.together.xyz')}/v1/completions"
        payload = {
            "model": model,
            "temperature": temperature,
            "prompt": prompt
        }
    else:
        messages = prompt_or_messages
        url = f"{os.getenv('API_BASE_URL', 'https://api.together.xyz')}/v1/chat/completions"
        payload = {
            "model": model,
            "temperature": temperature,
            "messages": messages
        }

    if debug:
        print(payload)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}"
    }

    try:
        response = requests.post(
            url, headers=headers, data=json.dumps(payload)
        )
        response.raise_for_status()  # Raises HTTPError for bad responses
        res = response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")

    if 'error' in res:
        raise Exception(f"API Error: {res['error']}")

    if raw:
        return res

    if isinstance(prompt_or_messages, str):
        return res['choices'][0].get('text', '')
    else:
        return res['choices'][0].get('message', {}).get('content', '')

def disp_image(address):
    if address.startswith("http://") or address.startswith("https://"):
        response = requests.get(address)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(address)
    
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def resize_image(img, max_dimension = 1120):
    original_width, original_height = img.size

    if original_width > original_height:
        scaling_factor = max_dimension / original_width
    else:
        scaling_factor = max_dimension / original_height

    new_width = int(original_width * scaling_factor)
    new_height = int(original_height * scaling_factor)

    # Resize the image while maintaining aspect ratio
    resized_img = img.resize((new_width, new_height))

    resized_img.save("images/resized_image.jpg")

    print("Original size:", original_width, "x", original_height)
    print("New size:", new_width, "x", new_height)

    return resized_img
