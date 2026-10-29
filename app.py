import streamlit as st
import pandas as pd
from datetime import date
 
st.set_page_config(
page_title="Dev Team Planner",
layout="wide"
)
 
# Inicialização
if "tasks" not in st.session_state:
st.session_state.tasks = [
{
"id": 1,
"titulo": "Implementar Login MFA",
"responsavel": "Pedro",
"status": "Backlog",
"prioridade": "Alta",
"inicio": "2026-10-21",
"fim": "2026-10-25"
},
{
"id": 2,
"titulo": "Dashboard Financeiro",
"responsavel": "Ana",
"status": "Em Progresso",
"prioridade": "Média",
"inicio": "2026-10-20",
"fim": "2026-10-30"
}
]
 
st.title("🚀 Gerenciamento de Atividades da Equipe")
 
# Sidebar
st.sidebar.header("Nova Atividade")
 
titulo = st.sidebar.text_input("Título")
 
responsavel = st.sidebar.selectbox(
"Responsável",
["Ana", "Carlos", "Pedro", "Marina"]
)
 
prioridade = st.sidebar.selectbox(
"Prioridade",
["Baixa", "Média", "Alta", "Crítica"]
)
 
inicio = st.sidebar.date_input("Data de Início", value=date.today())
fim = st.sidebar.date_input("Data de Entrega", value=date.today())
 
if st.sidebar.button("Adicionar"):
novo_id = len(st.session_state.tasks) + 1
 
st.session_state.tasks.append({
"id": novo_id,
"titulo": titulo,
"responsavel": responsavel,
"status": "Backlog",
"prioridade": prioridade,
"inicio": str(inicio),
"fim": str(fim)
})
 
st.sidebar.success("Atividade criada!")
 
# Converter em DataFrame
df = pd.DataFrame(st.session_state.tasks)
 
# Indicadores
st.subheader("📊 Indicadores")
 
c1, c2, c3 = st.columns(3)
 
c1.metric("Total de Atividades", len(df))
c2.metric(
"Em Progresso",
len(df[df["status"] == "Em Progresso"])
)
c3.metric(
"Concluídas",
len(df[df["status"] == "Concluído"])
)
 
st.divider()
 
# Kanban
st.subheader("📋 Quadro Kanban")
 
col1, col2, col3, col4, col5 = st.columns(5)
 
status_list = [
"Backlog",
"A Fazer",
"Em Progresso",
"Revisão",
"Concluído"
]
 
cols = [col1, col2, col3, col4, col5]
 
for status, coluna in zip(status_list, cols):
 
with coluna:
st.markdown(f"### {status}")
 
tarefas = df[df["status"] == status]
 
for idx, row in tarefas.iterrows():
 
with st.container(border=True):
 
st.write(f"*{row['titulo']}*")
st.write(f"👤 {row['responsavel']}")
st.write(f"🔥 {row['prioridade']}")
st.write(f"📅 {row['fim']}")
 
novo_status = st.selectbox(
"Mover para",
status_list,
index=status_list.index(status),
key=f"{row['id']}"
)
 
if novo_status != status:
for task in st.session_state.tasks:
if task["id"] == row["id"]:
task["status"] = novo_status
st.rerun()
 
st.divider()
 
# Calendário simplificado
st.subheader("📅 Calendário de Entregas")
 
calendar_df = df[
[
"titulo",
"responsavel",
"inicio",
"fim",
"status"
]
]
 
st.dataframe(
calendar_df,
use_container_width=True
)
 
st.divider()
 
# Equipe
st.subheader("👥 Distribuição da Equipe")
 
count_team = (
df.groupby("responsavel")
.size()
.reset_index(name="atividades")
)
 
st.bar_chart(
count_team.set_index("responsavel")
)
 
st.divider()
 
# Relatório
st.subheader("📈 Resumo do Projeto")
 
concluidas = len(df[df["status"] == "Concluído"])
 
progresso = (
concluidas / max(len(df), 1)
) * 100
 
st.progress(int(progresso))
 
st.write(
f"Projeto concluído: {progresso:.1f}%"
)
