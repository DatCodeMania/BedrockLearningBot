import json

import requests

url = 'https://jamsapi.hackclub.dev/openai/chat/completions'
instruction = "Choose the number. Triple check your answer, and ONLY output the number. It is very important that you only return the number as you are being used in API state. Example output: '2'."
text = """
What did Florence Nightingale have no proof of?

She applied directly to two nurses preparing to join Florence Nightingale’s company in the Crimea, but each told her they had all the help they needed. Famous nurse Florence Nightingale herself reportedly wrote, without any proof of Mary being unscrupulous, that employing her would result in “drunkenness and improper conduct”. It was no use - her expert services were being refused based on prejudice.

1. Mary having cholera.
2. Mary's previous work as a nurse.
3. Mary's name and address.
4. Mary doing anything wrong.
"""
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer CENSORED'
}
data = {
    'model': 'gpt-3.5-turbo',
    'messages': [
        {
            'role': 'user',
            'content': f"{text}\n{instruction}"
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(data))
response_data = response.json()

print(response_data['choices'][0]['message']['content'])