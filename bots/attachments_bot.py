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

            prompt = [{"role": "user", "content": turn_context.activity.text}]
           
            response = openai.ChatCompletion.create(engine="tuckerai", messages=prompt, max_tokens=1024, temperature=0.6)

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



