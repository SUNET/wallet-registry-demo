FROM debian:bookworm-20230814-slim@sha256:a60c0c42bc6bdc09d91cd57067fcc952b68ad62de651c4cf939c27c9f007d1c5

MAINTAINER victor@sunet.se

EXPOSE 8006/tcp

# Metadata
LABEL version="1.03"
LABEL description="pkcs11_ca web"

# Set work dir
WORKDIR /app

# Copy the requirement.txt file needed to install deps
COPY ./requirements.txt /app/requirements.txt

# Install deps
RUN apt-get update \
    && apt-get install -y \
    python3-pip \
    python3-dev \
    python3 \
    wget \
    dnsutils \
    python3-venv

RUN python3 -m venv .venv && . .venv/bin/activate \
    && pip3 install --require-hashes -r requirements.txt

# RUN apt-get remove -y \
#     wget \
#     curl \
#     gcc \
#     python3-pip \
#     python3-dev \
#     && apt-get autoremove -y

# Remove setuid and setgid
RUN find / -xdev -perm /6000 -type f -exec chmod a-s {} \; || true

# Add user and add to softhsm group
RUN useradd wallet -u 1500 -s /usr/sbin/nologin

# Copy files
COPY ./src /app/src
# COPY ./tests /app/tests
# COPY ./data/trusted_keys /app/trusted_keys
# COPY ./containers/healthcheck.sh /app/healthcheck.sh
# COPY ./containers/healthcheck.py /app/healthcheck.py
COPY ./containers/logging.json /app/logging.json
# COPY ./data/tls_certificate.pem /app/tls_certificate.pem
# COPY ./data/tls_key.key /app/tls_key.key

# Run as user
USER wallet

# Add healthcheck
# HEALTHCHECK --interval=120s --timeout=15s --retries=1 --start-period=30s \
#     CMD sh '. .venv/bin/activate && healthcheck.sh' || bash -c 'kill -s 15 1 && (sleep 7; kill -s 9 1)'

CMD sh -c '. .venv/bin/activate && uvicorn src.wallet_registry.main:app --log-config ./logging.json --host 0.0.0.0 --port 8006 --workers 1 --header server:wallet_registry'