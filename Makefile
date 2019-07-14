all:
	docker build -t u03013112/ting-server .
push:
	docker push u03013112/ting-server