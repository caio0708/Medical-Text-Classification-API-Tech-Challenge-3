# Imagem base leve recomendada para otimização de serviços
FROM python:3.9-slim

# 1. Resolve o erro de idioma (Locale) exigido pelo conversor do ONNX
RUN apt-get update && apt-get install -y locales && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

WORKDIR /app

# 2. Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Resolve o erro de segurança do WSL2/Docker Desktop modificando o pacote recém-instalado
# Ref: https://github.com/MolecularAI/aizynthfinder/issues/194
RUN apt-get update && apt-get install -y --no-install-recommends patchelf \
    && find /usr/local/lib/python3.9/site-packages/onnxruntime -name "*.so" \
        -exec patchelf --clear-execstack {} \; \
    && apt-get purge -y --auto-remove patchelf \
    && rm -rf /var/lib/apt/lists/*

# 4. Copia o código da aplicação e os modelos
COPY main.py .
COPY models/ ./models/

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]