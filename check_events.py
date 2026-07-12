import json
import os
import requests

TOPDECK_URL = "https://topdeck.gg/api/events"

STORE_NAME = "Mythic Hobbies"

DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

response = requests.get(TOPDECK_URL, timeout=30)
response.raise_for_status()

events = response.json()

store_events = [
    e for e in events
    if STORE_NAME.lower() in e.get("storeName", "").lower()
]

seen_file = "seen.json"

if os.path.exists(seen_file):
    with open(seen_file) as f:
        seen = set(json.load(f))
else:
    seen = set()

new_events = []

for event in store_events:
    event_id = str(event["id"])
    if event_id not in seen:
        new_events.append(event)
        seen.add(event_id)

if new_events:
    for event in new_events:
        message = {
            "content":
                f"🎉 New Mythic Hobbies event!\n"
                f"**{event['name']}**\n"
                f"{event['date']}\n"
                f"https://topdeck.gg/event/{event['id']}"
        }

        requests.post(DISCORD_WEBHOOK, json=message)

with open(seen_file, "w") as f:
    json.dump(list(seen), f)
