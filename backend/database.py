"""This module handles the database connection with Azure."""

import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from utils import DATABASECOLUMNS
from dotenv import load_dotenv

load_dotenv()

class database():

    def __init__(self) -> None:
        self.tableName = 'app_data'
        self.insertionMethod = 'append'
        self.KVName = os.getenv('KVName')
        self.DBName = os.getenv('DBName')
        # self.dataRead = False
        pass

    def getKeyVaultSecret(self, secretName: str):
        # keyVaultName = "levels-password"
        KVUri = f"https://{self.KVName}.vault.azure.net"

        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=KVUri, credential=credential)


        return client.get_secret(secretName).value    # "levels-db-connection"

    def createDatabaseConnection(self):
        connection_url = URL.create(
            "mssql+pyodbc", 
            query={"odbc_connect": self.getKeyVaultSecret(self.DBName)}
        )

        return create_engine(connection_url)
    
    def addRowToTable(self, Row):
        return pd.DataFrame(
            data = [Row],
            columns = DATABASECOLUMNS
        ).to_sql(
            name = self.tableName,
            con = self.createDatabaseConnection(),
            if_exists = self.insertionMethod,
            index=False
            )
    @st.cache_data
    def getTableAsDataFrame(_self):
        return pd.read_sql(
            f"Select * from {_self.tableName}",
            con=_self.createDatabaseConnection()
            )

