# python:3.8-slim image is installed basically
FROM python:3.8-slim

COPY . /app
WORKDIR /app
# commands will be executed as follows when iamges are created
RUN apt-get update
# RUN apt-get install vim -> error occur
RUN pip3 install -r requirements.txt

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
