from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import dotenv_values
from .logger import setup_logger
from .exceptions import handle_exception
from fastapi.encoders import jsonable_encoder

config = dotenv_values(".env")
logger = setup_logger()

class MongoDB():
    def __init__(self):
        pass


    async def __aenter__(self):
        # mongo_url = str("mongodb://localhost:27017")
        mongo_url = config["mongo_db_url"]
        database_name = str(config["mongo_database"])
        collection_name = str(config["mongo_collection"])
        
        self.client = AsyncIOMotorClient(mongo_url, ssl=True) # ssl=True for production and false for development
        logger.info("MongoDB Client Initialised")
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        
        return self


    async def add_user(self, user) -> bool:
        try:
            sec_code_query = {"securityCode": user.securityCode}
            
            if not await self.collection.find_one(sec_code_query):
                raise Exception("Invalid security code")
            
            exist_user_query = {"email": user.email}
            if await self.collection.find_one(exist_user_query):
                raise Exception("User already exists")
            
            del user.securityCode
            if await self.collection.insert_one(jsonable_encoder(user)):
                logger.info(f"User {user.name} added to database")
        
        except Exception as e:
            handle_exception(e)
        
        return True


    async def login_check(self, user_cred) -> bool:
        query = {"email": user_cred.email, "password": user_cred.password}
        try:
            query_result = await self.collection.find_one(query)
            
            if not query_result:
                raise Exception("Invalid email or password")
            
            logger.info(f"{user_cred.email} Logged in successfully")
    
        except Exception as e:
            handle_exception(e)
        
        return True


    async def reset_password(self, reset_user_cred) -> bool:
        sec_code_query = {"securityCode": reset_user_cred.securityCode}
        email_check_query = {"email": reset_user_cred.email}
        new_password = {"$set": {"password": reset_user_cred.newPassword}}
        
        try:
            if not await self.collection.find_one(sec_code_query):
                raise Exception("Invalid security code or email")
            
            if not await self.collection.find_one(email_check_query):
                raise Exception("Invalid email or security code")
            
            if await self.collection.update_one(email_check_query, new_password):
                logger.info(f"Password resetted for {reset_user_cred.email}")
        
        except Exception as e:
            handle_exception(e)
    
        return True

    async def __aexit__(self, exc_type, exc, tb):
        self.client.close()











    # def insert_document(self, document):
    #     self.collection.insert_one(document)
        
    # def get_documents(self):
    #     return list(self.collection.find())
    
    
    # # export_and_delete_production_data
    # def production_databackup(self, csv_filename):
    #     try:
    #         # Fetch the data from MongoDB
    #         production_data = list(self.collection.find())
            
    #         # Export the data to a CSV file using Pandas
    #         df = pd.DataFrame(production_data)
    #         df.to_csv(csv_filename, mode='a',index=False)
            
    #         # Delete the data from the MongoDB collection
    #         self.collection.delete_many({})   
    #         logger.info(f"Production data exported to {csv_filename} and deleted from MongoDB.")
            
    #     except Exception as e:
    #         logger.error(f"Error exporting and deleting production data: {e}")