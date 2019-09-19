FROM alpine

ARG REPO="https://github.com/CU-Cybersecurity-Club/Fakebook.git"
ARG DEBUG="false"
ENV FAKEBOOK_HOME="/var/www/fakebook"

# Install required packages
RUN apk update && apk upgrade
RUN apk add --no-cache build-base gcc abuild binutils \
		binutils-doc gcc-doc
RUN apk add --no-cache git python3 python3-dev sqlite \
		sudo libffi-dev openssl-dev

###
### Install gunicorn webapp
###
# Clone repository
RUN mkdir -p "$FAKEBOOK_HOME"
RUN adduser www-data -h /var/www -D && \
	chown -R www-data "$FAKEBOOK_HOME" && \
	chgrp -R www-data "$FAKEBOOK_HOME"

USER www-data
RUN git clone --depth 1 "$REPO" "$FAKEBOOK_HOME"

# Install dependencies
USER root
RUN python3 -m pip install -q --no-cache-dir setuptools
RUN python3 -m pip install -r "$FAKEBOOK_HOME/requirements.txt" \
		--no-cache-dir --no-warn-script-location
USER www-data

# Add a .env for the gunicorn server
RUN echo "SECRET_KEY=$(head -c 40 /dev/urandom | base64 | tr -d '\n')" > \
	"$FAKEBOOK_HOME/.env"
RUN echo "PORT=unix:/tmp/webserver.socket" >> "$FAKEBOOK_HOME/.env"
RUN echo "FLASK_DEBUG=$DEBUG" >> "$FAKEBOOK_HOME/.env"

# Reset the database
RUN cd "$FAKEBOOK_HOME" && \
	chmod +x reset_db.sh && \
	./reset_db.sh

# Add gunicorn config into /etc/gunicorn/
USER root
RUN mkdir /etc/gunicorn
COPY config/gunicorn.py /etc/gunicorn/gunicorn.py

# Expose ports for http and https
EXPOSE 8000

# Run gunicorn and nginx servers when the container is started
USER root
COPY run.sh /root/run.sh
CMD /root/run.sh && tail -f /dev/null
