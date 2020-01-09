FROM u03013112/py2and3

COPY requirements2.txt requirements2.txt
COPY requirements3.txt requirements3.txt

RUN pip2 install --no-cache-dir -r requirements2.txt
RUN pip3 install --no-cache-dir -r requirements3.txt

COPY . .

ENV LC_ALL "zh_CN.UTF-8"

CMD [ "python3", "-m", "aiohttp.web", "-P", "18004", "-H", "0.0.0.0" ,"server:app" ]
