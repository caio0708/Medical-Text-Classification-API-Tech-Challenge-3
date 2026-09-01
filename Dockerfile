# Imagem base leve recomendada para otimização de serviços
FROM python:3.9-slim

# Diretório de trabalho no container
WORKDIR /app

# Copia os arquivos de dependência e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação e o modelo (quando existir)
COPY main.py .

# Expõe a porta que a API rodará
EXPOSE 8000

# Comando para iniciar o servidor Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]