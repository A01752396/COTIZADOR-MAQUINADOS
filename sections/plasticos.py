import streamlit as st
from data.plasticos_data import get_plasticos

def formulario_plasticos(partida_idx):
    st.subheader("🟢 Sección: Plásticos de Ingeniería")

    if "partidas" not in st.session_state:
        st.session_state["partidas"] = []

    if len(st.session_state["partidas"]) <= partida_idx:
        st.session_state["partidas"].append({
            "nombre": f"Partida {partida_idx+1}",
            "items": []
        })

    partida = st.session_state["partidas"][partida_idx]
    if "plasticos" not in partida:
        partida["plasticos"] = []

    plasticos = get_plasticos()
    total_global = 0

    # 🔹 función auxiliar para decimales
    def decimal_input(label, key):
        val = st.text_input(label, key=key)
        try:
            return float(val) if val else 0.0
        except ValueError:
            return 0.0

    for idx, item in enumerate(partida["plasticos"]):
        with st.expander(f"🧱 Plástico {idx+1}", expanded=(idx == len(partida["plasticos"]) - 1)):
            codigo_plastico = st.selectbox(
                f"Selecciona el código del plástico {idx+1}",
                list(plasticos.keys()),
                key=f"plasticos_codigo_plastico_{partida_idx}_{idx}"
            )
            descripcion, peso_m2 = plasticos[codigo_plastico]

            st.write(f"**Descripción:** {descripcion}")
            st.write(f"**Peso por m² (teórico):** {peso_m2:.2f} kg/m²")

            # Número de piezas (entero)
            num_piezas = st.number_input(
                "Número de piezas", min_value=1, step=1,
                key=f"plasticos_num_piezas_{partida_idx}_{idx}"
            )

            # 📐 Datos de la placa base
            st.markdown("### 📐 Datos de la placa base")
            medida1_placa = decimal_input("Medida de la placa (lado 1 en pulgadas)", f"plasticos_medida1_placa_{partida_idx}_{idx}")
            medida2_placa = decimal_input("Medida de la placa (lado 2 en pulgadas)", f"plasticos_medida2_placa_{partida_idx}_{idx}")
            costo_total_placa = decimal_input("Costo total de la placa ($)", f"plasticos_costo_total_placa_{partida_idx}_{idx}")

            if medida1_placa and medida2_placa:
                area_total_pulg2 = medida1_placa * medida2_placa
                st.info(f"Área total de la placa: {area_total_pulg2:.2f} pulg²")

                costo_por_pulg2 = (costo_total_placa / area_total_pulg2) if costo_total_placa else 0
                if costo_por_pulg2:
                    st.info(f"Costo por pulg²: ${costo_por_pulg2:.2f}")
            else:
                costo_por_pulg2 = 0

            # 📏 Dimensiones de la pieza
            st.markdown("### 📏 Dimensiones de la pieza")
            medida1_pieza = decimal_input("Medida pieza 1 (pulgadas)", f"plasticos_medida1_pieza_{partida_idx}_{idx}")
            medida2_pieza = decimal_input("Medida pieza 2 (pulgadas)", f"plasticos_medida2_pieza_{partida_idx}_{idx}")

            if medida1_pieza and medida2_pieza:
                area_pieza_pulg2 = medida1_pieza * medida2_pieza
                st.info(f"Área de la pieza: {area_pieza_pulg2:.2f} pulg²")
            else:
                area_pieza_pulg2 = 0

            if area_pieza_pulg2 and costo_por_pulg2:
                costo_material_unitario = area_pieza_pulg2 * costo_por_pulg2
                costo_material_total = costo_material_unitario * num_piezas
                st.success(f"Costo del material por pieza: ${costo_material_unitario:.2f}")
                st.success(f"Costo total del material ({num_piezas} piezas): ${costo_material_total:.2f}")
            else:
                costo_material_unitario = 0
                costo_material_total = 0

            # 🛠️ Maquinado convencional
            st.markdown("### 🛠️ Maquinado convencional")
            costo_hora_conve = decimal_input("Costo por hora convencional ($)", f"plasticos_costo_hora_conve_{partida_idx}_{idx}")
            horas_conve = decimal_input("Horas convencionales por pieza", f"plasticos_horas_conve_{partida_idx}_{idx}")
            total_conve = costo_hora_conve * horas_conve

            # 🤖 Maquinado CNC
            st.markdown("### 🤖 Maquinado CNC")
            costo_hora_cnc = decimal_input("Costo por hora CNC ($)", f"plasticos_costo_hora_cnc_{partida_idx}_{idx}")
            horas_cnc = decimal_input("Horas CNC por pieza", f"plasticos_horas_cnc_{partida_idx}_{idx}")
            total_cnc = costo_hora_cnc * horas_cnc

            # 🧪 Tratamiento
            st.markdown("### 🧪 Tratamiento")
            tratamiento_texto = st.text_input("Detalle del tratamiento", key=f"plasticos_tratamiento_{partida_idx}_{idx}")
            costo_tratamiento = decimal_input("Costo del tratamiento por pieza ($)", f"plasticos_costo_tratamiento_{partida_idx}_{idx}")

            # 💰 Totales
            st.markdown("### 💰 Totales")
            costo_unitario = costo_material_unitario + total_conve + total_cnc + costo_tratamiento
            costo_total = costo_unitario * num_piezas

            st.success(f"**Costo unitario total (Plástico {idx+1}): ${costo_unitario:.2f}**")
            st.success(f"**Costo total (Plástico {idx+1}): ${costo_total:.2f}**")

            total_global += costo_total

            # Guardar o actualizar item
            if st.button(f"💾 Guardar Plástico {idx+1}", key=f"plasticos_guardar_{partida_idx}_{idx}"):
                item_id = f"Plasticos-{partida_idx}-{idx}"
                nuevo_item = {
                    "id": item_id,
                    "Sección": "Plásticos",
                    "Código": codigo_plastico,
                    "Piezas": num_piezas,
                    "Costo unitario": round(costo_unitario, 2),
                    "Costo total": round(costo_total, 2),
                    "Tratamiento": tratamiento_texto
                }

                ids_existentes = [i["id"] for i in partida["items"]]
                if item_id in ids_existentes:
                    idx_existente = ids_existentes.index(item_id)
                    partida["items"][idx_existente] = nuevo_item
                    st.success(f"🔄 Plástico {idx+1} actualizado en {partida['nombre']}")
                else:
                    partida["items"].append(nuevo_item)
                    st.success(f"✅ Plástico {idx+1} agregado a {partida['nombre']}")

            # Botón eliminar
            if st.button(f"❌ Eliminar Plástico {idx+1}", key=f"plasticos_eliminar_{partida_idx}_{idx}"):
                partida["plasticos"].pop(idx)
                st.rerun()

    if st.button("➕ Agregar otro plástico", key=f"plasticos_agregar_{partida_idx}"):
        partida["plasticos"].append({})
        st.rerun()

    if partida["plasticos"]:
        st.markdown(f"## 🔢 Total sección Plásticos en {partida['nombre']}")
        st.success(f"**Total global de plásticos: ${total_global:.2f}**")
