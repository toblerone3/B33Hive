FROM python:latest
ADD requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /app
COPY Client.py ./
COPY B33Hive.png ./

RUN mkdir -p /app/RSA
RUN mkdir -p /app/reverseshell

COPY /reverseshell/reverseServer.py /app/reverseshell/reverseServer.py

RUN apt-get update && apt-get install -y libx11-6 libxext-dev libxrender-dev libxinerama-dev libxi-dev libxrandr-dev libxcursor-dev libxtst-dev tk-dev && rm -rf /var/lib/apt/lists/*

RUN apt-get install tk -y


# Commands to run Tkinter application
CMD [ "python3", "./Client.py" ]
