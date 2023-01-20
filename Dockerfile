FROM deepset/haystack:cpu-v1.12.2


# install dapr
RUN  apt-get update \
    && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/*
# Install dapr CLI
RUN wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

# Install daprd
ARG DAPR_BUILD_DIR
COPY $DAPR_BUILD_DIR /opt/dapr
ENV PATH="/opt/dapr/:${PATH}"
RUN dapr init --slim

# Install your app
WORKDIR /home/user

COPY main.py main.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# TMP
CMD ["tail", "-f", "/dev/null"]

# ENTRYPOINT ["dapr"]
# CMD ["run", "--app-id", "haystack", "--components-path", "./components", "--app-port", "30212", "python3", "main.py"]