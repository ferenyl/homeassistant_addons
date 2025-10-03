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
  netcat-openbsd \
  && \
  curl -sSLf -o /usr/bin/tempio \
  "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${BUILD_ARCH}" \
  && \
  chmod a+x /usr/bin/tempio

# Install MkDocs and plugins
RUN pip3 install --upgrade pip setuptools
RUN \
  pip3 install --no-cache-dir \
  mkdocs \
  mkdocs-mermaid2-plugin \
  mkdocs-minify-plugin \
  mkdocs-material \
  mkdocs-awesome-pages-plugin

# Copy root filesystem
COPY rootfs /


# Create necessary directories and remove default nginx configs
RUN \
  mkdir -p /var/run/nginx \
  && mkdir -p /var/www/html \
  && mkdir -p /tmp/mkdocs \
  && ln -sf /homeassistant /config \
  && rm -rf /etc/nginx/conf.d/*

# Set permissions
RUN \
  chmod +x /etc/cont-init.d/10-build-mkdocs \
  && chmod +x /etc/cont-init.d/10-generate-nginx-config \
  && chmod +x /etc/services.d/nginx/run \
  && chmod +x /etc/services.d/nginx/finish \
  && chmod +x /etc/services.d/mkdocs-api/run \
  && chmod +x /etc/services.d/mkdocs-api/finish \
  && chmod +x /usr/bin/mkdocs-rebuild \
  && chmod +x /usr/bin/mkdocs-api-server \
  && chmod +x /usr/bin/mkdocs-api-server.py \
  && rm -f -r \
  /app \
  /etc/init.d/nginx \
  /etc/logrotate.d/nginx \
  /opt/nginx-proxy-manager/node_modules/bcrypt/build \
  /root/.cache \
  /root/.node-gyp \
  /tmp/.[!.]* \
  /tmp/* \
  /usr/lib/node_modules \
  /usr/local/share/.cache \
  /var/lib/nginx \
  /var/log/nginx \
  /var/tmp/nginx \
  /var/www
