from typing import List
from twilio.rest import Client

from get_env import get_env

TWILIO_AUTH_TOKEN = get_env("TWILIO_AUTH_TOKEN")


def send_sms(phone_numbers: List[str], message: str) -> bool:

    account_sid = "ACad27668acfcbbc413a2945e48864a477"
    client = Client(account_sid, TWILIO_AUTH_TOKEN)

    for number in phone_numbers:
        print(f"DEBUG sending '{message}' to number {number}")
        response = client.messages.create(
        from_ ='+17865743633',
        body=message,
        to=number
        )
        print(f"DEBUG response: {response}")
    return True


if __name__ == "__main__":
    send_sms(["+48693343789"], "test message")
