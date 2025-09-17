import streamlit as st
import pandas as pd

from sections.placas import formulario_placas
from sections.barras import formulario_barras
from sections.plasticos import formulario_plasticos

# ============================
# ⚙️ Configuración general
# ============================
st.set_page_config(page_title="Cotizador GEMPSA", layout="wide")

# ============================
# 🏭 Header corporativo
# ============================
col_logo, col_title = st.columns([1, 5])

with col_logo:
    st.image("gempsa_logo.png", width=250)  # 👈 Logo visible sí o sí

with col_title:
    st.markdown(
        """
        <div style="background-color:#0a2f5a; padding:1.5rem 2rem; border-radius:0 0 14px 14px;
                    box-shadow:0 4px 12px rgba(0,0,0,0.25);">
            <h1 style="color:white; font-size:5rem; font-weight:1100; margin:0;">
                Cotizador de Maquinados
            </h1>
            <h4 style="color:#e30613; font-size:3.7rem; font-weight:700; margin:0.3rem 0 0 0;">
                GEMPSA
            </h4>
            <div style="margin-top:0.5rem; height:4px; width:50%; background-color:#e30613; border-radius:2px;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================
# 💅 CSS empresarial
# ============================
st.markdown(
    """
    <style>
    /* Hacer que la columna de resumen se quede fija */
    [data-testid="column"]:nth-of-type(2) {
        position: -webkit-sticky !important;
        position: sticky !important;
        top: 1rem;
        align-self: flex-start;
        z-index: 100;
    }
    .resumen-box {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================
# 🗂️ Manejo de partidas
# ============================
if "partidas" not in st.session_state:
    st.session_state["partidas"] = []

# Botón para nueva partida
if st.button("➕ Nueva partida"):
    st.session_state["partidas"].append({"nombre": f"Partida {len(st.session_state['partidas'])+1}", "items": []})
    st.session_state["partida_activa"] = len(st.session_state["partidas"]) - 1
    st.rerun()

if not st.session_state["partidas"]:
    st.info("Crea una partida para comenzar a cotizar.")
    st.stop()

# Selector de partida activa
partida_idx = st.selectbox(
    "Selecciona la partida activa",
    range(len(st.session_state["partidas"])),
    format_func=lambda i: st.session_state["partidas"][i]["nombre"],
    key="partida_selector"
)

partida = st.session_state["partidas"][partida_idx]

# ============================
# 🔘 Botones de acciones sobre la partida
# ============================
c1, c2, c3 = st.columns([1,1,1])

with c1:
    nuevo_nombre = st.text_input("✏️ Renombrar partida", value=partida["nombre"], key=f"rename_{partida_idx}")
    if st.button("Guardar nombre", key=f"save_name_{partida_idx}"):
        partida["nombre"] = nuevo_nombre
        st.rerun()

with c2:
    if st.button("🗑️ Eliminar partida", key=f"delete_{partida_idx}"):
        st.session_state["partidas"].pop(partida_idx)
        if st.session_state["partidas"]:
            st.session_state["partida_activa"] = 0
        else:
            st.session_state["partida_activa"] = None
        st.rerun()

with c3:
    if st.button("📑 Duplicar partida", key=f"duplicate_{partida_idx}"):
        copia = partida.copy()
        copia["nombre"] = f"{partida['nombre']} (copia)"
        st.session_state["partidas"].append(copia)
        st.rerun()

# ============================
# 📐 Layout en dos columnas (2/3 - 1/3)
# ============================
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Paso 1: Selecciona las secciones que deseas cotizar en esta partida:")

    if st.checkbox("➕ Agregar placas", key=f"chk_placas_{partida_idx}"):
        formulario_placas(partida_idx)

    if st.checkbox("➕ Agregar barras", key=f"chk_barras_{partida_idx}"):
        formulario_barras(partida_idx)

    if st.checkbox("➕ Agregar plásticos de ingeniería", key=f"chk_plasticos_{partida_idx}"):
        formulario_plasticos(partida_idx)

    # 👉 Reiniciar partida actual
    if st.button("🧹 Reiniciar partida actual"):
        partida["items"] = []
        partida["placas"] = []
        partida["barras"] = []
        partida["plasticos"] = []
        st.rerun()

with col2:
    st.markdown(f"<div class='resumen-box'>", unsafe_allow_html=True)
    st.markdown(f"### 📊 Resumen de {partida['nombre']}")

    if partida["items"]:
        df = pd.DataFrame(partida["items"])
        df.index = df.index + 1

        total_partida = sum(item["Costo total"] for item in partida["items"])
        st.markdown(
            f"""
            <div style="background-color:#0a2f5a; color:white; padding:20px; border-radius:10px; 
                        text-align:center; font-size:22px; font-weight:bold; margin-bottom:15px;">
                💵 Total {partida['nombre']}: ${total_partida:,.2f}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Mostrar tabla con los ítems
        st.dataframe(df, use_container_width=True)

    else:
        st.info("Aún no has agregado ítems en esta partida.")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================
# 📊 Resumen global
# ============================
st.markdown("## 📊 Resumen global de todas las partidas")

totales = []
for i, p in enumerate(st.session_state["partidas"]):
    total = sum(item["Costo total"] for item in p["items"])
    totales.append({"Partida": p["nombre"], "Total": total})

df_global = pd.DataFrame(totales)
df_global.index = df_global.index + 1

st.table(df_global)

total_global = sum(t["Total"] for t in totales)
st.success(f"**💵 Total global de cotización: ${total_global:,.2f}**")
