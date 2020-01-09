all:
	docker build -f Dockerfile.base -t u03013112/py2and3 .
	docker build -t u03013112/ting-server .
push:
	docker push u03013112/ting-server