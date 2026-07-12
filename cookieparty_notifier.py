import json
import os
import time
import requests

 # Configuration
TOPDECK_URL = "https://topdeck.gg/"
EVENTS_API = "https://topdeck.gg/api/organizer/mythic-hobbies/events"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1525695444292735036/jTblsktK14vOYmcFIyoOfNmLLUluZs4633ffvwVm9s2Ay1U3MTuu-gXqcDDEllkkAL1k"

CHECK_INTERVAL = 300  # seconds (5 minutes)
SEEN_FILE = "seen_events.json"


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def send_discord(event):
    message = {
        "content": (
            f"🎉 New Mythic Hobbies Event Posted!\n\n"
            f"{event['name']}\n"
            f"Date: {event.get('date', 'TBD')}\n"
            f"{TOPDECK_URL}/event/{event['id']}"
        )
    }

    requests.post(DISCORD_WEBHOOK, json=message)


def fetch_events():
    response = requests.get(EVENTS_API, timeout=15)
    response.raise_for_status()
    return response.json()


def main():
    seen = load_seen()

    while True:
        try:
            events = fetch_events()

            for event in events:
                event_id = str(event["id"])

                if event_id not in seen:
                    send_discord(event)
                    seen.add(event_id)

            save_seen(seen)

        except Exception as e:
            print("Error:", e)

        time.sleep(CHECK_INTERVAL)


if name == "main":
    main() 
