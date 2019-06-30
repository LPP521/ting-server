FROM centos:7.2.1511


RUN set -ex \
    && yum provides '*/applydeltarpm' \
    && rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7 \
    && yum install -y deltarpm \
    && yum update -y \
    && yum install -y wget tar libffi-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make \
    && wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz \
    && tar -xvJf  Python-3.6.5.tar.xz \
    && cd Python-3.6.5 \
    && ./configure prefix=/usr/local/python3 \
    && make \
    && make install \
    && make clean \
    && ln -s /usr/local/python3/bin/python3 /usr/bin/python3 \
    && rm -rf /Python-3.6.5* \
    && yum install -y epel-release \
    && yum install -y python-pip

RUN set -ex \
    && ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3 \
    && python --version \
    && python3 --version

RUN set -ex \
    && rpm --rebuilddb \
    && yum -y install kde-l10n-Chinese telnet \
    && yum -y reinstall glibc-common \
    && yum clean all \
    && localedef -c -f UTF-8 -i zh_CN zh_CN.utf8 

COPY . .

RUN pip2 install --no-cache-dir -r requirements2.txt
RUN pip3 install --no-cache-dir -r requirements3.txt


ENV LC_ALL "zh_CN.UTF-8"

CMD [ "python3", "-m", "aiohttp.web", "-P", "18004", "-H", "0.0.0.0" ,"server:app" ]
