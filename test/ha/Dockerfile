FROM alpine:latest AS fswatch

RUN apk add --no-cache autoconf alpine-sdk

RUN rm /usr/include/sys/inotify.h
RUN wget https://github.com/emcrisostomo/fswatch/releases/download/1.17.1/fswatch-1.17.1.tar.gz \
    && tar -xzvf fswatch-1.17.1.tar.gz \
    && cd fswatch-1.17.1 \
    && ./configure \
    && make \
    && make install \
    && rm -rf /fswatch-1.17.1

FROM ghcr.io/home-assistant/home-assistant:stable

# Add fswatch
COPY --from=fswatch /usr/local/bin/fswatch /usr/local/bin/fswatch
COPY --from=fswatch /usr/local/lib/libfswatch.so* /usr/local/lib/

RUN apk add supervisor
COPY supervisord.conf /etc/supervisor.d/fswatch.ini

COPY fswatch.sh /
COPY check.sh /
COPY entrypoint.sh /
COPY config_entries.py /usr/src/homeassistant/homeassistant/config_entries.py

HEALTHCHECK --interval=1ms --timeout=5s \
    CMD sh /check.sh || exit 1

ENTRYPOINT [ "/entrypoint.sh" ]