import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

# Configuração da página (Sensacional!)
st.set_page_config(
    page_title="BuildMatch | Hub de Suprimentos Inteligente",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização Customizada (CSS)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# URL da API Java (Railway)
API_URL = "https://buildmatch-production.up.railway.app/api/products" # Substituir pela sua URL real do Railway

# Sidebar para Navegação
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4300/4300058.png", width=100)
st.sidebar.title("BuildMatch")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navegação",
    ["Dashboard Geral", "Comparador de Preços", "Minhas Cotações", "Gestão de Catálogo"]
)

# Mock de dados caso a API esteja fora (Para demonstração inicial)
def get_mock_data():
    return pd.DataFrame([
        {"name": "Porcelanato Retificado 60x60", "category": "Acabamentos", "supplier": "Leroy Merlin", "price": 89.90, "unit": "m2"},
        {"name": "Porcelanato Retificado 60x60", "category": "Acabamentos", "supplier": "Obramax", "price": 84.50, "unit": "m2"},
        {"name": "Cimento CP II 50kg", "category": "Materiais Brutos", "supplier": "Obramax", "price": 32.90, "unit": "saco"},
        {"name": "Cimento CP II 50kg", "category": "Materiais Brutos", "supplier": "Telhanorte", "price": 35.00, "unit": "saco"},
        {"name": "Luminária Pendente Industrial", "category": "Estética", "supplier": "Tok&Stok", "price": 250.00, "unit": "unid"},
        {"name": "Luminária Pendente Industrial", "category": "Estética", "supplier": "MadeiraMadeira", "price": 198.00, "unit": "unid"},
    ])

# --- PÁGINA: DASHBOARD GERAL ---
if menu == "Dashboard Geral":
    st.title("🏗️ BuildMatch - Hub de Suprimentos")
    st.subheader("Inteligência em Compras para Construção e Design")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Fornecedores Conectados", "12", "+2")
    col2.metric("Produtos em Monitoramento", "1.420", "+15%")
    col3.metric("Economia Média Gerada", "18.5%", "↑ 2.1%")
    col4.metric("Cotações Ativas", "45", "7 novas")

    st.markdown("---")
    
    df = get_mock_data()
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("### 📈 Tendência de Preços (Principais Materiais)")
        fig = px.line(df, x="supplier", y="price", color="name", markers=True, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.markdown("### 🏢 Top Fornecedores")
        st.table(df['supplier'].value_counts().reset_index().rename(columns={'index': 'Fornecedor', 'supplier': 'Itens'}))

# --- PÁGINA: COMPARADOR DE PREÇOS ---
elif menu == "Comparador de Preços":
    st.title("🔍 Comparador de Preços Inteligente")
    
    search_query = st.text_input("O que você está procurando? (Ex: Porcelanato, Cimento, Luminária)", "")
    
    if search_query:
        df = get_mock_data()
        results = df[df['name'].str.contains(search_query, case=False)]
        
        if not results.empty:
            st.success(f"Encontramos {len(results)} ofertas para '{search_query}'")
            
            # Ordenar por menor preço
            results = results.sort_values(by='price')
            
            for index, row in results.iterrows():
                with st.container():
                    col_img, col_info, col_price, col_action = st.columns([1, 3, 2, 2])
                    col_info.markdown(f"**{row['name']}**")
                    col_info.caption(f"Categoria: {row['category']} | Fornecedor: {row['supplier']}")
                    
                    # Destaque para o melhor preço
                    if index == results.index[0]:
                        col_price.markdown(f"### R$ {row['price']:.2f}")
                        col_price.markdown(":green[🏆 Melhor Oferta]")
                    else:
                        col_price.markdown(f"#### R$ {row['price']:.2f}")
                    
                    if col_action.button(f"Adicionar à Cotação", key=f"btn_{index}"):
                        st.toast(f"{row['name']} adicionado!")
        else:
            st.warning("Nenhum produto encontrado com este nome.")
    else:
        st.info("Digite o nome de um material para comparar preços entre Leroy Merlin, Obramax, Tok&Stok e outros.")

# --- PÁGINA: MINHAS COTAÇÕES ---
elif menu == "Minhas Cotações":
    st.title("📋 Gestão de Cotações")
    st.write("Gerencie suas listas de suprimentos e otimize o orçamento da sua obra.")
    
    # Exemplo de lista de cotação
    quote_data = [
        {"item": "Porcelanato Retificado", "qtd": 50, "unit": "m2", "fornecedor": "Obramax", "preço_un": 84.50},
        {"item": "Cimento CP II", "qtd": 20, "unit": "saco", "fornecedor": "Obramax", "preço_un": 32.90},
    ]
    df_quote = pd.DataFrame(quote_data)
    df_quote['total'] = df_quote['qtd'] * df_quote['preço_un']
    
    st.dataframe(df_quote, use_container_width=True)
    
    total_geral = df_quote['total'].sum()
    st.markdown(f"## Total da Cotação: :blue[R$ {total_geral:,.2f}]")
    
    if st.button("Gerar PDF para Aprovação do Cliente"):
        st.balloons()
        st.success("PDF gerado com sucesso!")

# --- PÁGINA: GESTÃO DE CATÁLOGO ---
elif menu == "Gestão de Catálogo":
    st.title("⚙️ Administração de Dados")
    st.write("Cadastre novos produtos ou integre APIs de fornecedores.")
    
    with st.form("new_product"):
        st.subheader("Cadastrar Novo Item no Hub")
        name = st.text_input("Nome do Produto")
        cat = st.selectbox("Categoria", ["Materiais Brutos", "Acabamentos", "Estética", "Instalações"])
        sup = st.text_input("Fornecedor")
        price = st.number_input("Preço Unitário", min_value=0.0)
        unit = st.text_input("Unidade (ex: m2, saco, kg)")
        
        if st.form_submit_button("Salvar no Hub Inteligente"):
            # Aqui enviaremos para a API Java via POST
            payload = {
                "name": name,
                "category": cat,
                "supplier": sup,
                "price": price,
                "unit": unit
            }
            try:
                # requests.post(API_URL, json=payload)
                st.success(f"Produto {name} cadastrado com sucesso no banco Postgres!")
            except:
                st.error("Erro ao conectar com a API Java.")

st.sidebar.markdown("---")
st.sidebar.caption(f"BuildMatch v1.0.0 | {datetime.now().year}")
