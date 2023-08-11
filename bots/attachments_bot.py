# Author CDFH Joey Chan
# If you have any questions, please contact Joey 

import os
import urllib.parse
import urllib.request
import base64
import json
import openai
import requests
import datetime 
import time
import logging
import socket
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, CardFactory
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardAction,
    ActivityTypes,
    Attachment,
    AttachmentData,
    Activity,
    ActionTypes,
)

import sys
sys.path.append("..")
from config import DefaultConfig


CONFIG = DefaultConfig()


class AttachmentsBot(ActivityHandler):
    """
    Represents a bot that processes incoming activities.
    For each user interaction, an instance of this class is created and the OnTurnAsync method is called.
    This is a Transient lifetime service. Transient lifetime services are created
    each time they're requested. For each Activity received, a new instance of this
    class is created. Objects that are expensive to construct, or have a lifetime
    beyond the single turn, should be carefully managed.
    """

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        await self._send_welcome_message(turn_context)

    #依據輸入行為執行動作
    async def on_message_activity(self, turn_context: TurnContext):
        lcontext = turn_context.activity.text.split(" ")[0].lower()
        lcontextai = turn_context.activity.text.lower()

        if lcontext == "hello":
           await turn_context.send_activity(f"您好！我是TuckerAI!")
        #Azure openAI 3.5 testing    
        elif lcontextai[0:7] == "hi kgis":
            await turn_context.send_activity(f"證劵小幫手, 暫時無證劵的內部資料!")
        else:

            openai.api_type = "azure"
            openai.api_base = "https://tucker-ai.openai.azure.com/"
            openai.api_version = "2023-03-15-preview"
            openai.api_key = CONFIG.APP_AZURE_OPENAIAPIKEY

            last_response = ""
            #user_input = turn_context.activity.text + "使用繁體中文回答"

            user_input = turn_context.activity.text

            # Initialize messages list with the system message
            messages = [
            {"role": "system", "content": "使用繁體中文，.\
                                        簡潔答覆，忽略禮貌用語，.\
                                        你是具有多領域專長的專家，若我提出的問題，。若我提出的問題，你目前的角色無法解決目前遇到的問題，就自行切換能解決此問題的角色以獲得最佳效果，.\
                                        回答前，請說現在是擔任什麼角色，然後繼續回答，.\
                                        若我說幫我整理以下內容，請說'沒問題~我知道了'，然後用專業口吻，把內容重新敘述，辨識錯字，刪除贅字，重複語句，並且使上下文流暢好閱讀，抓重點並保留原意"},
            ]
            
            prompt =  messages.append({"role": "user", "content": user_input})

            # Only send the last 5 messages to the API
            recent_messages = messages[-5:]

            #response = openai.ChatCompletion.create(engine="tuckerai", messages=prompt, max_tokens=1024, temperature=0.6)
            response = openai.ChatCompletion.create(engine="tuckerai", messages=recent_messages, max_tokens=1024, temperature=0.6)
            # Append the assistant's response to the messages list
            messages.append({"role": "assistant", "content": response['choices'][0]['message']['content'].strip()})
            reply_msg = response['choices'][0]['message']['content']#.replace('\n','')

            await turn_context.send_activity(reply_msg)


    async def _send_welcome_message(self, turn_context: TurnContext):
        """
        Greet the user and give them instructions on how to interact with the bot.
        :param turn_context:
        :return:
        """
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                #    f"Welcome to AttachmentsBot {member.name}. This bot will introduce "
                    f"您好！我是TuckerAI,提供了ChatGPT的功能,只需輸入您的問題或要求,就會立即為您提供答案或解決方案"
                )
                #await self._display_index(turn_context)
    #錯誤訊息
    async def _send_unrecognizable_message(self, turn_context: TurnContext):
        await turn_context.send_activity(f"TuckerAI罷工中．請重新輸入")
        await self._display_index(turn_context)



