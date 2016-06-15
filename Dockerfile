FROM python:3.5.1

RUN apt-get update \
    && apt-get install -y gettext \
    && apt-get autoremove -y --purge \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/
RUN wget https://nodejs.org/dist/v6.1.0/node-v6.1.0-linux-x64.tar.xz \
    && tar xvf node-v6.1.0-linux-x64.tar.xz \
    && cp -rp node-v6.1.0-linux-x64/* /usr/local/ \
    && rm -rf node-v6.1.0-linux-x64.tar.xz node-v6.1.0-linux-x64/

WORKDIR /usr/local/lib/
RUN wget https://github.com/sass/libsass/archive/3.3.6.tar.gz \
    && tar xvzf 3.3.6.tar.gz && rm 3.3.6.tar.gz
ENV SASS_LIBSASS_PATH "/usr/local/lib/libsass-3.3.6"
RUN echo 'SASS_LIBSASS_PATH="/usr/local/lib/libsass-3.3.6"' >> /etc/environment
RUN wget https://github.com/sass/sassc/archive/3.3.6.tar.gz \
    && tar xvzf 3.3.6.tar.gz && rm 3.3.6.tar.gz
WORKDIR /usr/local/lib/sassc-3.3.6/
RUN make && ln -s /usr/local/lib/sassc-3.3.6/bin/sassc /usr/local/bin/sassc

RUN mkdir /code
WORKDIR /code
RUN easy_install -U pip
RUN npm install -g gulp bower

ADD requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
