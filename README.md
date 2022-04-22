# Flask_model_server
web server code for deep learning model service
<br>

## Version Info
Flask==1.1.4 <br>
markupsafe==2.0.1 <br>
imageio==2.9.0 <br>
pymongo==3.12.0 <br>
mongoengine==0.24.1 <br>
joblib==1.0.1 <br>
<br>

## How to build image file
1. clone this repository into your computer
2. type "docker build -t "image name what you want" "Dockerfile's path"
3. check that the image file has been built or not with "docker images"
4. docker run -d -p "outer port":"inner port" --name "container name what you want" "image file's path"
5. type "docker ps", then you can verify that container is completely made. If not type "docker logs "container name""
6. docker start "container name": start container
7. docker stop "container name": stop container
