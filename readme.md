# install packages
>> pip install -r requirements.txt

# run file
>> uvicorn main:app


# docker command
>> docker build -t image_name:version .
- Used for creating a image from a Dockerfile
- for eg: docker build -t blog:v1

>> docker run -d -t -p 8000:8000 image_name:version
- for eg docker run -d -t -p 8000:8000 blog:v1

>> docker ps
- Used to check for running containers

>> docker images
- Used to check for locally available images


## API Endpoints

### blog_api

- `/blog/get-all-blogs/`: Endpoint for getting all the blogs from the database.
- `/blog/get-blog/{title}/`: Endpoint for getting title specific blog.
- `/blog/create-blog/`: Endpoint for writing blog.
- `/blog/update-blog/`: Endpoint for modifying an existing blog.
- `/blog/delete-blog/`: Endpoint for deleting an existing blog.


### edmonk_api

- `/webinar/get-all-webinars/`: Endpoint for getting all the webinars from the database.
- `/webinar/create-webinar/`: Endpoint for writing webinar.
- `/webinar/update-webinar/{webinarTitle}`: Endpoint for modifying an existing webinar.
- `/webinar/delete-webinar/{webinarTitle}`: Endpoint for deleting an existing webinar.