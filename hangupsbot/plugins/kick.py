import asyncio

from hangups.ui.utils import get_conv_name

def _initialise(Handlers, bot=None):
    Handlers.register_admin_command(["kick"])
    return []

def kick(bot, event, *args):
    user_ids_to_remove = list(set(args))
    user_ids = list()

    for u in sorted(event.conv.users, key=lambda x: x.full_name.split()[-1]):
        if not u.id_.chat_id in user_ids_to_remove:
            user_ids.append(u.id_.chat_id)

    response = yield from bot._client.createconversation(user_ids)
    new_conversation_id = response['conversation']['id']['id']
    bot.send_html_to_conversation(new_conversation_id, "<i>New conversation created</i><br /><b>Please leave the old one</b>")
    bot.send_html_to_conversation(event.conv_id, "<b>PLEASE LEAVE THIS HANGOUT</b>")

    topic = "[NEW] Hangout"
    yield from bot._client.setchatname(event.conv_id, "[DEAD]")
    yield from bot._client.setchatname(new_conversation_id, topic)
