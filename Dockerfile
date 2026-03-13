# 1. Usa uma imagem leve do Python
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copia o arquivo de dependências
COPY requirements.txt .

# 4. Instala as dependências (sem usar cache para a imagem ficar leve)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia a pasta APP para dentro do container
COPY ./APP ./APP

# 6. Expõe a porta 8000
EXPOSE 8000

# 7. Comando para rodar a API (ajustado para seus nomes de pasta/variável)
CMD ["uvicorn", "APP.main:app", "--host", "0.0.0.0", "--port", "8000"]