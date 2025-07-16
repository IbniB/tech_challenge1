import os
import streamlit as st
import requests
from dotenv import load_dotenv
from tech_challenge1.core.settings import settings

load_dotenv()
st.set_page_config("Dashboard - Books API")

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")
LOGIN = {"username": settings.DASHBOARD_USER, "password": settings.DASHBOARD_PASSWORD}

# Autenticação
auth = requests.post(
    f"{API_BASE}/api/v1/auth/login",
    data=LOGIN,
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)
token = auth.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

st.title("📊 Dashboard - Books API")

# 🚀 Features
with st.expander("1️⃣ Features disponíveis", expanded=True):
    feats = requests.get(f"{API_BASE}/api/v1/ml/features", headers=headers)
    feats.raise_for_status()
    st.write(feats.json()["features"])

# 📈 Estatísticas
col_over, col_cat, col_top = st.columns(3)
with col_over:
    st.subheader("Overview")
    if st.button("Carregar Overview", key="btn_overview"):
        ov = requests.get(f"{API_BASE}/api/v1/stats/overview", headers=headers); ov.raise_for_status()
        st.json(ov.json())
with col_cat:
    st.subheader("Por Categoria")
    if st.button("Carregar por Categoria", key="btn_cat"):
        sc = requests.get(f"{API_BASE}/api/v1/stats/categories", headers=headers); sc.raise_for_status()
        st.dataframe(sc.json())
with col_top:
    st.subheader("Top Rated")
    if st.button("Carregar Top Rated", key="btn_top"):
        tr = requests.get(f"{API_BASE}/api/v1/stats/top-rated", headers=headers); tr.raise_for_status()
        st.dataframe(tr.json())

# 📚 Livros
with st.expander("📚 Todos os Livros", expanded=False):
    if st.button("Carregar Livros", key="btn_books"):
        bs = requests.get(f"{API_BASE}/api/v1/books", headers=headers); bs.raise_for_status()
        st.dataframe(bs.json())

# 🔎 Buscar Livros
with st.expander("🔎 Buscar Livros", expanded=True):
    col1, col2 = st.columns(2)
    title = col1.text_input("Título", key="search_title")
    category = col2.text_input("Categoria", key="search_category")
    if st.button("Buscar", key="search_btn"):
        params = {}
        if title:    params["title"]    = title
        if category: params["category"] = category
        resp = requests.get(f"{API_BASE}/api/v1/books/search", params=params)
        resp.raise_for_status()
        st.dataframe(resp.json())

# 🤖 ML & Predição
with st.expander("🤖 Dados de Treino ML"):
    if st.button("Carregar Training Data", key="btn_td"):
        td = requests.get(f"{API_BASE}/api/v1/ml/training-data", headers=headers); td.raise_for_status()
        st.json(td.json())

with st.expander("🔮 Fazer Predição", expanded=False):
    col1, col2, col3 = st.columns([1,1,1])
    price     = col1.number_input("Price", 0.0, key="pred_price")
    rating    = col2.number_input("Rating", 0.0, key="pred_rating")
    category_in = col3.text_input("Categoria", key="pred_category")
    avail       = col3.selectbox("Disponível?", [0,1], key="pred_avail")
    if st.button("Prever", key="predict_btn"):
        payload = {
            "price": price,
            "rating": rating,
            "category": category_in,
            "availability": avail
        }
        p = requests.post(f"{API_BASE}/api/v1/ml/predictions", headers=headers, json=payload)
        p.raise_for_status()
        st.success(f"Predição: {p.json()['prediction']}")

# 📊 Métricas
with st.expander("📊 Métricas Prometheus"):
    m = requests.get(f"{API_BASE}/api/v1/metrics"); m.raise_for_status()
    st.text(m.text)

# 📝 Logs
with st.expander("📝 Últimos Logs"):
    lr = requests.get(f"{API_BASE}/api/v1/logs", headers=headers); lr.raise_for_status()
    for line in lr.json()["logs"]:
        st.text(line)