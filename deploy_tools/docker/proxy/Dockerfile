FROM nginx

###
### Copy nginx config files into the container
###
COPY config/nginx.conf /etc/nginx/nginx.conf
RUN mkdir /etc/nginx/sites-available && \
	mkdir /etc/nginx/sites-enabled
COPY config/webserver.nginx /etc/nginx/sites-available
RUN ln -s /etc/nginx/sites-available/* /etc/nginx/sites-enabled/

# Create caching directory for nginx
RUN mkdir -p /data/nginx/cache && \
	chown -R www-data /data/nginx/cache && \
	chgrp -R www-data /data/nginx/cache

# Copy SSL certificates
RUN mkdir -p /etc/letsencrypt/live/fakebook/
COPY keys/fullchain.pem /etc/letsencrypt/live/fakebook/
COPY keys/privkey.pem /etc/letsencrypt/live/fakebook/

# Expose ports for http and https
EXPOSE 80 443

# Run nginx proxy when the container is started
COPY run.sh /root/run.sh
CMD /root/run.sh && tail -f /dev/null
