import streamlit as st
from data.barras_data import get_barras

def formulario_barras(partida_idx):
    st.subheader("🔵 Sección: Barras")

    # Asegurar que existan partidas
    if "partidas" not in st.session_state:
        st.session_state["partidas"] = []

    # Si la partida aún no existe, inicializarla
    if len(st.session_state["partidas"]) <= partida_idx:
        st.session_state["partidas"].append({
            "nombre": f"Partida {partida_idx+1}",
            "items": []
        })

    partida = st.session_state["partidas"][partida_idx]
    if "barras" not in partida:
        partida["barras"] = []

    barras = get_barras()
    total_global = 0

    for idx, item in enumerate(partida["barras"]):
        with st.expander(f"🔩 Barra {idx+1}", expanded=(idx == len(partida["barras"]) - 1)):
            codigo_barra = st.selectbox(
                f"Selecciona el código de la barra {idx+1}",
                list(barras.keys()),
                key=f"barras_codigo_barra_{partida_idx}_{idx}"
            )
            descripcion, peso_metro = barras[codigo_barra]

            st.write(f"**Descripción:** {descripcion}")
            st.write(f"**Peso por metro:** {peso_metro} kg/m")

            num_piezas = st.number_input(
                "Número de piezas", min_value=1, step=1,
                key=f"barras_num_piezas_{partida_idx}_{idx}"
            )

            longitud_pieza = st.number_input(
                "Longitud de cada pieza (m)",
                key=f"barras_longitud_{partida_idx}_{idx}",
                min_value=0.0,
                step=0.01,
                format="%.6f"
            )

            costo_por_kg = st.number_input(
                "Costo por kilogramo ($)",
                key=f"barras_costo_kg_{partida_idx}_{idx}",
                min_value=0.0,
                step=0.01,
                format="%.6f"
            )

            # Maquinado convencional
            st.markdown("### 🛠️ Maquinado convencional")
            costo_hora_conve = st.number_input(
                "Costo por hora convencional ($)",
                key=f"barras_costo_hora_conve_{partida_idx}_{idx}",
                min_value=0.0,
                step=0.01,
                format="%.6f"
            )
            horas_conve = st.number_input(
                "Horas convencionales por pieza",
                key=f"barras_horas_conve_{partida_idx}_{idx}",
                min_value=0.0,
                step=0.01,
                format="%.6f"
            )

            # Maquinado CNC
            st.markdown("### 🤖 Maquinado CNC")
            costo_hora_cnc = st.number_input(
                "Costo por hora CNC ($)",
                key=f"barras_costo_hora_cnc_{partida_idx}_{idx}",
                min_value=0.0,
                step=0.01,
                format="%.6f"
            )
            horas_cnc = st.number_input(
                "Horas CNC por pieza",
                key=f"barras_horas_cnc_{partida_idx}_{idx}",
                min_value=0.0,
                step=0.01,
                format="%.6f"
            )

            # Tratamiento
            st.markdown("### 🧪 Tratamiento")
            tratamiento_texto = st.text_input(
                "Detalle del tratamiento",
                key=f"barras_tratamiento_{partida_idx}_{idx}"
            )
            costo_tratamiento = st.number_input(
                "Costo del tratamiento por pieza ($)",
                key=f"barras_costo_tratamiento_{partida_idx}_{idx}",
                min_value=0.0,
                step=0.01,
                format="%.6f"
            )

            # Totales
            st.markdown("### 💰 Totales")
            costo_unitario = costo_material_unitario + total_conve + total_cnc + costo_tratamiento
            costo_total = costo_unitario * num_piezas

            st.success(f"**Costo unitario total (Barra {idx+1}): ${costo_unitario:.2f}**")
            st.success(f"**Costo total (Barra {idx+1}): ${costo_total:.2f}**")

            total_global += costo_total

            # ==========================
            # Guardar o actualizar item
            # ==========================
            if st.button(f"💾 Guardar Barra {idx+1}", key=f"barras_guardar_{partida_idx}_{idx}"):
                item_id = f"Barras-{partida_idx}-{idx}"  # ID único
                nuevo_item = {
                    "id": item_id,
                    "Sección": "Barras",
                    "Código": codigo_barra,
                    "Piezas": num_piezas,
                    "Costo unitario": round(costo_unitario, 2),
                    "Costo total": round(costo_total, 2),
                    "Tratamiento": tratamiento_texto
                }

                ids_existentes = [i["id"] for i in partida["items"]]
                if item_id in ids_existentes:
                    idx_existente = ids_existentes.index(item_id)
                    partida["items"][idx_existente] = nuevo_item
                    st.success(f"🔄 Barra {idx+1} actualizada en {partida['nombre']}")
                else:
                    partida["items"].append(nuevo_item)
                    st.success(f"✅ Barra {idx+1} agregada a {partida['nombre']}")

            # Botón eliminar
            if st.button(f"❌ Eliminar Barra {idx+1}", key=f"barras_eliminar_{partida_idx}_{idx}"):
                partida["barras"].pop(idx)
                st.rerun()

    # Botón agregar al final
    if st.button("➕ Agregar barra", key=f"barras_agregar_{partida_idx}"):
        partida["barras"].append({})
        st.rerun()

    if partida["barras"]:
        st.markdown(f"## 🔢 Total sección Barras en {partida['nombre']}")
        st.success(f"**Total global de barras: ${total_global:.2f}**")
