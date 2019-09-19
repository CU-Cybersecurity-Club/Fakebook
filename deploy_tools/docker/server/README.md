To build the Docker container: run

```bash
$ touch .env && \
	echo "flask_user_password=$(head -c 40 /dev/urandom | base32 -w0)" > .env && \	
	docker build -t fakebook --network host .
```
