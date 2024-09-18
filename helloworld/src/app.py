import json
from nacl.signing import VerifyKey
import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from commands import send_message

DISCORD_PUBLIC_KEY = os.getenv("DiscordPublicKey")
DISCORD_BOT_ID = os.getenv("DiscordBotId") # https://docs.discloud.com/v/en/suport/faq/id-bot

def lambda_handler(event, context):
    try:
        raw_body = event['body']
        auth_sig = event['headers'].get('x-signature-ed25519')
        auth_ts = event['headers'].get('x-signature-timestamp')
        verify_key = VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY))
        verify_key.verify(f'{auth_ts}{raw_body}'.encode(), bytes.fromhex(auth_sig))
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")

    body = json.loads(raw_body)
    if body["type"] == 1:
        return { 'statusCode': 200, 'body': json.dumps({ 'type': 1 })}
    
    send("Loading...", body['id'], body['token'])
    updated_message = send_message()
    update(updated_message, body['token'], DISCORD_BOT_ID)

def send(message, id, token):
    url = f"https://discord.com/api/interactions/{id}/{token}/callback"
    callback_data = { "type": 4, "data": { "content": message } }
    requests.post(url, json=callback_data)

def update(message, token, app_id):
    url = f"https://discord.com/api/webhooks/{app_id}/{token}/messages/@original"
    data = { "content": message }
    requests.patch(url, json=data)