import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
import numpy as np

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Passos Mágicos - Datathon",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CORRIGIDO (VISUAL DAS ABAS) ---
st.markdown("""
<style>
    /* Estilo dos Cards de Métricas */
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Títulos */
    h1 { color: #4F46E5; font-family: 'Helvetica', sans-serif; }
    h3 { color: #1f2937; }
    
    /* --- CORREÇÃO DAS ABAS (TABS) --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px; /* Espaço entre as abas */
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F3F4F6; /* Cinza claro para abas inativas */
        color: #374151; /* Texto escuro */
        border-radius: 8px; /* Bordas arredondadas */
        padding: 10px 20px;
        font-weight: 500;
        border: 1px solid #E5E7EB;
    }

    /* Aba Selecionada (Destaque) */
    .stTabs [aria-selected="true"] {
        background-color: #4F46E5 !important; /* Azul Índigo */
        color: #FFFFFF !important; /* Texto Branco */
        font-weight: bold;
        border: 1px solid #4F46E5;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. CARREGAMENTO DE DADOS E MODELO ---
@st.cache_data
def load_data():
    try:
        # Lê o arquivo unificado
        df = pd.read_csv('dados_unificados.csv')
        # Converte ANO para string
        df['ANO'] = df['ANO'].astype(str)
        # Garante números
        cols_num = ['INDE', 'IAA', 'IEG', 'IPS', 'IDA', 'IPP', 'IPV', 'IAN']
        for col in cols_num:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        return df
    except FileNotFoundError:
        st.error("Erro: Arquivo 'dados_unificados.csv' não encontrado. Rode 'preparar_dados.py'.")
        return pd.DataFrame()

df = load_data()

try:
    model = joblib.load('model_v4.pkl')
    scaler = joblib.load('scaler_v3.pkl')
except FileNotFoundError:
    model = None
    scaler = None

# --- 3. SIDEBAR (FILTROS) ---
with st.sidebar:
    st.image("https://passosmagicos.org.br/wp-content/uploads/2023/07/Logo-Passos-Magicos-1.png", use_column_width=True)
    st.header("🔍 Filtros")
    
    anos_disponiveis = sorted(df['ANO'].unique()) if not df.empty else []
    ano_selecionado = st.multiselect("Ano Letivo:", options=anos_disponiveis, default=anos_disponiveis)

    pedras_disponiveis = sorted(df['PEDRA'].unique().astype(str)) if 'PEDRA' in df.columns else []
    pedra_selecionada = st.multiselect("Classificação (Pedra):", options=pedras_disponiveis, default=pedras_disponiveis)

    if not df.empty:
        df_filtrado = df[
            (df['ANO'].isin(ano_selecionado)) & 
            (df['PEDRA'].astype(str).isin(pedra_selecionada))
        ]
    else:
        df_filtrado = pd.DataFrame()

# --- 4. DASHBOARD PRINCIPAL ---
st.title("✨ Monitoramento de Impacto - Passos Mágicos")

if df_filtrado.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros atuais.")
else:
    # --- KPIs ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Alunos", len(df_filtrado))
    with col2:
        media_inde = df_filtrado['INDE'].mean()
        st.metric("Média INDE", f"{media_inde:.2f}")
    with col3:
        alunos_fase = df_filtrado[df_filtrado['IAN'] >= 5].shape[0]
        perc_fase = (alunos_fase / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0
        st.metric("% Fase Adequada", f"{perc_fase:.1f}%")
    with col4:
        topazio = df_filtrado[df_filtrado['PEDRA'].astype(str).str.contains('Topázio', case=False)].shape[0]
        st.metric("Alunos Topázio", topazio)

    st.markdown("---")

    # --- ABAS DE NAVEGAÇÃO ---
    tab1, tab2, tab3 = st.tabs(["📊 Visão Estratégica", "🧠 Análise Multidimensional", "🔮 Simulador & Predição"])

    # === ABA 1: VISÃO ESTRATÉGICA ===
    with tab1:
        col_graf1, col_graf2 = st.columns(2)
        
        with col_graf1:
            st.subheader("Evolução do INDE por Ano")
            fig_box = px.box(df_filtrado, x="ANO", y="INDE", color="ANO", 
                             points="all", title="Distribuição do INDE (2022-2024)",
                             color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_box, use_container_width=True)
            
        with col_graf2:
            st.subheader("Engajamento (IEG) vs. Desempenho (IDA)")
            fig_scatter = px.scatter(df_filtrado, x="IEG", y="IDA", 
                                     color="PEDRA", size="INDE", 
                                     hover_data=['ANO', 'IAN'],
                                     title="Correlação: Esforço x Nota",
                                     color_discrete_sequence=px.colors.qualitative.Bold)
            st.plotly_chart(fig_scatter, use_container_width=True)

        st.subheader("Distribuição de Pedras")
        # Contagem simples para gráfico de barras
        df_count = df_filtrado.groupby(['ANO', 'PEDRA']).size().reset_index(name='Contagem')
        fig_bar = px.bar(df_count, x="ANO", y="Contagem", color="PEDRA", barmode="group",
                         title="Quantidade de Alunos por Pedra e Ano")
        st.plotly_chart(fig_bar, use_container_width=True)

    # === ABA 2: ANÁLISE MULTIDIMENSIONAL (RADAR) ===
    with tab2:
        st.subheader("Raio-X das Dimensões Educacionais")
        st.markdown("Comparativo das dimensões do grupo selecionado.")
        
        categorias = ['IAA', 'IEG', 'IPS', 'IDA', 'IPP', 'IPV', 'IAN']
        
        # Média
        valores_medios = df_filtrado[categorias].mean().values.tolist()
        valores_medios += valores_medios[:1] # Fechar o ciclo
        categorias_radar = categorias + [categorias[0]]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=valores_medios,
            theta=categorias_radar,
            fill='toself',
            name='Média Selecionada',
            line_color='#4F46E5'
        ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=False,
            height=500
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # === ABA 3: SIMULADOR ===
    with tab3:
        st.subheader("🔮 Simulador de Ponto de Virada")
        st.info("Ajuste os indicadores abaixo para prever o sucesso do aluno.")

        if model and scaler:
            c1, c2, c3 = st.columns(3)
            with c1:
                iaa = st.slider("IAA (Autoavaliação)", 0.0, 10.0, 5.0)
                ieg = st.slider("IEG (Engajamento)", 0.0, 10.0, 5.0)
                ips = st.slider("IPS (Psicossocial)", 0.0, 10.0, 5.0)
            with c2:
                ida = st.slider("IDA (Notas)", 0.0, 10.0, 5.0)
                ipp = st.slider("IPP (Psicopedagógico)", 0.0, 10.0, 5.0)
                ipv = st.slider("IPV (Voluntariado)", 0.0, 10.0, 5.0)
            with c3:
                ian = st.slider("IAN (Adequação Nível)", 0.0, 10.0, 5.0)

            if st.button("Calcular Previsão", type="primary"):
                features = np.array([[iaa, ieg, ips, ida, ipp, ipv, ian]])
                features_scaled = scaler.transform(features)
                proba = model.predict_proba(features_scaled)[0][1]
                
                st.divider()
                cr1, cr2 = st.columns([1, 2])
                with cr1:
                    st.metric("Probabilidade", f"{proba:.1%}")
                with cr2:
                    if proba > 0.8:
                        st.success("🌟 **Grande Potencial (Topázio/Ametista)**")
                    elif proba > 0.5:
                        st.warning("⚠️ **Atenção Moderada (Ágata)**")
                    else:
                        st.error("🛑 **Risco Alto (Quartzo)**")
        else:
            st.warning("Modelo não carregado. Treine o modelo primeiro.")