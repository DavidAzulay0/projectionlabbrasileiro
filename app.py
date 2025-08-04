
import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import date

DB_PATH = os.path.join(os.path.dirname(__file__), "projectionlab_mvp.db")

def conectar_db():
    return sqlite3.connect(DB_PATH)

def carregar_dados(tabela):
    conn = conectar_db()
    df = pd.read_sql_query(f"SELECT * FROM {tabela} WHERE ativo = 1", conn)
    conn.close()
    return df

def inserir_dado(tabela, dados):
    conn = conectar_db()
    colunas = ', '.join(dados.keys())
    valores = tuple(dados.values())
    placeholders = ', '.join(['?'] * len(dados))
    query = f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})"
    conn.execute(query, valores)
    conn.commit()
    conn.close()

# ---------------------- INÍCIO DO APP ----------------------

st.set_page_config(layout="wide", page_title="ProjectionLab BR")

aba = st.sidebar.radio("Escolha a aba:", ["Simulação e Projeções", "Editor de Dados"])

# ------------------- ABA 1: SIMULAÇÃO E PROJEÇÕES -------------------

if aba == "Simulação e Projeções":
    aba_simulacao = st.tabs(["Entradas", "Saídas", "Bens", "Premissas"])

    with aba_simulacao[0]:
        st.header("Visualização de Entradas Ativas")
        df_entradas = carregar_dados("Entradas")
        st.dataframe(df_entradas)

    with aba_simulacao[1]:
        st.header("Visualização de Saídas Ativas")
        df_saidas = carregar_dados("Saidas")
        st.dataframe(df_saidas)

    with aba_simulacao[2]:
        st.header("Visualização de Bens Ativos")
        df_bens = carregar_dados("Bens")
        st.dataframe(df_bens)

    with aba_simulacao[3]:
        st.header("Premissas Atuais")
        df_premissas = carregar_dados("Premissas")
        st.dataframe(df_premissas)

# ------------------- ABA 2: EDITOR DE DADOS -------------------

elif aba == "Editor de Dados":
    st.title("Editor de Entradas, Saídas e Bens")
    categoria = st.radio("Escolha a categoria:", ["Entradas", "Saídas", "Bens"])

    st.markdown(f"### {categoria} Ativas")
    df = carregar_dados(categoria)
    st.dataframe(df)

    st.markdown(f"### Cadastrar Nova {categoria[:-1]}")
    with st.form(key="formulario"):
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor", min_value=0.0, format="%.2f")
        tipo = st.selectbox("Tipo", ["fixo", "variável"])
        data_inicio = st.date_input("Data de Início", value=date.today())
        frequencia = st.selectbox("Frequência", ["mensal", "anual", "única"])
        duracao = st.number_input("Duração (em meses)", min_value=0)
        imposto = st.number_input("Imposto (%)", min_value=0.0, max_value=100.0, step=0.1)
        ativo = 1  # Sempre ativo no cadastro

        submit = st.form_submit_button("Cadastrar")

    if submit:
        nova_linha = {
            "descricao": descricao,
            "valor": valor,
            "tipo": tipo,
            "data_inicio": str(data_inicio),
            "frequencia": frequencia,
            "duracao": duracao,
            "imposto": imposto,
            "ativo": ativo,
        }
        tabela = "Entradas" if categoria == "Entradas" else "Saidas" if categoria == "Saídas" else "Bens"
        inserir_dado(tabela, nova_linha)
        st.success(f"{categoria[:-1]} cadastrada com sucesso!")
