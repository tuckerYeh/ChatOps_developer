#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 8008

    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", " ")
    APP_AZURE_OPENAIAPIBASE= os.environ.get("OPENAI_API_BASE"," ")
    APP_AZURE_OPENAIAPIKEY= os.environ.get("OPENAI_API_KEY","4 ")
