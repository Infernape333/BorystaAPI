FROM python:3.11-slim

# 1. Criar um usuário não-root (ex: borysta_user)
RUN useradd -m borysta_user

# 2. Definir o diretório de trabalho
WORKDIR /app

# 3. Copiar e instalar requisitos como root (para ter permissão de escrita no cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar o restante do código
COPY . .

# 5. Mudar o dono da pasta /app para o novo usuário
RUN chown -R borysta_user:borysta_user /app

# 6. TROCAR PARA O USUÁRIO NÃO-ROOT
USER borysta_user

# 7. Comando para rodar (o usuário agora é seguro)
CMD ["uvicorn", "APP.main:app", "--host", "0.0.0.0", "--port", "8000"]