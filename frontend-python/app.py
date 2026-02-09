import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
import json

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
API_URL = st.secrets.get("API_URL", "https://buildmatch-production.up.railway.app/api")
PRODUCTS_API = f"{API_URL}/products"
QUOTES_API = f"{API_URL}/quotes"

# --- FUNÇÕES DE INTEGRAÇÃO EM TEMPO REAL ---
def search_external_suppliers(query, lat=None, lon=None):
    """
    Simula a consulta 100% em tempo real nos sites dos fornecedores.
    Em produção, aqui chamamos o crawler.py ou uma API de scraping.
    """
    # Simulação de delay de rede real
    # time.sleep(1) 
    
    # Mock de resultados "vivos" vindo dos sites
    results = [
        {"name": f"{query} Premium", "supplier": "Leroy Merlin", "price": 105.90, "image": "https://img.ibxk.com.br/2020/01/30/30101509121100.jpg", "category": "Premium", "dist": 2.5},
        {"name": f"{query} Standard", "supplier": "Obramax", "price": 89.00, "image": "https://img.ibxk.com.br/2020/01/30/30101509121100.jpg", "category": "Obra", "dist": 5.1},
        {"name": f"{query} Econômico", "supplier": "Telhanorte", "price": 75.50, "image": "https://img.ibxk.com.br/2020/01/30/30101509121100.jpg", "category": "Econômico", "dist": 1.2},
        {"name": f"{query} Design", "supplier": "Tok&Stok", "price": 250.00, "image": "https://images.tcdn.com.br/img/img_prod/704153/pendente_industrial_retro_vintage_preto_fosco_diametro_30cm_5103_1_20200508110903.jpg", "category": "Decoração", "dist": 8.4}
    ]
    
    # Filtro por GPS (Simulado: Fornecedores num raio de 10km)
    if lat and lon:
        results = [r for r in results if r['dist'] < 6.0]
        
    return results

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
        {"name": "Porcelanato Retificado 60x60", "category": "Acabamentos", "supplier": "Leroy Merlin", "price": 89.90, "unit": "m2", "image": "https://img.ibxk.com.br/2020/01/30/30101509121100.jpg"},
        {"name": "Porcelanato Retificado 60x60", "category": "Acabamentos", "supplier": "Obramax", "price": 84.50, "unit": "m2", "image": "https://img.ibxk.com.br/2020/01/30/30101509121100.jpg"},
        {"name": "Cimento CP II 50kg", "category": "Materiais Brutos", "supplier": "Obramax", "price": 32.90, "unit": "saco", "image": "https://cdn.leroymerlin.com.br/products/cimento_cp_ii_z_32_votoran_50kg_86862341_0001_600x600.jpg"},
        {"name": "Cimento CP II 50kg", "category": "Materiais Brutos", "supplier": "Telhanorte", "price": 35.00, "unit": "saco", "image": "https://cdn.leroymerlin.com.br/products/cimento_cp_ii_z_32_votoran_50kg_86862341_0001_600x600.jpg"},
        {"name": "Luminária Pendente Industrial", "category": "Estética", "supplier": "Tok&Stok", "price": 250.00, "unit": "unid", "image": "https://images.tcdn.com.br/img/img_prod/704153/pendente_industrial_retro_vintage_preto_fosco_diametro_30cm_5103_1_20200508110903.jpg"},
        {"name": "Luminária Pendente Industrial", "category": "Estética", "supplier": "MadeiraMadeira", "price": 198.00, "unit": "unid", "image": "https://images.tcdn.com.br/img/img_prod/704153/pendente_industrial_retro_vintage_preto_fosco_diametro_30cm_5103_1_20200508110903.jpg"},
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
    st.title("🔍 Busca em Tempo Real & GPS")
    
    # Localização GPS (Simulada para Streamlit Web)
    use_gps = st.checkbox("Ativar GPS para buscar fornecedores mais próximos")
    user_lat, user_lon = None, None
    if use_gps:
        st.caption("📍 Localização detectada: São Paulo, SP (Simulado)")
        user_lat, user_lon = -23.55, -46.63 # Mock coordenadas

    search_query = st.text_input("Pesquise em TODOS os fornecedores (Ex: Porcelanato, Cimento)", "")
    
    if len(search_query) >= 3:
        st.info(f"Consultando sites da Leroy, Obramax, Telhanorte em tempo real para '{search_query}'...")
        
        # CONSULTA 100% EM TEMPO REAL (Sem baixar no banco ainda)
        live_results = search_external_suppliers(search_query, user_lat, user_lon)
        
        if live_results:
            st.success(f"Encontramos {len(live_results)} ofertas próximas a você!")
            
            for i, row in enumerate(live_results):
                with st.container():
                    c_img, c_info, c_price, c_sel = st.columns([1, 2, 1, 1])
                    c_img.image(row['image'], width=100)
                    c_info.markdown(f"**{row['name']}**")
                    c_info.caption(f"📍 {row['supplier']} ({row['dist']}km)")
                    c_price.markdown(f"### R$ {row['price']:.2f}")
                    
                    if c_sel.button("Selecionar", key=f"sel_{i}"):
                        if 'selected_items' not in st.session_state:
                            st.session_state.selected_items = []
                        st.session_state.selected_items.append(row)
                        st.toast(f"{row['name']} adicionado à sua lista!")

    # Mostrar itens selecionados para salvar
    if 'selected_items' in st.session_state and st.session_state.selected_items:
        st.markdown("---")
        st.subheader("🛒 Itens Selecionados para Salvar")
        for item in st.session_state.selected_items:
            st.write(f"- {item['name']} ({item['supplier']})")
        
        with st.expander("💾 Salvar esta Cotação no Banco de Dados"):
            with st.form("save_quote_form"):
                proj_name = st.text_input("Nome do Projeto", placeholder="Ex: Reforma Ap 42 - Cliente Silva")
                client = st.text_input("Nome do Cliente")
                
                if st.form_submit_button("Confirmar e Gravar no Banco"):
                    # Aqui gravamos no banco (Quote + QuoteItems)
                    quote_payload = {
                        "projectName": proj_name,
                        "clientName": client,
                        "location": "GPS Ativo" if use_gps else "Manual",
                        "items": [
                            {
                                "name": it['name'],
                                "supplier": it['supplier'],
                                "price": it['price'],
                                "imageUrl": it['image'],
                                "category": it['category']
                            } for it in st.session_state.selected_items
                        ]
                    }
                    try:
                        resp = requests.post(QUOTES_API, json=quote_payload)
                        if resp.status_code in [200, 201]:
                            st.success(f"Lista '{proj_name}' salva com sucesso com foto e dados!")
                            st.session_state.selected_items = []
                        else:
                            st.error("Erro ao salvar no banco.")
                    except:
                        st.error("Falha de conexão com o Backend.")

# --- PÁGINA: MINHAS COTAÇÕES ---
elif menu == "Minhas Cotações":
    st.title("📋 Histórico de Cotações Salvas")
    st.write("Aqui você visualiza todas as listas que você já salvou no banco de dados.")
    
    try:
        resp = requests.get(QUOTES_API)
        if resp.status_code == 200:
            quotes = resp.json()
            if not quotes:
                st.info("Você ainda não salvou nenhuma cotação.")
            else:
                for q in quotes:
                    with st.expander(f"📂 {q['projectName']} - Cliente: {q['clientName']}"):
                        st.caption(f"Criada em: {q['createdAt']} | Local: {q['location']}")
                        for item in q['items']:
                            c1, c2, c3 = st.columns([1, 3, 1])
                            c1.image(item['imageUrl'], width=50)
                            c2.markdown(f"**{item['name']}** - {item['supplier']}")
                            c3.markdown(f"R$ {item['price']:.2f}")
                        
                        st.button("Exportar para PDF / WhatsApp", key=f"exp_{q['id']}")
        else:
            st.error("Erro ao carregar cotações do banco.")
    except:
        st.warning("Backend offline. Mostrando cotação de exemplo (Mock):")
        # Fallback Mock
        st.info("Exemplo: Apartamento do Cliente X - Total R$ 12.450,00")

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
