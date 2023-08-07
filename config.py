#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 8000
    APP_ID = os.environ.get("MicrosoftAppId", "90372b8c-c4b3-435f-80e9-270a48fc12da")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "b0o8Q~Zyv5tC_BamL~VUXQqMmFNF9~BtSEtxNbtR")
    #APP_OPENAIAPIKEY= os.environ.get("OpenAIAPIkey","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")
    APP_AZURE_OPENAIAPIKEY= os.environ.get("OPENAI_API_KEY","ea75d3fa0090468bb1c00ae896e8c846")
