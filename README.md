# configuration

store username and password in secret.yaml, then integrate them in configuration.yaml

```yaml
yro_hassio_beem:
  username: !secret beem_username
  password: !secret beem_password
```

# how to test this addons

## work in a virtual env on vscode side

```
python3 -m venv $PWD/.venv
pip3 install -r requirements.txt
```

## test your addon in a compose project

```
echo WORKSPACE=/home/yroffin/repo/hass-beem > test/.env
cd test && docker compose build && docker compose up
```

# build

```
docker build --build-arg BUILD_FROM="homeassistant/amd64-base:latest" -t local/my-test-addon .
```
