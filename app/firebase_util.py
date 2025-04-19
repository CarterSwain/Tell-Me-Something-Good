# firebase_util.py (now just handles Expo pushes)

import requests

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"

def send_push_notification(title, body, expo_token):
    payload = {
        "to": expo_token,
        "title": title,
        "body": body,
        "sound": "default"
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(EXPO_PUSH_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Expo push error: {response.text}")

    print("✅ Expo Push sent! Response:", response.json())
    return response.json()
