FROM python:3.6.0

RUN apt-get update && apt-get install -y \
        # Required for geodjango
        binutils libproj-dev gdal-bin \
    && apt-get autoremove -y --purge \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/
RUN wget https://nodejs.org/dist/v7.10.0/node-v7.10.0-linux-x64.tar.xz \
    && tar xvf node-v7.10.0-linux-x64.tar.xz \
    && cp -rp node-v7.10.0-linux-x64/* /usr/local/ \
    && rm -rf node-v7.10.0-linux-x64.tar.xz node-v7.10.0-linux-x64/

WORKDIR /usr/local/lib/
RUN wget https://github.com/sass/libsass/archive/3.4.4.tar.gz \
    && tar xvzf 3.4.4.tar.gz && rm 3.4.4.tar.gz
ENV SASS_LIBSASS_PATH "/usr/local/lib/libsass-3.4.4"
RUN echo 'SASS_LIBSASS_PATH="/usr/local/lib/libsass-3.4.4"' >> /etc/environment

RUN wget https://github.com/sass/sassc/archive/3.4.2.tar.gz \
    && tar xvzf 3.4.2.tar.gz && rm 3.4.2.tar.gz
WORKDIR /usr/local/lib/sassc-3.4.2/
RUN make && ln -s /usr/local/lib/sassc-3.4.2/bin/sassc /usr/local/bin/sassc

RUN npm install gulp-cli -g

RUN curl -o- -L https://yarnpkg.com/install.sh | bash -s -- --version 0.24.6
RUN ln -s /root/.yarn/bin/yarn /usr/local/bin/yarn

RUN easy_install -U pip
RUN apt-get update && apt-get install -y gettext libgettextpo-dev

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
