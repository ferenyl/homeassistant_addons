# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Execute during the build of the image
ARG TEMPIO_VERSION BUILD_ARCH

# Install dependencies
RUN \
    apk add --no-cache \
        python3 \
        py3-pip \
        python3-dev \
        libffi-dev \
        openssl-dev \
        nginx \
        git \
        openssh-client \
        bash \
        gcc \
        musl-dev \
    && \
    curl -sSLf -o /usr/bin/tempio \
    "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${BUILD_ARCH}" \
    && \
    chmod a+x /usr/bin/tempio

# Install MkDocs and plugins
RUN \
    pip3 install --no-cache-dir \
        mkdocs \
        mkdocs-mermaid2-plugin \
        mkdocs-minify-plugin \
        mkdocs-material \
        mkdocs-awesome-pages-plugin

# Copy root filesystem
COPY rootfs /

# Create necessary directories
RUN \
    mkdir -p /var/run/nginx \
    && mkdir -p /var/www/html \
    && mkdir -p /tmp/mkdocs \
    && ln -sf /homeassistant /config

# Set permissions
RUN \
    chmod +x /etc/services.d/mkdocs/run \
    && chmod +x /etc/services.d/mkdocs/finish \
    && chmod +x /usr/bin/mkdocs_build \
    && chmod +x /etc/cont-init.d/nginx.sh
