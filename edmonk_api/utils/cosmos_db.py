from dotenv import dotenv_values
from azure.cosmos.aio import CosmosClient
from azure.cosmos import PartitionKey, exceptions
from .logger import setup_logger

config = dotenv_values(".env")
logger = setup_logger()

class CosmoDB:
    def __init__(self, config):
        self.config = config

    async def __aenter__(self):
        self.cosmos_client = CosmosClient(url=str(self.config["URL"]), credential=str(self.config["KEY"]))
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.cosmos_client.close()
    
    async def get_or_create_db(self, db_name):
        try:
            database = await self.cosmos_client.create_database_if_not_exists(db_name)
            await database.read()
            return database

        except exceptions.CosmosResourceNotFoundError:
            logger.info("Creating database")
            return await self.cosmos_client.create_database(db_name)

    async def get_or_create_container(self, db_name, container_name, path):
        database = await self.get_or_create_db(db_name)
        try:
            partition_key_path = PartitionKey(path)
            container = await database.create_container_if_not_exists(
                id=container_name,
                partition_key=partition_key_path,
            )
            logger.info("Container created or returned")
            return container

        except exceptions.CosmosHttpResponseError:
            raise
