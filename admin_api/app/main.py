from fastapi import FastAPI
from fastapi import status

# User defined modules
from utils.models import Login, AddUser, ResetPassword
from utils.exceptions import handle_exception
from utils.logger import setup_logger

#MongoDB connection client
from utils.database_dev import MongoDB

# Python modules
import uvicorn

logger = setup_logger()

app=FastAPI(debug=True,
            title="Admin API")
logger.info("Admin API App started")

@app.post("/admin/add-user")
async def add_user(user: AddUser):
    logger.info("add_user endpoint of admin api called")
    
    try:
        async with MongoDB() as mongo_db_client:
            if await mongo_db_client.add_user(user):
                return {"status": status.HTTP_201_CREATED, "response": f"User {user.email} added successfully"}
            
            return {"status": status.HTTP_400_BAD_REQUEST, "response": "Invalid security code or user already exists"}
    
    except Exception as e:
        return handle_exception(e)

@app.post("/admin/login")
async def login(login_cred: Login):
    logger.info("login endpoint of admin api called")
    
    try:
        async with MongoDB() as mongo_db_client:
            if await mongo_db_client.login_check(login_cred):
                return {"status": status.HTTP_200_OK, "response": f"{login_cred.email} Logged in successfully"}

            return {"status": status.HTTP_400_BAD_REQUEST, "response": "Invalid email or password"}
    
    except Exception as e:
        return handle_exception(e)

@app.put("/admin/reset-password")
async def reset_password(user_cred: ResetPassword):
    logger.info("reset_password endpoint of admin api called")
    
    try:
        async with MongoDB() as mongo_db_client:
            if await mongo_db_client.reset_password(user_cred):
                return {"status": status.HTTP_200_OK, "response": f"Password resetted for {user_cred.email}"}
            
            return {"status": status.HTTP_400_BAD_REQUEST, "response": "Invalid email or security code"}
    
    except Exception as e:
        return handle_exception(e)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)