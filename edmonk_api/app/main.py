# FastAPI modules
from fastapi import FastAPI
from fastapi import status
from fastapi.encoders import jsonable_encoder

# User defined modules
from utils.models import WebinarSchema
from utils.exceptions import handle_exception
from utils.logger import setup_logger

#CosmosDB connection client
from utils.cosmos_db import CosmoDB

# Python modules
from dotenv import dotenv_values
import datetime
import uvicorn

config = dotenv_values(".env")
logger = setup_logger()

DATABASE_NAME = config["DATABASE_DEV"]
CONTAINER_NAME = 'webinar'

app=FastAPI(debug=True,
            title="Webinar API")
logger.info("App started")

@app.get("/webinar/get_all_webinars/")
async def get_all_webinars():
    logger.info("get_webinar api called")
    try:
        async with CosmoDB(config) as cosmo_db:
            webinar_container = await cosmo_db.get_or_create_container(DATABASE_NAME, CONTAINER_NAME, "/Tag")
            all_webinars = [webinar async for webinar in webinar_container.read_all_items()]
            response = {
                "status_msg": True,
                "status_code": status.HTTP_200_OK,
                "message": "Success",
            }
            return {"response": response, "all webinars": all_webinars}
    
    except Exception as e:
        return handle_exception(e)

@app.post("/webinar/create_webinar/")
async def create_webinar(webinar: WebinarSchema):
    logger.info("create_webinar api called")
    try:
        webinar_data_items = jsonable_encoder(webinar)
        webinar_data_items["id"] = datetime.datetime.now().isoformat()
        async with CosmoDB(config) as cosmo_db:
            webinar_container = await cosmo_db.get_or_create_container(DATABASE_NAME, CONTAINER_NAME, "/Tag")
            webinar_data_insert = await webinar_container.create_item(webinar_data_items)

            logger.info(f"Successfully inserted {webinar_data_items}")
            response = {
                "status_msg": True,
                "status_code": status.HTTP_200_OK,
                "message": "Success",
            }
            return {"response": response, "webinar_data": webinar_data_insert}

    except Exception as e:
        return handle_exception(e)


@app.put("/webinar/update_webinar/{webinar_title}")
async def update_webinar(webinar_title: str, new_data: WebinarSchema):
    logger.info("update_webinar api called")
    try:
        async with CosmoDB(config) as cosmo_db:
            webinar_container = await cosmo_db.get_or_create_container(DATABASE_NAME, CONTAINER_NAME, "/Tag")
            queried_webinars = webinar_container.query_items(
                query="SELECT * FROM c WHERE c.title = @webinar_title",
                parameters=[{"name": "@webinar_title", "value": webinar_title}]
            )
            existing_item = [item async for item in queried_webinars][0]
            update_items_encoded = jsonable_encoder(new_data)
            update_items_encoded["id"] = existing_item["id"]
            update_items_encoded["last_modified"] = datetime.datetime.now().isoformat()
            updated_item = await webinar_container.replace_item(existing_item, update_items_encoded)
            
            response = {
                "status_msg": True,
                "status_code": status.HTTP_200_OK,
                "message": "Success",
            }
            
            return {"response": response, "updated_item": updated_item}
    
    except Exception as e:
        return handle_exception(e)

@app.delete("/webinar/delete_webinar/{webinar_title}")
async def delete_webinar(webinar_title: str):
    logger.info("delete_webinar api called")
    try:
        async with CosmoDB(config) as cosmo_db:
            webinar_container = await cosmo_db.get_or_create_container(DATABASE_NAME, CONTAINER_NAME, "/Tag")
            queried_webinars = webinar_container.query_items(
                query="SELECT * FROM c WHERE c.title = @webinar_title",
                parameters=[{"name": "@webinar_title", "value": webinar_title}]
            )
            queried_webinar = [item async for item in queried_webinars][0]
            await webinar_container.delete_item(queried_webinar, partition_key=queried_webinar["Tag"])
            logger.info(f"deleted item: {webinar_title}")

            response = {
                "status_msg": True,
                "status_code": status.HTTP_200_OK,
                "message": f"Successfully deleted item: {webinar_title}",
            }

            return {"response": response, "deleted_webinar": queried_webinar}

    except Exception as e:
        return handle_exception(e)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)