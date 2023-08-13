#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 8004

    APP_ID = os.environ.get("MicrosoftAppId", "1a589cb1-1dbe-4f42-9c92-68c1c7e51b74")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "Ofe8Q~1NfmXsBgaE7i~DF~dy-.a2d0qfHcvwta1u")

    #APP_OPENAIAPIKEY= os.environ.get("OpenAIAPIkey","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")
    APP_AZURE_OPENAIAPIKEY= os.environ.get("OPENAI_API_KEY","498e27ca0d0742b4b65f952e67714870") #GPT3.5 
    #APP_AZURE_OPENAIAPIKEY= os.environ.get("OPENAI_API_KEY","ce7ef7b4a5974e34bfb8c2594bd03125") #GPT4


