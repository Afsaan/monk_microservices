from fastapi import FastAPI
from fastapi import HTTPException,status
from fastapi.encoders import jsonable_encoder

# User defined modules
from utils.models import BlogSchema, BlogUpdateSchema
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
CONTAINER_NAME = 'blog'

app=FastAPI(debug=True,
            title="Blog API")
logger.info("Blog API App started")


@app.get("/blog/get-all-blogs/")
async def get_all_blogs():
    logger.info("get_all_blogs api called")
    try:
        async with CosmoDB(config) as cosmo_db:
            blog_container = await cosmo_db.get_or_create_container(DATABASE_NAME, CONTAINER_NAME, "/Tag")
            all_blogs = [blog async for blog in blog_container.read_all_items() if blog["is_deleted"] == False]
            
            response = {
                "status_msg": True,
                "status_code": status.HTTP_200_OK,
                "message": "Success",
            }
            return {"response": response, "all_blogs": all_blogs}
    
    except Exception as e:
        return handle_exception(e)


@app.get("/blog/get-blog/{title}")
async def get_blog(title : str):
    logger.info("get_blog api called")
    try:
        async with CosmoDB(config) as cosmo_db:
            blog_container = await cosmo_db.get_or_create_container(DATABASE_NAME, CONTAINER_NAME, "/Tag")
            all_blogs = [blog async for blog in blog_container.read_all_items() if blog["is_deleted"] == False]
            if title:
                filtered_blogs = [blog for blog in all_blogs if blog["blog_title"] == title]
                if filtered_blogs:
                    logger.info(f"Retrieved item: {filtered_blogs}")
                    return {"response": status.HTTP_200_OK ,"filtered_blogs": filtered_blogs}
                
                else:
                    raise HTTPException(status_code=404, detail="Blog not found")
            else:
                # If no title provided, return all blogs
                response = {
                    "status_msg": True,
                    "status_code": status.HTTP_200_OK,
                    "message": "Success",
                    "all_blogs": all_blogs
                }
                return response
    
    except Exception as e:
        return handle_exception(e)


@app.post("/blog/create-blog/")
async def create_blog(blog: BlogSchema):
    logger.info("create_blog api called")
    try:
        blog_data_items = jsonable_encoder(blog)
        blog_data_items["id"] = datetime.datetime.now().isoformat()
        blog_data_items["is_deleted"] = False
        async with CosmoDB(config) as cosmo_db:
            blog_container = await cosmo_db.get_or_create_container(DATABASE_NAME, CONTAINER_NAME, "/Tag")
            
            # query to check for duplicate title
            queried_blogs = blog_container.query_items(
                query="SELECT * FROM c WHERE c.blog_title = @title",
                parameters=[{"name": "@title", "value": blog.blog_title}]
            )
            queried_blog = [item async for item in queried_blogs] if queried_blogs else None
            
            if queried_blog:
                print("Duplicate title detected:", blog.blog_title)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog with this title already exists")

            blogdata_insert = await blog_container.create_item(blog_data_items)

            logger.info(f"Successfully inserted {blog_data_items}")
            response = {
                "status_msg": True,
                "status_code": status.HTTP_200_OK,
                "message": "Success",
            }
            return {"response": response, "created_blog": blog_data_items}
    # # Data for backup in CSV
    #     with open('Data_backup/userregistration_production1.csv', mode='a', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow([blog_data_items['Blog'], blog_data_items['Tag'], blog_data_items['Title'], blog_data_items['id']])
    #         logger.info("Successfully processed registration data")  
    
    except Exception as e:
        return handle_exception(e)


@app.put("/blog/update-blog")
async def update_blog(new_data: BlogUpdateSchema):
    try:
        async with CosmoDB(config) as cosmo_db:
            blog_container = await cosmo_db.get_or_create_container(DATABASE_NAME, CONTAINER_NAME, "/Tag")
            queried_blogs = blog_container.query_items(
                query="SELECT * FROM c WHERE c.blog_title = @old_blog_title",
                parameters=[{"name": "@old_blog_title", "value": new_data.old_blog_title}]
            )
            queried_blog = [item async for item in queried_blogs][0]
            del new_data.old_blog_title
            update_items_encoded = jsonable_encoder(new_data)
            update_items_encoded["id"] = queried_blog["id"]
            update_items_encoded["last_modified"] = datetime.datetime.now().isoformat()
            update_items_encoded["is_deleted"] = False
            # update_items_encoded["Title"] = new_data.Title.lower()
            
            updated_item = await blog_container.replace_item(queried_blog, update_items_encoded)
            
            response = {
                "status_msg": True,
                "status_code": status.HTTP_200_OK,
                "message": "Success",
            }
            
            # Return both response and updated item
            return {"response": response, "updated_blog": updated_item}
    
    except Exception as e:
        return handle_exception(e)


@app.delete("/blog/delete-blog")
async def delete_blog(blog_title: str):
    logger.info("delete_blog api called")
    try:
        async with CosmoDB(config) as cosmo_db:
            blog_container = await cosmo_db.get_or_create_container(DATABASE_NAME, CONTAINER_NAME, "/Tag")
            queried_blogs = blog_container.query_items(
                query="SELECT * FROM c WHERE c.blog_title = @title",
                parameters=[{"name": "@title", "value": blog_title}]
            )
            queried_blog = [item async for item in queried_blogs][0]
            deleted_item = {key: value for key, value in queried_blog.items()}
            deleted_item["is_deleted"] = True
            deleted_blog = await blog_container.replace_item(queried_blog, deleted_item)
            logger.info(f"deleted item: {blog_title}")

            # Create success response
            response = {
                "status_msg": True,
                "status_code": status.HTTP_200_OK,
                "message": f"Successfully deleted item: {blog_title}",
            }

            # Return success response
            return {"response": response, "deleted_blog": deleted_blog}

    except Exception as e:
        return handle_exception(e)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)