# python:3.8-slim image is installed basically
FROM python:3.8-slim
#FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-devel
COPY . /app
WORKDIR /app
# commands will be executed as follows when iamges are created
RUN apt-get update
# -y: yes to all question
RUN apt-get install -y vim
RUN apt-get install -y git
# clone slayer from remote repository
RUN git clone https://github.com/bamsumit/slayerPytorch.git

# install build-essential package for gcc compiler
RUN apt install build-essential

# install all of the modules written in requirements.txt
RUN pip3 install -r requirements.txt

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
