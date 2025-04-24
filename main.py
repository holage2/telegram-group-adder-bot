from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest, InviteToChannelRequest
from telethon.tl.types import ChannelParticipantsSearch
import csv
import time

api_id = 23227708
api_hash = "693cc2af54c6112d21cb6f26b0693569"
phone = "YOUR_PHONE_NUMBER"  # Replace with your phone number

client = TelegramClient(phone, api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input("Enter the code: "))

source_group = "https://t.me/Lucknow_University_Students"
target_group = "https://t.me/lkodisc"

def scrape_members():
    print("Scraping members...")
    all_participants = []
    offset_user = 0
    limit_user = 100
    while True:
        participants = client(GetParticipantsRequest(
            source_group, ChannelParticipantsSearch(''), offset_user, limit_user, hash=0))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset_user += len(participants.users)
    with open("numbers.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["username", "user_id", "access_hash", "name"])
        for user in all_participants:
            if user.username:
                writer.writerow([user.username, user.id, user.access_hash, user.first_name])

def add_members():
    with open("numbers.csv", "r", encoding='utf-8') as f:
        rows = csv.reader(f)
        next(rows, None)
        for row in rows:
            try:
                user = client.get_input_entity(row[0])
                client(InviteToChannelRequest(target_group, [user]))
                print(f"Added {row[0]}")
                time.sleep(30)
            except Exception as e:
                print(f"Could not add {row[0]}: {e}")
                time.sleep(5)

scrape_members()
add_members()