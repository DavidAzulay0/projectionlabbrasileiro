import streamlit as st
import sqlite3
import pandas as pd

# Conexão com o banco SQLite
DB_PATH = os.path.join("data", "projectionlab_mvp.db")

# Funções utilitárias
def carregar_dados(tabela):
    conn = sqlite3.connect(DB_PATH)
    return pd.read_sql_query(f"SELECT * FROM {tabela} WHERE ativo = 1", conn)

def atualizar_registro(tabela, id, colunas, valores):
    sets = ', '.join([f"{col} = ?" for col in colunas])
    cursor.execute(f"UPDATE {tabela} SET {sets} WHERE id = ?", (*valores, id))
    conn.commit()

def deletar_registro(tabela, id):
    cursor.execute(f"UPDATE {tabela} SET ativo = 0 WHERE id = ?", (id,))
    conn.commit()

# Título principal
st.title("Editor de Entradas, Saídas e Bens")

aba = st.radio("Escolha a categoria:", ["Entradas", "Saídas", "Bens"])

if aba == "Entradas":
    st.subheader("Entradas Ativas")
    df = carregar_dados("Entradas")
    for _, row in df.iterrows():
        with st.expander(f"{row['nome']} - R$ {row['valor_anual']:.2f}/ano"):
            novo_nome = st.text_input(f"Nome #{row['id']}", row['nome'], key=f"nome_entrada_{row['id']}")
            novo_valor = st.number_input(f"Valor anual #{row['id']}", value=row['valor_anual'], key=f"valor_entrada_{row['id']}")
            nova_fonte = st.text_input(f"Fonte #{row['id']}", row['fonte'] or "", key=f"fonte_entrada_{row['id']}")
            if st.button("Salvar", key=f"salvar_entrada_{row['id']}"):
                atualizar_registro("Entradas", row['id'], ["nome", "valor_anual", "fonte"], [novo_nome, novo_valor, nova_fonte])
                st.success("Entrada atualizada!")
                st.experimental_rerun()
            if st.button("Excluir", key=f"excluir_entrada_{row['id']}"):
                deletar_registro("Entradas", row['id'])
                st.warning("Entrada excluída.")
                st.experimental_rerun()

elif aba == "Saídas":
    st.subheader("Saídas Ativas")
    df = carregar_dados("Saidas")
    for _, row in df.iterrows():
        with st.expander(f"{row['nome']} - R$ {row['valor_anual']:.2f}/ano"):
            novo_nome = st.text_input(f"Nome #{row['id']}", row['nome'], key=f"nome_saida_{row['id']}")
            novo_valor = st.number_input(f"Valor anual #{row['id']}", value=row['valor_anual'], key=f"valor_saida_{row['id']}")
            novo_tipo = st.text_input(f"Tipo #{row['id']}", row['tipo'], key=f"tipo_saida_{row['id']}")
            if st.button("Salvar", key=f"salvar_saida_{row['id']}"):
                atualizar_registro("Saidas", row['id'], ["nome", "valor_anual", "tipo"], [novo_nome, novo_valor, novo_tipo])
                st.success("Saída atualizada!")
                st.experimental_rerun()
            if st.button("Excluir", key=f"excluir_saida_{row['id']}"):
                deletar_registro("Saidas", row['id'])
                st.warning("Saída excluída.")
                st.experimental_rerun()

elif aba == "Bens":
    st.subheader("Bens Ativos")
    df = carregar_dados("Bens")
    for _, row in df.iterrows():
        with st.expander(f"{row['nome']} - R$ {row['valor']:.2f}"):
            novo_nome = st.text_input(f"Nome #{row['id']}", row['nome'], key=f"nome_bem_{row['id']}")
            novo_valor = st.number_input(f"Valor #{row['id']}", value=row['valor'], key=f"valor_bem_{row['id']}")
            novo_tipo = st.text_input(f"Tipo #{row['id']}", row['tipo'], key=f"tipo_bem_{row['id']}")
            novo_rendimento = st.number_input(f"Rendimento esperado #{row['id']}", value=row['rendimento_esperado'], key=f"rendimento_bem_{row['id']}")
            novo_passivo = st.checkbox(f"É passivo?", value=bool(row['passivo']), key=f"passivo_bem_{row['id']}")
            if st.button("Salvar", key=f"salvar_bem_{row['id']}"):
                atualizar_registro("Bens", row['id'], ["nome", "valor", "tipo", "rendimento_esperado", "passivo"],
                                   [novo_nome, novo_valor, novo_tipo, novo_rendimento, int(novo_passivo)])
                st.success("Bem atualizado!")
                st.experimental_rerun()
            if st.button("Excluir", key=f"excluir_bem_{row['id']}"):
                deletar_registro("Bens", row['id'])
                st.warning("Bem excluído.")
                st.experimental_rerun()
