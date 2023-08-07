import os, sys
import json
import string
import requests
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import re
import openai
import urllib.parse
import urllib.request


class azure_search_web():
      def __init__(self):
          self.search_endpoint = "https://api.bing.microsoft.com/v7.0/search"
          self.subscription_key = "c1712b1c42d445cc884df84635742cdc"
          self.credentials = AzureKeyCredential(self.subscription_key)
          self.headers = {'Ocp-Apim-Subscription-Key': self.subscription_key}

      def search_web(self, query):
          tmp_info = ""
          params = {'q': query, 'count': 10}
          response = requests.get(self.search_endpoint, headers=self.headers, params=params)
          response.raise_for_status()

          data = response.json()

          if 'webPages' in data and 'value' in data['webPages']:
             results = data['webPages']['value']
           #return results


          # 調用函數搜尋
          ##results = search_web(query)
          # 處理結果
          if results:
             for i, result in enumerate(results, start=1):
                 tmp_info += result["snippet"] + ","
                 #print (result["snippet"])
             tmp_info = tmp_info[:-1]
             print (tmp_info)
             return tmp_info 

if __name__ == '__main__':
   my_search = azure_search_web()
   my_search.search_web("誰是中華開發金控董事長")
