import os
import requests
import websocket

import json
import threading
import time
import random

from parser import parse_message

# To be replaced.
### WEBSOCKET

BASE_API = "https://discord.com/api/v9"


def send_json_request(ws, request):
    ws.send(json.dumps(request))


def receive_json_response(ws):
    response = ws.recv()
    print(response)
    if response:
        return json.loads(response)


payload = {
    "op": 2,
    "d": {
        "token": TOKEN,
        "intents": 512,  # or 513 for all ?
        "properties": {"$os": "linux", "$browser": "chrome", "$device": "pc"},
    },
}

payload_heartbeat = {
    "op": 1,
    "d": 2,
}


def is_MESSAGE_CREATE_type(event: dict) -> str | None:
    """
    For now: Raises if "channel_id" dont exist.

    message content is removed when using the webhook.

    1. This function filters out anything that is
    NOT a "MESSAGE_CREATE" within the given "CHANNEL_ID".
    2. It returns the message id if it exists.

    """

    if (
        (event.get("t") == "MESSAGE_CREATE")
        # and (event["d"]["author"]["id"] == AUTHOR_ID)
        and (event["d"]["channel_id"] == CHANNEL_ID)
    ):

        return True


### API CALLS


def get_message_content(id: str, last_message_id):

    messages = f"{BASE_API}/channels/{CHANNEL_ID}/webhook"
    if last_message_id:
        return f"{messages}/after?/{last_message_id}"
    else:
        return messages


def get_latest_message(latest_message):

    url = f"{BASE_API}/channels/{CHANNEL_ID}/messages?limit=1"

    headers = {
        "Authorization": TOKEN,
    }
    if not latest_message:
        response = requests.request("GET", url, headers=headers)

        return json.loads(response.content)[0]
    else:
        f"{url}&after?={latest_message}"
        response = requests.request("GET", url, headers=headers)
        return json.loads(response.content)[0]


def main():
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")
    send_json_request(ws, payload)

    class BackgroundTasksKeepWSalive(threading.Thread):
        def run(self, *args, **kwargs):
            while True:
                ws.send(json.dumps(payload_heartbeat))
                # not ideal,
                # paranoid way of preventing some bot detection mechanism that probably don't exist
                time.sleep(round(random.uniform(15, 41), 2))

    BackgroundTasksKeepWSalive().start()

    latest_message = None

    while True:
        event: dict = receive_json_response(ws)
        if event:
            if is_MESSAGE_CREATE_type(event):

                latest_message = get_latest_message(latest_message)
                print(latest_message["content"])
                parsed_latest_message = parse_message(latest_message["content"])
                if parsed_latest_message:
                    x = f"docker exec {parsed_latest_message}"
                    os.system("x")


if __name__ == "__main__":
    main()
