import asyncio
import re
import logging
import json
import hangups
import random

from hangups.ui.utils import get_conv_name

def _initialise(Handlers, bot=None):
    Handlers.register_admin_command(["addusers", "createconversation"])
    return []

def addusers(bot, event, *args):
    user_ids = list(set(args))
    current_conv_id = event.conv_id
    print("addusers: {}".format(user_ids))
    yield from bot._client.adduser(current_conv_id, user_ids)

def createconversation(bot, event, *args):
    user_ids = list(args)
    user_ids.insert(0, bot.user_self()["chat_id"])
    user_ids = list(set(user_ids))
    print("createconversation: {}".format(user_ids))
    response = yield from bot._client.createconversation(user_ids)
    print("createconversation: {}".format(response))
    new_conversation_id = response['conversation']['id']['id']
    bot.send_html_to_conversation(new_conversation_id, "<i>conversation created</i>")
