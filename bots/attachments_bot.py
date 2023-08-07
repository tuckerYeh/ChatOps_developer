# Author CDFH Joey Chan
# If you have any questions, please contact Joey 

import os
import urllib.parse
import urllib.request
import base64
import json
import redis
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
        FORMAT = '%(asctime)s %(levelname)s: %(message)s'
        user_name = turn_context.activity.from_property.name
        logName = 'My_Bot.log'
        logging.basicConfig(level=logging.INFO, filename=logName, filemode='w', format=FORMAT)

        if lcontext == "hello":
           await turn_context.send_activity(f"您好！我是證劵小幫手!")


        #Azure openAI 3.5 testing
        
        elif lcontextai[0:7] == "hi kgis":
            await turn_context.send_activity(f"證劵小幫手, 暫時無證劵的內部資料!")
       
        else:
            #ELK and redis address
            # ip = "10.129.12.11"
            # elk_port = 50000
            # redis_port = 6379
            # r = redis.Redis(host=ip, port=redis_port, decode_responses=True)

            # logging.info("user name = " + user_name)

            # from_property_id = turn_context.activity.from_property.id
            # logging.info("from_property_id = " + from_property_id)

            # #get msg from redis
            # try:
            #    previous_msg = r.get(from_property_id)
            #    ai_previous_answer = r.get(from_property_id + "_answer")
            except:
               pass

            openai.api_type = "azure"
            openai.api_base = "https://tucker-ai.openai.azure.com/"
            openai.api_version = "2023-03-15-preview"
            openai.api_key = CONFIG.APP_AZURE_OPENAIAPIKEY

            if previous_msg and ai_previous_answer:
               this_message = [{"role": "user", "content": previous_msg}, {"role": "assistant", "content": ai_previous_answer}, {"role": "user", "content": turn_context.activity.text}]
               prompt = this_message
            else:
               prompt = [{"role": "user", "content": turn_context.activity.text}]

            ##log to ELK
            try:
                # msg = {"company":"kgis", "user_name": user_name, "user_msg": turn_context.activity.text}
                # msg = json.dumps(msg)
                # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # sock.connect((ip, elk_port))
                # sock.send(msg.encode())
            except:
                pass

            response = openai.ChatCompletion.create(engine="gpt-35-turbo", messages=prompt, max_tokens=1024, temperature=0.6)

            reply_msg = response['choices'][0]['message']['content']#.replace('\n','')
            ## send to redis
            try:
               r.set(from_property_id, turn_context.activity.text)
               r.set(from_property_id + "_answer", reply_msg)
            except:
               pass

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
                    f"您好！我是證劵小幫手，一個企業版的生成式AI機器人。小幫手提供了ChatGPT的功能，可以協助您更有效地處理日常業務，提高工作效率。我們的界面非常簡單易用，只需輸入您的問題或要求，小幫手就會立即為您提供答案或解決方案。相信未來能成為您工作的好夥伴，持續為您提供所需的資訊和服務！"
                )
                #await self._display_index(turn_context)
    #錯誤訊息
    async def _send_unrecognizable_message(self, turn_context: TurnContext):
        await turn_context.send_activity(f"您好！我是證劵小幫手．請重新輸入")
        await self._display_index(turn_context)



