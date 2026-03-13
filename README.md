# 🛡️ Motor de Risco SUFRAMA Digital - Desafio Borysta

Este repositório contém o desenvolvimento de um **Microsserviço de Análise de Risco** para o ecossistema da SUFRAMA Digital. A solução foi projetada para processar dados de Protocolos de Internamento de Mercadoria (PIN) e determinar, através de critérios técnicos, o nível de criticidade de cada operação.

---

## 🎯 A Ideia por Trás do Projeto

O objetivo central foi criar um motor que não fosse apenas um "gerador de números aleatórios", mas uma ferramenta que pudesse auxiliar na tomada de decisão de inspeção fiscal. 

A ideia foi unir **segurança de dados**, **performance** e uma **lógica de risco previsível**. Para isso, implementei uma regra de negócio baseada em faixas de valores e antecedentes, onde o score de risco cresce proporcionalmente ao valor da mercadoria dentro de cada canal, permitindo uma triagem muito mais refinada.

---

## 🛠️ Tecnologias Utilizadas e o "Porquê"

### 1. **Python 3.11 & FastAPI**
Optei pelo **FastAPI** por ser um dos frameworks mais modernos e rápidos da atualidade. 
- **Performance:** Ele utiliza `uvicorn` (ASGI), permitindo alta concorrência.
- **Documentação Automática:** O Swagger UI embutido facilita o teste imediato para os avaliadores e desenvolvedores de front-end.
- **Tipagem Estática:** O uso de Type Hints reduz drasticamente a chance de erros em produção.

### 2. **Pydantic (Validação de Dados)**
Fundamental para a integridade do sistema. O código utiliza modelos Pydantic para garantir que o PIN só seja processado se todos os campos (como estados, valores positivos e IDs) estiverem corretos, retornando erros claros caso contrário.

### 3. **Docker & Docker Compose**
Para garantir a "portabilidade total". 
- O **Dockerfile** utiliza uma imagem *slim* para reduzir o consumo de recursos.
- O **Docker Compose** permite que o ambiente seja levantado com um único comando, isolando as dependências do Python do sistema operacional do avaliador.

---

## ⚙️ Regras de Negócio e Algoritmo de Risco

O coração da aplicação é a função de cálculo de risco, que segue uma lógica de **Interpolação Linear** para evitar saltos bruscos no score:

| Critério | Canal | Score | Lógica Aplicada |
| :--- | :--- | :--- | :--- |
| **Valor < 100k** | Verde | 0 - 39 | Risco baixo, proporcional ao valor. |
| **100k - 500k** | Amarelo | 40 - 79 | Risco moderado. Ex: R$ 300k gera um score ~59. |
| **Valor > 500k ou Infração** | Vermelho | 80 - 100 | Risco crítico. Infrações levam o score direto ao topo. |

---

## 🚀 Como Executar e Testar

### Rodando com Docker
1. Clone este repositório.
2. Na raiz, execute:
   docker-compose up --build