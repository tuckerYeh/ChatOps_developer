#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 8008

    APP_ID = os.environ.get("MicrosoftAppId", "1a589cb1-1dbe-4f42-9c92-68c1c7e51b74")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "Ofe8Q~1NfmXsBgaE7i~DF~dy-.a2d0qfHcvwta1u")

    #APP_OPENAIAPIKEY= os.environ.get("OpenAIAPIkey","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")
    APP_AZURE_OPENAIAPIBASE= os.environ.get("OPENAI_API_BASE","https://kgis-openai.openai.azure.com/")
    APP_AZURE_OPENAIAPIKEY= os.environ.get("OPENAI_API_KEY","4742123a7df64e46ba77bbe98e784ac1")

    #APP_AZURE_OPENAIAPIBASE= os.environ.get("OPENAI_API_BASE","https://tucker-ai.openai.azure.com/")
    #APP_AZURE_OPENAIAPIKEY= os.environ.get("OPENAI_API_KEY","498e27ca0d0742b4b65f952e67714870")

#https://tucker-ai-web-app-1.azurewebsites.net/api/messages