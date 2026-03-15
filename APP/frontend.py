import streamlit as st
import requests
import random
from datetime import datetime

st.set_page_config(page_title="BorystaAI", layout="centered")

if 'banco_de_dados' not in st.session_state:
    st.session_state['banco_de_dados'] = []

st.markdown("""
    <style>
    .result  {
            border: 1px solid #000000;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 5px;
            color: #000000;
            }
    </style>
""", unsafe_allow_html=True)

st.title("BorystaAI - Motor de Risco SUFRAMA Digital")
st.subheader("API para análise de risco de Notas Fiscais e PINs")

with st.form("risk_analysis_form"):
    col1, col2 = st.columns(2)
    with col1:
        pin_id = st.text_input("PIN ID", placeholder="Ex: PIN123456")
        company_name = st.text_input("Nome da Empresa", placeholder="Ex: Empresa XYZ LTDA")
        merchandise_value = st.number_input("Valor da Mercadoria", min_value=0.01, step=0.01, format="%f")
    with col2:
        origin_state = st.text_input("Estado de Origem", max_chars=2, placeholder="Ex: SP")
        destination_state = st.text_input("Estado de Destino", max_chars=2, placeholder="Ex: AM")
        has_infractions = st.checkbox("Possui Infrações Anteriores?")
    submit_button = st.form_submit_button("Analisar Risco")

if submit_button:
    # Ajuste nas chaves para bater com o que foi salvo no "banco"
    nomes_existentes = [registro.get('Empresa', '') for registro in st.session_state['banco_de_dados']]
    ids_existentes = [registro.get('PIN ID', '') for registro in st.session_state['banco_de_dados']]

    missing_messages = []
    if not pin_id.strip(): missing_messages.append("PIN ID vazio ou incompleto")
    if not company_name.strip(): missing_messages.append("Nome da Empresa vazio ou incompleto")
    if len(origin_state.strip()) != 2: missing_messages.append("Estado de Origem vazio ou incompleto")
    if len(destination_state.strip()) != 2: missing_messages.append("Estado de Destino vazio ou incompleto")

    if missing_messages:
        for msg in missing_messages:
            st.warning(msg)
    else:
        if company_name in nomes_existentes:
            st.warning(f"Nome da empresa '{company_name}' já está registrado.")
        elif pin_id in ids_existentes:
            st.warning(f"PIN ID '{pin_id}' já está registrado.")
        else:
            payload = {
                "pin_id": pin_id,
                "company_name": company_name,
                "merchandise_value": merchandise_value,
                "origin_state": origin_state,
                "destination_state": destination_state,
                "has_previous_infractions": has_infractions
            }

            try:
                # SÓ UM BLOCO DE REQUEST AGORA
                response = requests.post("http://api-risco:8000/api/v1/risk-score", json=payload)
                response.raise_for_status()
                result = response.json()

                data_formatada = datetime.now().strftime('%d/%m/%Y')

                novo_registro = {
                    "PIN ID": result.get("pin_id", pin_id), 
                    "Empresa": result.get("company_name", company_name),
                    "Origem": origin_state.upper(),
                    "Destino": destination_state.upper(),
                    "Score": result.get("risk_score"),
                    "Nível": result.get("risk_level"),
                    "Data": data_formatada
                }

                st.session_state['banco_de_dados'].append(novo_registro)

                st.markdown(f"""
                    <div class="result">
                        <h3>Resultado da Análise de Risco</h3>
                        <p><strong>PIN ID:</strong> {novo_registro['PIN ID']}</p>
                        <p><strong>Risco:</strong> {novo_registro['Nível']} ({novo_registro['Score']} pts)</p>
                        <p><strong>Rota:</strong> {novo_registro['Origem']} ➡️ {novo_registro['Destino']}</p>
                        <p><strong>Data:</strong> {novo_registro['Data']}</p>
                    </div>
                """, unsafe_allow_html=True)

            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao conectar com a API: {e}")

st.write("---")
st.subheader("📋 Histórico de Análises")

if st.session_state['banco_de_dados']:
    st.table(st.session_state['banco_de_dados'])
    if st.button("Limpar Histórico"):
        st.session_state['banco_de_dados'] = []
        st.rerun()
else:
    st.info("Nenhuma análise realizada ainda.")