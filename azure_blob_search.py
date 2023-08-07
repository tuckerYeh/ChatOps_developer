import os, sys
from azure.data.tables import * #TableServiceClient
from azure.core.exceptions import ResourceNotFoundError


class azure_table_search():

  def __init__(self):
      self.connection_string = "DefaultEndpointsProtocol=https;AccountName=cdfhbotdata;AccountKey=ljmTsLZP4snnw2LypeiVBG3/IvP+nHFuhJYBa49+GOoGpcp4C7VrzoXVJRHAxNRTH2lrCYmuF3ZY+AStT/sOAg==;EndpointSuffix=core.windows.net"

      self.table_name = "botAiData"


  def conn_table(self):
      # 建立 TableService 並使用連接字串進行身分驗證
      self.table_service_client = TableServiceClient.from_connection_string(conn_str=self.connection_string)

      # 設定要查詢的 PartitionKey 和 RowKey
      ##partition_key = "func"
      ##row_key = "1"

      # 從資料表中取得指定實體
      self.table_client = self.table_service_client.get_table_client(table_name=self.table_name)


  def get_data_once(self, partition_key, row_key):
      entity = self.table_client.get_entity(partition_key=partition_key, row_key=row_key)

      # return實體的內容
      print (entity)
      return entity

  def get_data_all(self):
      entity_list = []
      entity = self.table_client.query_entities(query_filter="")
      for entity_data in entity:
          entity_list.append(entity_data)
      print(entity_list)

      # return實體的內容
      return entity_list