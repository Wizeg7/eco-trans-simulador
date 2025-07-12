import streamlit as st
import pandas as pd
import random

# Configuración de la página
st.set_page_config(page_title="EcoTrans - Seguimiento", layout="centered")

# Estilos con fondo funcional (usando data-testid)
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://images.unsplash.com/photo-1549921296-3a6b221bfb2a?auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
    }}

    .main {{
        background-color: rgba(255, 255, 255, 0.93);
        padding: 2rem;
        border-radius: 15px;
        max-width: 850px;
        margin: auto;
    }}

    .title {{
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #ffffff;
        background-color: rgba(0, 0, 0, 0.6);
        padding: 1rem;
        border-radius: 10px;
    }}

    .pedido-card {{
        background-color: #ffffffdd;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }}

    .stButton>button {{
        color: white;
        background-color: #007BFF;
        border-radius: 8px;
        padding: 0.5em 1.2em;
        font-weight: bold;
    }}

    .stButton>button:hover {{
        background-color: #0056b3;
    }}
    </style>
""", unsafe_allow_html=True)

# Iniciar contenedor principal
st.markdown('<div class="main">', unsafe_allow_html=True)

# Título
st.markdown('<div class="title">🚚 EcoTrans Logistic S.A.</div>', unsafe_allow_html=True)
st.markdown('<h5 style="text-align:center;">Simulador de Asignación y Seguimiento de Pedidos</h5>', unsafe_allow_html=True)

# Datos fijos
zonas = {
    "Lima Norte": ["San Martín de Porres", "Los Olivos", "Comas", "Independencia"],
    "Lima Sur": ["Chorrillos", "Villa El Salvador", "Villa María del Triunfo", "San Juan de Miraflores"]
}

repartidores = {
    "Lima Norte": ["José", "Carla"],
    "Lima Sur": ["Andrés", "Luisa"]
}

# Estado de sesión
if "pedidos" not in st.session_state:
    st.session_state.pedidos = []

# Funciones clave
def detectar_zona(distrito):
    for zona, distritos in zonas.items():
        if distrito in distritos:
            return zona
    return "Zona desconocida"

def asignar_repartidor(zona):
    return random.choice(repartidores.get(zona, ["Sin asignar"]))

def avanzar_estado(estado_actual):
    estados = ["Pendiente", "En camino", "Entregado"]
    if estado_actual in estados:
        i = estados.index(estado_actual)
        return estados[i + 1] if i < 2 else "Entregado"
    return "Pendiente"

# Formulario de registro
st.subheader("📦 Registrar nuevo pedido")
with st.form("form_pedido"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("👤 Nombre del cliente")
    with col2:
        distrito = st.selectbox("🌐 Distrito de destino", zonas["Lima Norte"] + zonas["Lima Sur"])
    
    direccion = st.text_input("🏠 Dirección exacta")
    submitted = st.form_submit_button("Registrar pedido")

    if submitted and nombre and direccion:
        zona = detectar_zona(distrito)
        repartidor = asignar_repartidor(zona)
        nuevo_pedido = {
            "Cliente": nombre,
            "Distrito": distrito,
            "Zona": zona,
            "Dirección": direccion,
            "Repartidor": repartidor,
            "Estado": "Pendiente"
        }
        st.session_state.pedidos.append(nuevo_pedido)
        st.success(f"✅ Pedido registrado y asignado a {repartidor} ({zona})")

# Seguimiento de pedidos
st.subheader("📋 Seguimiento de pedidos")
if st.session_state.pedidos:
    for i, pedido in enumerate(st.session_state.pedidos):
        color_estado = {
            "Pendiente": "🟡",
            "En camino": "🟠",
            "Entregado": "🟢"
        }

        st.markdown(f"""
        <div class="pedido-card">
            <h5>{color_estado[pedido['Estado']]} Pedido de {pedido['Cliente']}</h5>
            <p><strong>Zona:</strong> {pedido['Zona']}</p>
            <p><strong>Dirección:</strong> {pedido['Dirección']} - {pedido['Distrito']}</p>
            <p><strong>Repartidor:</strong> {pedido['Repartidor']}</p>
            <p><strong>Estado:</strong> {pedido['Estado']}</p>
        </div>
        """, unsafe_allow_html=True)

        if pedido["Estado"] != "Entregado":
            if st.button(f"➡️ Avanzar estado ({pedido['Cliente']})", key=f"avance_{i}"):
                st.session_state.pedidos[i]["Estado"] = avanzar_estado(pedido["Estado"])
                st.rerun()
else:
    st.info("🕐 Aún no hay pedidos registrados.")

# Cerrar contenedor
st.markdown('</div>', unsafe_allow_html=True)
