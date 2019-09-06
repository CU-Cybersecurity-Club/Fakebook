FROM ubuntu:18.04

ARG repo="https://github.com/CU-Cybersecurity-Club/Fakebook.git"
ARG flask_user_password="M6S5DNJSLI4Y2P42RDZLHWWLR22XRCZTJ2YVWNH76THB4SHVAK3U6BFETRF2GUQP"
ENV flask_user="flask"
ENV fakebook_home="/home/$flask_user/Fakebook"

# Install required packages
RUN apt-get update -qq -y && \
	apt-get install -qq -y apt-utils
RUN apt-get install -qq -y git python3 python3-pip sudo

### Install webapp in container
# 1. Add user
RUN adduser --quiet --home "/home/$flask_user" $flask_user --disabled-login --shell /bin/bash
RUN echo "$flask_user_password\n$flask_user_password" | passwd $flask_user
USER flask

# 2. Clone repository
RUN mkdir -p $fakebook_home
RUN git clone --depth 1 $repo $fakebook_home

# 3. Install dependencies
RUN pip3 install -r $fakebook_home/requirements.txt --user

# 4. Add a .env for the container
RUN touch $fakebook_home/.env
RUN echo "SECRET_KEY=$(head -c 40 /dev/urandom | base32 -w0)" >> $fakebook_home/.env
RUN echo "PORT=8000" >> $fakebook_home/.env
RUN echo "FLASK_DEBUG=true" >> $fakebook_home/.env

# Expose ports for http and ssh
EXPOSE 22 8000

# Run services when container is started
USER root
COPY run.sh /root/run.sh
CMD /root/run.sh && tail -f /dev/null
