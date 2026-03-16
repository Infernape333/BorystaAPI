# 🛡️ Motor de Risco SUFRAMA Digital - Desafio Borysta

Este repositório contém o desenvolvimento de um **Microsserviço de Análise de Risco** para o ecossistema da SUFRAMA Digital. A solução foi projetada para processar dados de Protocolos de Internamento de Mercadoria (PIN) e determinar, através de critérios técnicos, o nível de criticidade de cada operação.

---

## 🚀 Estrutura do Projeto: O Desafio vs. O Plus

O projeto foi dividido em duas camadas para demonstrar competência técnica e visão de produto:

### 1. ⚙️ Back-end: Motor de Risco (Requisito Obrigatório)
O núcleo da aplicação, desenvolvido rigorosamente conforme os requisitos técnicos solicitados.
* **API RESTful:** Desenvolvida com **FastAPI**, focada em performance e padronização.
* **Segurança de Processo:** Implementação de boas práticas de Docker, rodando a aplicação com um **usuário não-root** dedicado, mitigando riscos de segurança no ambiente de execução.
* **Documentação Interativa:** Disponível via Swagger UI, permitindo a validação de todos os esquemas de dados de forma imediata.

### 2. 🖥️ Interface BorystaIA (Melhoria Criativa)
Como uma iniciativa própria, desenvolvi um **Front-end exclusivo** para transformar o motor de risco em uma ferramenta visual completa.
* **Dashboard de Fiscalização:** Interface intuitiva desenvolvida em **Streamlit** para entrada de dados e visualização de resultados.
* **Validação em Tempo Real:** O sistema identifica campos vazios ou incompletos antes do envio, otimizando a experiência do usuário.
* **Banco de Dados Volátil (In-Memory):** Implementação de um histórico de sessões que impede a duplicidade de PINs e Nomes de Empresas, permitindo o acompanhamento de múltiplas análises simultâneas.

---

## 🎯 A Ideia por Trás do Projeto

O objetivo central foi criar um motor que auxiliasse na tomada de decisão de inspeção fiscal de forma previsível. Implementei uma regra de negócio baseada em **Interpolação Linear**, onde o score de risco cresce proporcionalmente ao valor da mercadoria dentro de cada canal (Verde, Amarelo, Vermelho), permitindo uma triagem refinada e justa.

---

## 🛠️ Tecnologias Utilizadas

### **Python 3.11 & FastAPI**
Optei pelo FastAPI pela alta concorrência com `uvicorn` e pela robustez da tipagem estática, que reduz erros em produção.

### **Pydantic (Validação)**
Garante a integridade dos dados, assegurando que apenas PINs com informações válidas (estados, valores positivos e IDs) sejam processados.

### **Docker & Docker Compose**
* **Dockerfile:** Utiliza imagem *slim* e cria um usuário de sistema para execução segura.
* **Docker Compose:** Orquestra a API e o Front-end em containers isolados que se comunicam via rede interna segura.

---

## ⚙️ Regras de Negócio e Algoritmo de Risco

| Critério | Canal | Score | Lógica Aplicada |
| :--- | :--- | :--- | :--- |
| **Valor < 100k** | Verde | 0 - 39 | Risco baixo, proporcional ao valor. |
| **100k - 500k** | Amarelo | 40 - 79 | Risco moderado. Interpolação baseada na faixa. |
| **Valor > 500k ou Infração** | Vermelho | 80 - 100 | Risco crítico. Infrações levam o score ao topo. |

---

## 🚦 Como Executar e Testar

### Rodando com Docker
1. Clone este repositório.

2. Na raiz do projeto, execute:
   docker-compose up --build

3. Para ir para a API use o localhost:
   http://127.0.0.1:8000/docs#/default/analyze_risk_api_v1_risk_score_post

4. Para ir para o Frontend use o localhost:
   localhost:8501