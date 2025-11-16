# Dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Instala dependências do sistema e GTK
RUN apt-get update && apt-get install -y \
  python3 python3-pip python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
  libgirepository1.0-dev gobject-introspection gir1.2-glib-2.0 \
  xvfb xauth x11-apps \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements.txt apenas se existir
# (não dá erro caso o arquivo não exista)
COPY requirements.txt /tmp/requirements.txt
RUN test -f /tmp/requirements.txt && pip install -r /tmp/requirements.txt || echo "Nenhum requirements.txt encontrado"

# Copiar código-fonte
COPY src/ ./src/

CMD ["bash"]
