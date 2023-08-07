#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 8000
    APP_ID = os.environ.get("MicrosoftAppId", "f2c76008-7ba7-4004-91ca-c4ead18fa405")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "dH88Q~3i3tNqAulnI.wyhyRaA-iZyM1nQrwspdtK")
    APP_OPENAIAPIKEY= os.environ.get("OpenAIAPIkey","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")
    APP_AZURE_OPENAIAPIKEY= os.environ.get("OPENAI_API_KEY","9e833eb0535441a4906f43f1d8d09b89")
