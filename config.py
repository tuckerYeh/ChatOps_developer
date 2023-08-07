#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 8000
    APP_ID = os.environ.get("MicrosoftAppId", "904e00ce-de5b-4d2c-9da9-523eed882806")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "5b73980e-9ec8-474d-b481-5190e63c1c34")
    #APP_OPENAIAPIKEY= os.environ.get("OpenAIAPIkey","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")
    APP_AZURE_OPENAIAPIKEY= os.environ.get("OPENAI_API_KEY","ad54cec485524fa590fd5ba8428505f0")
