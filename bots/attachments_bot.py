# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import urllib.parse
import urllib.request
import base64
import json
import redis
from botbuilder.core import TurnContext, ActivityHandler
import openai
import requests
import datetime
import time
import logging
import socket
from azure_web_search import *
#import Property
#from Property import get
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, CardFactory
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    ThumbnailCard,
    CardImage,
    CardAction,
    ActivityTypes,
    Attachment,
    AttachmentData,
    Activity,
    ActionTypes,
    AttachmentLayoutTypes,
)

#from adaptivecards import AdaptiveCard
#from adaptivecards import CardImage, ImageSet
#import bot_dict
from azure_web_search import azure_search_web
from azure_blob_search import azure_table_search
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
        ip = "10.129.12.6"
        port = 50000
        r = redis.Redis(host=ip, port=6379, decode_responses=True)
        from_property_id = turn_context.activity.from_property.id
        user_mode = from_property_id + "_mode"

        if lcontext == "hello":
           await turn_context.send_activity(f"您好！我是金控小幫手!")
           await self._display_index(turn_context)
        elif lcontext == "123":
             images_url = "https://cdf-bot-developer.azurewebsites.net/images/01.jpg"
             images_url_02 = "https://cdf-bot-developer.azurewebsites.net/images/02.jpg"
             images_url_03 = "https://cdf-bot-developer.azurewebsites.net/images/03.jpg"

             
             card = {
        "type": "AdaptiveCard",
        "version": "1.0",
        "body": [
            {
                "type": "TextBlock",
                "text": "角色展示",
                "size": "large",
                "weight": "bolder",
            },
            {
                "type": "ImageSet",
                "imageSize": "stretch",
                "images": [
                    {
                        "type": "Image",
                        "url": "https://cdf-bot-developer.azurewebsites.net/images/01.jpg",
                        "size": "large",
                    },
                    {
                        "type": "Image",
                        "url": "https://cdf-bot-developer.azurewebsites.net/images/02.jpg",
                        "size": "large",
                    },
                    {
                        "type": "Image",
                        "url": "https://cdf-bot-developer.azurewebsites.net/images/03.jpg",
                        "size": "large",
                    },
                    {
                        "type": "Image",
                        "url": "https://cdf-bot-developer.azurewebsites.net/images/04.jpg",
                        "size": "large",
                    },
                    {
                        "type": "Image",
                        "url": "https://cdf-bot-developer.azurewebsites.net/images/05.jpg",
                        "size": "large",
                    },
                ],
            },
        ],"actions": [
            {
                "type": "Action.Execute",
                "title": "查看更多",
                "url": "https://example.com/more_images",
            },
            {
                "type": "Action.Execute",
                "title": "按鈕1",
                "data": {"button_id": "1"},
            },
            {
                "type": "Action.Submit",
                "title": "按鈕2",
                "data": {"button_id": "2"},
            },
            {
                "type": "Action.Submit",
                "title": "按鈕3",
                "data": {"button_id": "3"},
            },
            {
                "type": "Action.Submit",
                "title": "按鈕4",
                "data": {"button_id": "4"},
            },
            {
                "type": "Action.Submit",
                "title": "按鈕5",
                "data": {"button_id": "5"},
            },
        ],
    }

        # 创建 Attachment 并发送给用户
             ##response = Attachment(content_type="application/vnd.microsoft.card.adaptive", content=card)
             #reply = MessageFactory.attachment(CardFactory.hero_card(card))
             #await turn_context.send_activity(reply)
             ##response = Activity(type="message",attachments=[response])
             #connector.conversations.send_to_conversation(response)
             card_attachment = CardFactory.adaptive_card(card)
             reply = MessageFactory.attachment(card_attachment)
             ##await turn_context.send_activity(response)

             #reply = MessageFactory.attachment(CardFactory.adaptive_card(card))
             await turn_context.send_activity(reply)
             

        elif lcontext == "help":
             result_data = self.help_usage()
             await turn_context.send_activity(result_data)
             #result = self.cards_generate()
             ##await self._display_index(turn_context)
        ##elif lcontext == "index":
        ##    await self._display_index(turn_context)
        ##elif lcontext == "report":
        ##   await self._display_report(turn_context)
        ##elif lcontext == "cthelp":
        ##   await self._display_ct(turn_context)
        ##elif lcontext == "devops":
        ##    await self._display_devops(turn_context)
        ##elif lcontext == "cdfhweb":
        ##    await self._display_cdfh(turn_context)

        ##elif lcontext == "cost":
        ##    cost_name = turn_context.activity.text.split(" ")[1].strip() + "_cost"
        ##    print (cost_name)
        ##    print ("http://10.129.12.6:8080/ado_upolad_report/send_photo?file_Name=" + cost_name + ".png")
        ##    r = requests.get("http://10.129.12.6:8080/ado_upolad_report/send_photo?file_Name=" + cost_name + ".png")
        ##    await self._handle_outgoing_attachment(turn_context, cost_name)

    #run pipeline command test + pipeline_id + project_name
    #Example: test 9 Selenium_Test
        elif lcontext == "test999":
           project_name = turn_context.activity.text.split(" ")[2].strip()
           run_ID = turn_context.activity.text.split(" ")[1].strip()
           r = requests.get("https://ado-api-test.azurewebsites.net/ado_pipeline/run_pipeline?pipeline_id=" + run_ID + "&project_name=" + project_name)
           await turn_context.send_activity(f"Testing " + project_name + " on going !!")
        elif lcontext == "get999":
            #Example: get uat cpu
            if len(turn_context.activity.text.split(" ")) == 3:
               my_env = turn_context.activity.text.split(" ")[1].lower()
               my_monitor = turn_context.activity.text.split(" ")[2].lower()
               r = requests.get("http://10.129.12.6:8080/azure_control/monitor_azure?env_name=" + my_env + "&monitor_name=" + my_monitor)
               time.sleep(1)
               r = requests.get("http://10.129.12.6:8080/ado_upolad_report/send_photo?file_Name=my_plot.png")
            #self._get_inline_attachment("my_plot.png")
               await self._handle_outgoing_attachment(turn_context, "my_plot")

            elif len(turn_context.activity.text.split(" ")) == 2 and turn_context.activity.text.split(" ")[1].lower() == "cost":
               r = requests.get("http://10.129.12.6:8080/ado_upolad_report/send_photo?file_Name=cdf_cost.png")
               await self._handle_outgoing_attachment(turn_context, "cdf_cost")
            else:
               await turn_context.send_activity(f"確認Azure Repo資訊")

        
        elif lcontextai[0:7] == "hi cdfh":
            await turn_context.send_activity("金控小幫手, 暫時無金控的內訊資料!")
            '''
            openai.api_type = "azure"
            openai.api_base = "https://openai-cdfh-eus-dev-ai-01.openai.azure.com/"
            openai.api_version = "2023-03-15-preview"
            openai.api_key = CONFIG.APP_AZURE_OPENAIAPIKEY
            prompt = turn_context.activity.text[8:]

            response = openai.ChatCompletion.create(engine="CDFH-Titan", messages=[{"role": "user", "content": prompt}], max_tokens=1024, temperature=0.6)

            reply_msg = response['choices'][0]['message']['content'].replace('\n','')
            await turn_context.send_activity(reply_msg)
            '''

        elif lcontextai == "execute2":
            self._post_trigger_ADOpipeline2('Pipeline-runscripts')
            await turn_context.send_activity(f"已執行專案cdfh-app\Cloud Technology之自動化測試腳本：Pipeline-runscripts")
        
        elif lcontextai == "conn_web":
            #user_mode = from_property_id + "_mode"
            r.set(user_mode, "conn_web")
            await turn_context.send_activity(f"已切換到web搜尋模式")
        elif lcontextai == "switch default":
            #user_mode = from_property_id + "_mode"
            r.set(user_mode, "default")
            await turn_context.send_activity(f"已切換到預設模式")
        elif lcontextai == "it_tools":
            r.set(user_mode, "it_tools")
            await turn_context.send_activity(f"已切換到IT專家模式")
        elif lcontextai == "cdfh_kb":
            r.set(user_mode, "cdfh_kb")
            await turn_context.send_activity(f"已切換到內部知識家模式")

        else:
            #ip = "10.129.12.6"
            #port = 50000

            #r = redis.Redis(host=ip, port=6379, decode_responses=True)
            logging.info("user name = " + user_name)

            ##if msg_dict.conversation_dict != " ":
            ##   logging.info("This is OLD Message:")
            ##   logging.info(msg_dict.conversation_dict)

            from_property_id = turn_context.activity.from_property.id
            logging.info("from_property_id = " + from_property_id)
            ##conversation_id = turn_context.activity.conversation.id
            ##logging.info("conversation_id = " + conversation_id)
            try:
               previous_msg = r.get(from_property_id)
               ai_previous_answer = r.get(from_property_id + "_answer")
            except:
               pass
            
            try:
               this_user_status = r.get(user_mode)
            except:
               pass

            #user_mode verify
            if this_user_status == "conn_web":
               try:
                  my_search = azure_search_web()
                  web_answer = my_search.search_web(turn_context.activity.text)
                  logging.info(web_answer)
               except:
                  pass

            openai.api_type = "azure"
            openai.api_base = "https://openai-cdfh-jpe-dev-ai-01.openai.azure.com/"
            openai.api_version = "2023-03-15-preview"
            openai.api_key = CONFIG.APP_AZURE_OPENAIAPIKEY

            #prompt creating
            if previous_msg and ai_previous_answer:
               if this_user_status == "conn_web":
                  this_message = [{"role": "system", "content": web_answer}, {"role": "user", "content": previous_msg}, {"role": "assistant", "content": ai_previous_answer}, {"role": "user", "content": turn_context.activity.text}]
               else:
                  this_message = [{"role": "user", "content": previous_msg}, {"role": "assistant", "content": ai_previous_answer}, {"role": "user", "content": turn_context.activity.text}]
               prompt = this_message ##"User: " + previous_msg + ", Q: " + turn_context.activity.text
            ##   logging.info(msg_dict.conversation_dict)
            #No previous_msg
            else:
               if this_user_status == "conn_web":
                  prompt = [{"role": "system", "content": web_answer}, {"role": "user", "content": turn_context.activity.text}]
               else:
                  prompt = [{"role": "user", "content": turn_context.activity.text}]

            
            ##log to ELK
            '''
            try:
                msg = {"company":"cdfh-developer", "user_name": user_name, "user_msg": turn_context.activity.text}
                msg = json.dumps(msg)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.connect((ip, port))
                sock.send(msg.encode())
            except:
                pass
            '''

            response = openai.ChatCompletion.create(engine="gpt-35-turbo", messages=prompt, max_tokens=1024, temperature=0.6)

            reply_msg = response['choices'][0]['message']['content']##.replace('\n','')

            ## send to redis
            try:
               r.set(from_property_id, turn_context.activity.text)
               r.set(from_property_id + "_answer", reply_msg)
            except:
               pass

            if this_user_status == "conn_web":
               await turn_context.send_activity("[web mode]" + "\n" + reply_msg)
            else:
               await turn_context.send_activity(reply_msg)

            '''
            #await turn_context.send_activity("Running in Else!!")
            result_dict = self.outgoing_dict(turn_context)
            if result_dict == "Input data is not in Dict":
                await turn_context.send_activity(result_dict)
            else:
                await turn_context.send_activity(lcontext)
                await self._send_unrecognizable_message(turn_context)
            #await turn_context.send_activity(f"Error input,Please check following lists. ")
            #await self._display_index(turn_context)
            '''

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
                    f"您好！我是金控小幫手，一個企業版的生成式AI機器人。小幫手提供了ChatGPT的功能，可以協助您更有效地處理日常業務，提高工作效率。我們的界面非常簡單易用，只需輸入您的問題或要求，小幫手就會立即為您提供答案或解決方案。相信未來能成為您工作的好夥伴，持續為您提供所需的資訊和服務！"
                #    f"請輸入選單選項或數字簡碼1~4"
                )
                #await self._display_index(turn_context)
    #錯誤訊息
    async def _send_unrecognizable_message(self, turn_context: TurnContext):
        await turn_context.send_activity(f"您好！我是金控小幫手．無法識別您的輸入，請重新確認以下指令選單")
        await self._display_index(turn_context)


    #help usage
    def help_usage(self):
        reply = []
        reply_list = []
        ##cdfh_cards_list = []
        ##images_url = "https://cdf-bot-developer.azurewebsites.net/images/01.jpg"
        ##images_url_02 = "https://cdf-bot-developer.azurewebsites.net/images/02.jpg"
        ##images_url_03 = "https://cdf-bot-developer.azurewebsites.net/images/03.jpg"
        ##images_url_04 = "https://cdf-bot-developer.azurewebsites.net/images/04.jpg"
        ##images_url_05 = "https://cdf-bot-developer.azurewebsites.net/images/05.jpg"
        images_list = ["https://cdf-bot-developer.azurewebsites.net/images/01.jpg", "https://cdf-bot-developer.azurewebsites.net/images/02.jpg", "https://cdf-bot-developer.azurewebsites.net/images/03.jpg", "https://cdf-bot-developer.azurewebsites.net/images/04.jpg", "https://cdf-bot-developer.azurewebsites.net/images/05.jpg"]
        
        data_info = self.cards_generate("ai_role")

        ##for help
        ##cdfh_cards_list.append(CardAction(type=ActionTypes.im_back, title="help", value="help"))
        for i in range(0, len(data_info), 1):
            ##cdfh_cards_list.append(data_info[i])
            reply_list.append(CardFactory.hero_card(HeroCard(title= "小幫手角色資訊:", text = "可點擊角色, 將自動切換!", images = [CardImage(url=images_list[i])], buttons = [data_info[i]],)))
            logging.info("ADD reply_list success")
            logging.info(reply_list)
            #buttons = cdfh_cards_list
        

        #, CardImage(url=images_url_02, alt="Image 2"), CardImage(url=images_url_03, alt="Image 3"), CardImage(url=images_url_04, alt="Image 4"), CardImage(url=images_url_05, alt="Image 5")
        ##card = ThumbnailCard(
        ## simple
        '''
        card = HeroCard(
            title= "小幫手角色資訊:",
            text = "可點擊角色, 將自動切換!", images = [CardImage(url=images_list[0], alt="Image 1")],
            #buttons = cdfh_cards_list
            buttons = [CardAction(type=ActionTypes.im_back, title="default", value="switch default")],
        )
        card2 = HeroCard(
            title= "小幫手角色資訊:",
            text = "可點擊角色, 將自動切換!", images = [CardImage(url=images_list[1], alt="Image 2")],
            buttons = [CardAction(type=ActionTypes.im_back, title="內部知識家", value="cdfh_KB")],
        )
        card3 = HeroCard(
            title= "小幫手角色資訊:",
            text = "可點擊角色, 將自動切換!", images = [CardImage(url=images_list[2], alt="Image 3")],
            buttons = [CardAction(type=ActionTypes.im_back, title="IT專家", value="IT_tools")],
        )
        card4 = HeroCard(
            title= "小幫手角色資訊:",
            text = "可點擊角色, 將自動切換!", images = [CardImage(url=images_list[3], alt="Image 4")],
            buttons = [CardAction(type=ActionTypes.im_back, title="網路知識搜尋家", value="conn_web")],
        )
        card5 = HeroCard(
            title= "小幫手角色資訊:",
            text = "可點擊角色, 將自動切換!", images = [CardImage(url=images_list[4], alt="Image 2")],
            buttons = [CardAction(type=ActionTypes.im_back, title="XX知識家", value="XXXXXXX")],
        )
        '''
        
        ##reply = MessageFactory.attachment(CardFactory.hero_card(card))
        reply = MessageFactory.list(reply_list)
        ###reply = MessageFactory.list([CardFactory.hero_card(card), CardFactory.hero_card(card2), CardFactory.hero_card(card3), CardFactory.hero_card(card4)])
        reply.attachment_layout = AttachmentLayoutTypes.carousel
        logging.info(reply)
        return reply

    #azure blob search
    def cards_generate(self, item):
        cards_data = []
        cdfh_get_table = azure_table_search()
        cdfh_get_table.conn_table()
        cards_data_all = cdfh_get_table.get_data_all()
        for i in range(0, len(cards_data_all), 1):
            ##Add 2 data now (functionItem, functionItem_en)
            ##get ai_role data
            if cards_data_all[i]['PartitionKey'] == item:
               if item == "func":
                  cards_data.append(CardAction(type=ActionTypes.im_back, title=cards_data_all[i]['functionItem'], value=cards_data_all[i]['functionItem_en']))
               #cards_data.append(cards_data_all[i]['functionItem'])
               #cards_data.append(cards_data_all[i]['functionItem_en'])
               elif item == "ai_role":
                  cards_data.append(CardAction(type=ActionTypes.im_back, title=cards_data_all[i]['ai_name'], value=cards_data_all[i]['ai_name_en']))

               else:
                  logging.info("No get cards data")
        logging.info("cards_generate")
        logging.info(cards_data)
        return cards_data

    async def _handle_incoming_attachment(self, turn_context: TurnContext):
        """
        Handle attachments uploaded by users. The bot receives an Attachment in an Activity.
        The activity has a List of attachments.
        Not all channels allow users to upload files. Some channels have restrictions
        on file type, size, and other attributes. Consult the documentation for the channel for
        more information. For example Skype's limits are here
        <see ref="https://support.skype.com/en/faq/FA34644/skype-file-sharing-file-types-size-and-time-limits"/>.
        :param turn_context:
        :return:
        """
        for attachment in turn_context.activity.attachments:
            attachment_info = await self._download_attachment_and_write(attachment)
            if "filename" in attachment_info:
                await turn_context.send_activity(
                    f"Attachment {attachment_info['filename']} has been received to {attachment_info['local_path']}"
                )

    async def _download_attachment_and_write(self, attachment: Attachment) -> dict:
        """
        Retrieve the attachment via the attachment's contentUrl.
        :param attachment:
        :return: Dict: keys "filename", "local_path"
        """
        try:
            response = urllib.request.urlopen(attachment.content_url)
            headers = response.info()

            # If user uploads JSON file, this prevents it from being written as
            # "{"type":"Buffer","data":[123,13,10,32,32,34,108..."
            if headers["content-type"] == "application/json":
                data = bytes(json.load(response)["data"])
            else:
                data = response.read()

            local_filename = os.path.join(os.getcwd(), attachment.name)
            with open(local_filename, "wb") as out_file:
                out_file.write(data)

            return {"filename": attachment.name, "local_path": local_filename}
        except Exception as exception:
            print(exception)
            return {}


    async def _handle_outgoing_attachment(self, turn_context: TurnContext, pic_name):
        reply = Activity(type=ActivityTypes.message)
        my_char = turn_context.activity.text.lower()
        if "get" in my_char and pic_name != " ":
           reply.text = "Report !!"
           reply.attachments = [self._get_inline_attachment(pic_name)]

           await turn_context.send_activity(reply)

        elif "cost" in my_char and pic_name != " ":
           reply.text = "Report !!"
           reply.attachments = [self._get_inline_attachment(pic_name)]

           await turn_context.send_activity(reply)


    def outgoing_dict(self, input_data):
        this_data = input_data.lower()
        try:
           reply_msg = bot_dict.options_dict[this_data]

        except:
           reply_msg = "Input data is not in Dict"

        return reply_msg


    async def _display_card(self, turn_context: TurnContext):
        card1 = HeroCard(
            text="這是help選單，請輸入help或按下按鈕查看功能表：",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="help", value="help"
                ),
            ],
        )
        card2 = HeroCard(
            text="這是總選單，請按下選單按鈕執行：",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="DevOps選單", value="devops"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="CT小組選單", value="cthelp"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Report選單", value="report"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="ChatGPT使用說明", value="ai"
                ),
            ],
        )
        card3 = HeroCard(
            text="這是ChatOps功能選單，請按下選單按鈕執行動作：",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="List:列出Project資訊.", value="list"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Execute:測試執行Project Pipeline.", value="execute"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Check:確認Project Pipeline狀態.", value="check"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Get:確認Azure Repo資訊.", value="get"
                ),
            ],
        )
        card4 = HeroCard(
            text="這是週報月報投影片選單，請按下選單按鈕產生Report連結：",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="IT monthly", value="itmonthly"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="CIO monthly", value="ciomonthly"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Project bi-weekly", value="projectbiweekly"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Tank weekly", value="tankweekly"
                ),
            ],
        )
        card5 = HeroCard(
            text="這是CT小組的選單，請按下選單按鈕產生Report連結：",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="CT report", value="ctreport"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Azure DevOps連結", value="adolink"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Azure Portal連結", value="azlink"
                ),
            ],
        )
        card = bot_dict.options_dict[turn_context]
        reply = MessageFactory.attachment(CardFactory.hero_card(card))
        await turn_context.send_activity(reply)

    async def _display_help(self, turn_context: TurnContext):
        card2 = HeroCard(
            text="這是help選單，請輸入help或按下按鈕查看功能表：",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="help", value="index"
                ),
            ],
        )
        reply = MessageFactory.attachment(CardFactory.hero_card(card2))
        await turn_context.send_activity(reply)

    # 顯示選單index
    async def _display_index(self, turn_context: TurnContext):
        card2 = HeroCard(
            text="這是功能表選單，請按下選單按鈕執行：",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="DevOps選單", value="devops"
                ),
                #CardAction(
                #    type=ActionTypes.im_back, title="CT小組選單", value="cthelp"
                #),
                CardAction(
                    type=ActionTypes.im_back, title="週報月報選單", value="report"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="金控常用網站", value="cdfhweb"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="ChatGPT使用說明", value="ai"
                ),
            ],
        )
        reply = MessageFactory.attachment(CardFactory.hero_card(card2))
        await turn_context.send_activity(reply)

    async def _display_cdfh(self, turn_context: TurnContext):
        card2 = HeroCard(
            text="這是金控常用網站選單，請按下選單按鈕執行：",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="金控入口網站", value="cdfh"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="電子簽核系統", value="bpm"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="二代採購系統", value="epb"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="員工服務平台", value="ehrweb"
                ),
#                CardAction(
#                    type=ActionTypes.im_back, title="金控規章", value="regulations"
#                ),
                CardAction(
                    type=ActionTypes.im_back, title="回到功能表", value="index"
                ),
            ],
        )
        reply = MessageFactory.attachment(CardFactory.hero_card(card2))
        await turn_context.send_activity(reply)

    # 顯示選單devops
    async def _display_devops(self, turn_context: TurnContext):
        card = HeroCard(
            text="這是ChatOps功能選單，請按下選單按鈕執行動作：",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="List:列出Project資訊.", value="card_list"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Execute:測試執行Project Pipeline.", value="card_execute"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Check:確認Project Pipeline狀態.", value="card_check"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Get:確認Azure Repo資訊.", value="card_get"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="回到功能表", value="index"
                ),
            ],
        )

        reply = MessageFactory.attachment(CardFactory.hero_card(card))
        await turn_context.send_activity(reply)

    # 顯示選單report
    async def _display_report(self, turn_context: TurnContext):
        card2 = HeroCard(
            text="這是週報月報投影片選單，請按下選單按鈕產生Report連結：",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="IT monthly", value="itmonthly"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="CIO monthly", value="ciomonthly"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Project bi-weekly", value="projectbiweekly"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Tank weekly", value="tankweekly"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="回到功能表", value="index"
                ),
            ],
        )

        reply = MessageFactory.attachment(CardFactory.hero_card(card2))
        await turn_context.send_activity(reply)

    # 顯示選單ct
    async def _display_ct(self, turn_context: TurnContext):
        card2 = HeroCard(
            text="這是CT小組的選單，請按下選單按鈕產生Report連結：",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="CT report", value="ctreport"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Azure DevOps連結", value="adolink"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="Azure Portal連結", value="azlink"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="回到功能表", value="index"
                ),
            ],
        )

        reply = MessageFactory.attachment(CardFactory.hero_card(card2))
        await turn_context.send_activity(reply)

    def _get_inline_attachment(self, pic_name) -> Attachment:
        """
        Creates an inline attachment sent from the bot to the user using a base64 string.
        Using a base64 string to send an attachment will not work on all channels.
        Additionally, some channels will only allow certain file types to be sent this way.
        For example a .png file may work but a .pdf file may not on some channels.
        Please consult the channel documentation for specifics.
        :return: Attachment
        """
        file_path = os.path.join(os.getcwd(), "static/images/01.png")
        ##r = redis.Redis(host='redis-10444.c285.us-west-2-2.ec2.cloud.redislabs.com', port=10444, password="tuHa8FQI8p5wMVYRFOyi7XuvbiQKmItj" , decode_responses=True)

        ##with open(file_path, "rb") as in_file:
        ##    base64_image = base64.b64encode(in_file.read()).decode()
        my_image = file_path#r.get(pic_name)
        my_data = base64.b64decode(my_image)
        ##with open(pic_name + ".png", "wb") as f:
        with open(pic_name + ".jpg", "wb") as f:
             f.write(my_data)

        file_path = os.path.join(os.getcwd(), pic_name +".jpg")
        with open(file_path, "rb") as in_file:
             base64_image = base64.b64encode(in_file.read()).decode()

        return Attachment(
            name=pic_name + ".jpg",
            content_type="image/jpg",
            content_url=f"data:image/jpg;base64,{base64_image}",
        )




    async def _get_upload_attachment(self, turn_context: TurnContext) -> Attachment:
        """
        Creates an "Attachment" to be sent from the bot to the user from an uploaded file.
        :param turn_context:
        :return: Attachment
        """
        with open(
            os.path.join(os.getcwd(), "resources/architecture-resize.png"), "rb"
        ) as in_file:
            image_data = in_file.read()

        connector = await turn_context.adapter.create_connector_client(
            turn_context.activity.service_url
        )
        conversation_id = turn_context.activity.conversation.id
        response = await connector.conversations.upload_attachment(
            conversation_id,
            AttachmentData(
                name="architecture-resize.png",
                original_base64=image_data,
                type="image/png",
            ),
        )

        base_uri: str = connector.config.base_url
        attachment_uri = (
            base_uri
            + ("" if base_uri.endswith("/") else "/")
            + f"v3/attachments/{response.id}/views/original"
        )

        return Attachment(
            name="architecture-resize.png",
            content_type="image/png",
            content_url=attachment_uri,
        )

    def _get_internet_attachment(self) -> Attachment:
        """
        Creates an Attachment to be sent from the bot to the user from a HTTP URL.
        :return: Attachment
        """
        return Attachment(
            name="architecture-resize.png",
            content_type="image/png",
            content_url="https://docs.microsoft.com/en-us/bot-framework/media/how-it-works/architecture-resize.png",
        )

    def _post_trigger_ADOpipeline2(self):
        personal_access_token = '2oyp3xxei2kljmbuboemp562onmwxk3kseazelqmxahph4erqomq'
        organization = 'cdfh-app'
        project = 'Cloud Technology'
        pipeline = 'Pipeline-runscripts'
        org_url = 'https://dev.azure.com/' + organization + "/"
        project_url = org_url + project + "/"

        pipelineID = '1'
        pipelineLastversion = '4'
        # pipelinename = input("Enter name:")
        pipelinename = 'Pipeline-runscripts'

        # get pipeline lists form all projects
        getpllistURL = project_url + '_apis/pipelines?orderBy={orderBy}&$top={$top}&continuationToken={continuationToken}&api-version=6.0-preview.1'
        print('getpllistURL= ', getpllistURL)
        rplist = requests.get(getpllistURL, auth=('user', personal_access_token))
        print(rplist)
        rplist_json = json.loads(rplist.text)
        print(rplist_json)
        # check the lists to find the same pipeline name with input/resouce piprline name
        i = '0'
        cn = 'value.' + i
        a = int(i)
        while pipelinename != Property.get(rplist_json, cn + '.name'):
            cn = 'value.' + i
            print("cn=", cn)
            a = a + 1
            i = str(a)

        pipelineID = Property.get(rplist_json, 'value.0.id')
        pipelineLastversion = Property.get(rplist_json, 'value.0.revision')

        # check last version pipeline info include id,revision,name
        id = Property.get(rplist_json, cn + '.id')
        rev = Property.get(rplist_json, cn + '.revision')
        name = Property.get(rplist_json, cn + '.name')
        print('id=', id)
        print('rev=', rev)
        print('name=', name)

        # get pipeline info to gen URL, the plinfoURL is same as runPLURL
        plinfoURL = project_url + '_apis/pipelines/' + str(id) + '/runs?pipelineVersion=' + str(
            rev) + '&api-version=6.0-preview.1'
        print('plinfoURL=', plinfoURL)
        getresult = requests.get(plinfoURL, auth=('user', personal_access_token))
        print(getresult.text)

        # return getresult.text

        my_header = {"Content-Type": "application/json"}
        my_body = {
            "requestBody": {
                "QDateTime": "2020-11-27 15:57:41",
                "CCY": "CHF"
            },
            "header": {
                "txnTime": "2020-11-27 16:43:25",
                "senderCode": "KyleComputer"
            }
        }
        my_data = json.dumps(my_body)

        # run POST by runPLURL
        runPLURL = project_url + '_apis/pipelines/' + str(id) + '/runs?pipelineVersion=' + str(
            rev) + '&api-version=6.0-preview.1'
        print("runPLURL: ", runPLURL)
        trigger = requests.post(runPLURL, auth=('user', personal_access_token), headers=my_header, data=my_data)
        print(trigger.text)
        result = json.loads(trigger.text)
        return result


#unit test
    #if __name__ == '__main__':
        #azure_test_plan = _post_trigger_ADOpipeline2('PL-testPowershell')
        #azure_test_plan = on_message_activity(0,'hello')
