import logging

from telethon.sync import TelegramClient, events
from telethon.tl.types import UserStatusOnline, UserStatusRecently

from settings import API_ID, API_HASH, BOT_TOKEN


logging.basicConfig(level=logging.INFO)

# Configuration
bot_token = BOT_TOKEN
api_id = API_ID
api_hash = API_HASH

# Initialize the Telegram client
client = TelegramClient('bot_session', api_id, api_hash)


# Event handlers
@client.on(events.NewMessage(pattern='/tageveryone'))
async def tag_everyone(event):
    chat = event.chat_id

    # Get a list of all users in the chat
    users = await client.get_participants(chat)

    tag_string = ' '.join([f'@{user.username}' for user in users if user.username])

    await event.respond(tag_string)


@client.on(events.NewMessage(pattern='/tagbykeywords (.+)'))
async def tag_by_keywords(event):
    # Get the keyword from the user's message
    keyword = event.pattern_match.group(1).lower()

    # Check if the message contains the keyword
    if keyword:
        async for message in event.client.iter_messages(event.chat_id, search=keyword):
            # Skip tagging the user who issued the command
            if message.sender_id != event.sender_id:
                # Tag other users who sent a message containing the keyword
                await event.reply(f'@{message.sender.username} tagged for saying {keyword}')
                break


@client.on(events.NewMessage(pattern='/tagbyactivity'))
async def tag_by_activity(event):
    chat = event.chat_id

    users = await client.get_participants(chat)

    # Filter users who are online
    active_users = [f'@{user.username}' for user in users if isinstance(user.status, UserStatusOnline)]

    if active_users:
        tag_string = ' '.join(active_users)
        await event.respond(tag_string)
    else:
        await event.respond("No active users found in the chat.")


@client.on(events.NewMessage(pattern='/tagbyrecentactivity'))
async def tag_by_recent_activity(event):
    chat = event.chat_id

    users = await client.get_participants(chat)

    active_users = [f'@{user.username}' for user in users if isinstance(user.status, UserStatusRecently)]

    if active_users:
        tag_string = ' '.join(active_users)
        await event.respond(tag_string)
    else:
        await event.respond("No users found who were active recently.")


# Start the client
def main():
    with client:
        client.start(bot_token=bot_token)
        client.run_until_disconnected()


if __name__ == '__main__':
    main()
