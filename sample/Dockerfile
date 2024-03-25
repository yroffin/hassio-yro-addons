ARG BUILD_FROM
FROM $BUILD_FROM

ARG BUILD_VERSION

# Create Working Directory
WORKDIR /app

# Install enoceanmqtt and requirements
RUN apk add --no-cache python3 py3-pip git && \
    python3 -m venv /app/venv && \
    . /app/venv/bin/activate && \
    python3 -m pip install --upgrade pip && \
    git clone -b main --single-branch --depth 1 https://github.com/yroffin/hassio-yro-addons && echo `date`

# Copy data for add-on
COPY run.sh .
RUN chmod a+x run.sh

CMD [ "/app/run.sh" ]
