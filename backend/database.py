"""This module handles the database connection with Azure."""

import os

import pandas as pd
import streamlit as st
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from utils import DATABASECOLUMNS

load_dotenv()


class Database:
    """
    This class serves as a database instead of using CSVs/Excels.

    It connects to Azure and manages the data in the table.
    """

    def __init__(self) -> None:
        """Constructor for the Database class."""
        self.tableName = "app_data"
        self.insertionMethod = "append"
        self.kvName = os.getenv("KVNAME")
        self.dbName = os.getenv("DBNAME")

    def getKeyVaultSecret(self, secretName: str):
        """This function gets the necassary secret, required to establish the connection."""
        kvUri = f"https://{self.kvName}.vault.azure.net"

        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=kvUri, credential=credential)

        return client.get_secret(secretName).value

    def createDatabaseConnection(self):
        """This function establishes the connection to Azure Database."""
        connectionUrl = URL.create(
            "mssql+pyodbc", query={"odbc_connect": self.getKeyVaultSecret(self.dbName)}
        )

        return create_engine(connectionUrl)

    def addRowToTable(self, row):
        """This function adds the `row` to the table in DB."""
        return pd.DataFrame(data=[row], columns=DATABASECOLUMNS).to_sql(
            name=self.tableName,
            con=self.createDatabaseConnection(),
            if_exists=self.insertionMethod,
            index=False,
        )

    # pylint: disable=no-self-argument
    @st.cache_data
    def getTableAsDataFrame(_self):
        """This function reads the table into a dataframe and returns it."""
        return pd.read_sql(
            f"Select * from {_self.tableName}", con=_self.createDatabaseConnection()
        )
