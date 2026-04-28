# %%
import streamlit as st
import pandas as pd
import plotly.express as px

# %%
# 1. Configuração da Página (Deve ser a primeira linha de comando Streamlit)
st.set_page_config(page_title="Dashboard - Retroagem Laudos", layout="wide")

# 2. Carregamento dos Dados
# Carregando o arquivo em excel
df_fertilidade = pd.read_excel("status.xlsx", sheet_name='FERTILIDADE')
df_carbono = pd.read_excel("status.xlsx", sheet_name='ESTOQUE_CARBONO')

for df, nome in [(df_fertilidade, 'FERTILIDADE'), (df_carbono, 'CARBONO')]:
    df['LAUDO'] = nome

dfs_list = [df_fertilidade, df_carbono]

dfs = pd.concat(dfs_list)
dfs.columns = dfs.columns.str.strip()

# %%

# ==== BARRA LATERAL DE FILTROS ====

st.sidebar.header("Filtros")
anos = dfs['ANO'].unique().tolist()
ano_selecionado = st.sidebar.multiselect("Selecione o ano", anos, default=anos)

df_ano = dfs[dfs['ANO'].isin(ano_selecionado)]

st.title("📊 Retroagem Laudos")

# ==== PROCESSAMENTO MÉTRICAS ====
contagem_os_LAUDO = df_ano['LAUDO'].value_counts()
resumo_status = df_ano.groupby(['LAUDO', 'STATUS']).size()

col1, col2 = st.columns(2, border=True)

with col2:
    st.header("Fertilidade")

    total_fert = contagem_os_LAUDO.get('FERTILIDADE', 0)
    ok_fert = resumo_status.get(('FERTILIDADE', 'OK'), 0)
    tratar_fert = resumo_status.get(('FERTILIDADE', 'TRATAR'), 0)
    retroagir_fert = resumo_status.get(('FERTILIDADE', 'RETROAGIR'), 0)

    perc_fert = (ok_fert/total_fert * 100) if total_fert > 0 else 0

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total OS", total_fert)
    m2.metric("Ok", ok_fert)
    m3.metric("Tratar", tratar_fert)
    m4.metric("Retroagir", retroagir_fert)
    m5.metric("Desempenho", f"{perc_fert:.0f}%")

with col1:
    st.header("Carbono")

    total_carbono = contagem_os_LAUDO.get("CARBONO", 0)
    ok_carbono = resumo_status.get(('CARBONO', 'OK'), 0)
    tratar_carbono = resumo_status.get(('CARBONO', 'TRATAR'), 0)
    retroagir_carbono = resumo_status.get(('CARBONO', 'RETROAGIR'), 0)

    perc_carbono = (ok_carbono/total_carbono * 100) if total_carbono > 0 else 0

    n1, n2, n3, n4, n5 = st.columns(5)
    n1.metric("Total OS", total_carbono)
    n2.metric("Ok", ok_carbono)
    n3.metric("Tratar", tratar_fert)
    n4.metric("Retroagir", retroagir_carbono)
    n5.metric("Desempenho", f"{perc_carbono:.0f}%")

st.markdown("---")

# Agrupamos por ANO, LAUDO e STATUS
df_grafico = df_ano.groupby(['ANO', 'LAUDO', 'STATUS']).size().reset_index(name='QUANTIDADE')
    
fig_barra = px.bar(
    df_grafico,
    x="ANO",
    y="QUANTIDADE",
    color="STATUS",
    facet_col="LAUDO",
    text_auto=True,
    barmode="group",
    color_discrete_map={
        'OK': '#2ecc71',
        'TRATAR': '#f1c40f',
        'RETROAGIR': '#e74c3c'
    },
    template="plotly_white",
    height=400
)

fig_barra.update_layout(
    xaxis_title='Ano',
    yaxis_title='Quantidade de OS',
    legend_title='Status'
)
fig_barra.update_xaxes(matches='x')
st.plotly_chart(fig_barra, use_container_width=True)