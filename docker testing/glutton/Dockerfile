FROM debian:latest
LABEL authors="Toby, Ethan, Cal, Kris"

ENTRYPOINT ["top", "-b"]

RUN apt-get update && apt-get install sudo -y

RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

USER docker
CMD /bin/bash
RUN sudo apt-get upgrade -y

RUN sudo apt-get install gcc libpcap-dev iptables -y

RUN sed -i 's/[# ]*Port .*/Port 5001/g' /etc/ssh/sshd_config #unsure if this will work. taken strignt from github, instructions unclear.
RUN exit