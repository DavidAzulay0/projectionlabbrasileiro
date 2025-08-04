import streamlit as st
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("simulador_financeiro.db")
cursor = conn.cursor()

st.title("💰 Simulador Financeiro de Casal - MVP")

st.sidebar.header("Menu")
opcao = st.sidebar.selectbox("Selecione uma seção", ["Entradas", "Saídas", "Bens", "Premissas Gerais"])

# --- Entradas ---
if opcao == "Entradas":
    st.subheader("Cadastrar Nova Entrada")
    nome = st.text_input("Nome da Entrada")
    valor = st.number_input("Valor Anual (R$)", min_value=0.0)
    fonte = st.selectbox("Fonte", ["parceiro1", "parceiro2", "casal"])
    if st.button("Adicionar Entrada"):
        cursor.execute("INSERT INTO Entradas (nome, valor_anual, fonte) VALUES (?, ?, ?)", (nome, valor, fonte))
        conn.commit()
        st.success("Entrada adicionada com sucesso!")

# --- Saídas ---
elif opcao == "Saídas":
    st.subheader("Cadastrar Nova Saída")
    nome = st.text_input("Nome da Saída")
    valor = st.number_input("Valor Anual (R$)", min_value=0.0)
    tipo = st.text_input("Tipo (ex: moradia, transporte)")
    if st.button("Adicionar Saída"):
        cursor.execute("INSERT INTO Saidas (nome, valor_anual, tipo) VALUES (?, ?, ?)", (nome, valor, tipo))
        conn.commit()
        st.success("Saída adicionada com sucesso!")

# --- Bens ---
elif opcao == "Bens":
    st.subheader("Cadastrar Novo Bem")
    nome = st.text_input("Nome do Bem")
    tipo = st.selectbox("Tipo", ["imovel", "reserva_emergencia", "investimento", "divida"])
    valor = st.number_input("Valor Atual (R$)", min_value=0.0)
    rendimento = st.number_input("Rendimento Esperado (%)", min_value=0.0)
    passivo = st.checkbox("É Passivo?")
    if st.button("Adicionar Bem"):
        cursor.execute("""
            INSERT INTO Bens (nome, tipo, valor, rendimento_esperado, passivo) 
            VALUES (?, ?, ?, ?, ?)""", (nome, tipo, valor, rendimento, passivo))
        conn.commit()
        st.success("Bem adicionado com sucesso!")

# --- Premissas Gerais ---
elif opcao == "Premissas Gerais":
    st.subheader("Definir Premissas Financeiras")
    ano = st.number_input("Ano Inicial", min_value=2020, step=1)
    inflacao = st.number_input("Taxa de Inflação (%)", min_value=0.0)
    crescimento_entrada = st.number_input("Crescimento Entradas (%)", min_value=0.0)
    crescimento_saida = st.number_input("Crescimento Saídas (%)", min_value=0.0)
    juros_divida = st.number_input("Juros Dívidas (%)", min_value=0.0)
    rendimento_inv = st.number_input("Rendimento Investimentos (%)", min_value=0.0)
    if st.button("Salvar Premissas"):
        cursor.execute("""
            INSERT INTO PremissasGerais (ano_inicial, taxa_inflacao, taxa_crescimento_entradas, taxa_crescimento_saidas, taxa_juros_dividas, taxa_rendimento_investimentos) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ano, inflacao, crescimento_entrada, crescimento_saida, juros_divida, rendimento_inv))
        conn.commit()
        st.success("Premissas salvas com sucesso!")
