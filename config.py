#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 2345
    #APP_ID = os.environ.get("MicrosoftAppId", "904e00ce-de5b-4d2c-9da9-523eed882806")
    #APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "9Lg8Q~Y72jnI6tIAIk3xlEdq73DYbQEb7dEJBc-q")
    #APP_OPENAIAPIKEY= os.environ.get("OpenAIAPIkey","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")
    APP_AZURE_OPENAIAPIKEY= os.environ.get("OPENAI_API_KEY","498e27ca0d0742b4b65f952e67714870")
    APP_ID = os.environ.get("MicrosoftAppId", "1a589cb1-1dbe-4f42-9c92-68c1c7e51b74")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "Ofe8Q~1NfmXsBgaE7i~DF~dy-.a2d0qfHcvwta1u")
