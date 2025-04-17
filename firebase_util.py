import firebase_admin
from firebase_admin import credentials, messaging

# Initialize the app with your service account
cred = credentials.Certificate("service_account_key.json")  
firebase_admin.initialize_app(cred)

def send_push_notification(title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        topic='happy-news'  # All mobile clients will subscribe to this
    )
    response = messaging.send(message)
    print("Push sent! Response:", response)
    return response
