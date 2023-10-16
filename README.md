# PYTHON BACKEND PROJECT
### Instructions for running the project locally

**Step 1:** 
Clone the repository locally

Write a command:
```
git clone https://github.com/DyshkantiukO/python_backend_project.git
```
Go to the cloned folder

**Step 2:** 
Build an image

Run Docker

Write a command:
```
docker build --build-arg PORT=<your port> . -t <image_name>:latest
```

**Step 3:**
Run and check if the application works

Write a command:
```
docker run -it --rm --network=host <image_name>:latest
```

**Step 4:**
Install docker-compose and try to build and run the container using commands:
```
docker-compose build
docker-compose up
```
