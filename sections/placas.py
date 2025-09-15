import streamlit as st
from data.placas_data import get_placas

def formulario_placas(partida_idx):
    st.subheader("🔵 Sección: Placas")

    # Asegurar que existan partidas
    if "partidas" not in st.session_state:
        st.session_state["partidas"] = []

    # Si la partida aún no tiene items, inicializarla
    if len(st.session_state["partidas"]) <= partida_idx:
        st.session_state["partidas"].append({
            "nombre": f"Partida {partida_idx+1}",
            "items": []
        })

    # Para comodidad
    partida = st.session_state["partidas"][partida_idx]
    if "placas" not in partida:
        partida["placas"] = []

    placas = get_placas()
    total_global = 0

    for idx, item in enumerate(partida["placas"]):
        with st.expander(f"📐 Placa {idx+1}", expanded=(idx == len(partida["placas"]) - 1)):
            codigo_placa = st.selectbox(
                f"Selecciona el código de la placa {idx+1}",
                list(placas.keys()),
                key=f"placas_codigo_placa_{partida_idx}_{idx}"
            )
            descripcion, peso = placas[codigo_placa]

            st.write(f"**Descripción:** {descripcion}")
            st.write(f"**Peso teórico por m²:** {peso:.2f} kg/m²")

            # Número de piezas
            num_piezas = st.number_input(
                "Número de piezas", min_value=1, step=1,
                key=f"placas_num_piezas_{partida_idx}_{idx}"
            )

            # Medidas
            medida1_m = st.number_input("Medida placa 1 (m)", format="%.4f", key=f"placas_medida1_m_{partida_idx}_{idx}")
            medida2_m = st.number_input("Medida placa 2 (m)", format="%.4f", key=f"placas_medida2_m_{partida_idx}_{idx}")

            # ============================
            # 💰 Costo del material
            # ============================
            st.markdown("### 💰 Costo del material (por peso)")
            costo_por_kg = st.number_input("Costo por kg del material ($)", key=f"placas_costo_kg_{partida_idx}_{idx}")
            area_m2 = medida1_m * medida2_m if (medida1_m and medida2_m) else 0
            costo_material_total = area_m2 * peso * costo_por_kg if (area_m2 and costo_por_kg) else 0

            # Conversión a pulg²
            st.markdown("### 💵 Costo del material (por pulg²)")
            area_pulg2 = area_m2 * 1550.0031 if area_m2 else 0
            costo_por_pulg2 = (costo_material_total / area_pulg2) if (costo_material_total and area_pulg2) else 0
            if area_pulg2:
                st.info(f"Área total de la placa: {area_pulg2:.2f} pulg²")
            if costo_por_pulg2:
                st.info(f"Costo por pulg²: ${costo_por_pulg2:.2f}")

            # ============================
            # 🛠️ Maquinado convencional
            # ============================
            st.markdown("### 🛠️ Maquinado convencional")
            costo_hora_conve = st.number_input("Costo por hora convencional ($)", key=f"placas_costo_hora_conve_{partida_idx}_{idx}")
            horas_conve = st.number_input("Horas convencionales por pieza", key=f"placas_horas_conve_{partida_idx}_{idx}")
            total_conve = costo_hora_conve * horas_conve
            if total_conve:
                st.success(f"Total convencional por pieza: ${total_conve:.2f}")

            # ============================
            # 🤖 Maquinado CNC
            # ============================
            st.markdown("### 🤖 Maquinado CNC")
            costo_hora_cnc = st.number_input("Costo por hora CNC ($)", key=f"placas_costo_hora_cnc_{partida_idx}_{idx}")
            horas_cnc = st.number_input("Horas CNC por pieza", key=f"placas_horas_cnc_{partida_idx}_{idx}")
            total_cnc = costo_hora_cnc * horas_cnc
            if total_cnc:
                st.success(f"Total CNC por pieza: ${total_cnc:.2f}")

            # ============================
            # 🧪 Tratamiento
            # ============================
            st.markdown("### 🧪 Tratamiento")
            tratamiento_texto = st.text_input("Detalle del tratamiento", key=f"placas_tratamiento_{partida_idx}_{idx}")
            costo_tratamiento = st.number_input("Costo del tratamiento por pieza ($)", key=f"placas_costo_tratamiento_{partida_idx}_{idx}")

            # ============================
            # 💰 Totales
            # ============================
            st.markdown("### 💰 Totales")
            costo_material_unitario = (costo_material_total / num_piezas) if (num_piezas and costo_material_total) else 0
            costo_unitario = costo_material_unitario + total_conve + total_cnc + costo_tratamiento
            costo_total = costo_unitario * num_piezas

            st.success(f"**Costo unitario total (Placa {idx+1}): ${costo_unitario:.2f}**")
            st.success(f"**Costo total (Placa {idx+1}): ${costo_total:.2f}**")

            total_global += costo_total

            # Guardar con botón (guardar o actualizar)
            if st.button(f"💾 Guardar Placa {idx+1}", key=f"placas_guardar_{partida_idx}_{idx}"):
                item_id = f"Placas-{partida_idx}-{idx}"  # ID único por partida y posición
                nuevo_item = {
                    "id": item_id,
                    "Sección": "Placas",
                    "Código": codigo_placa,
                    "Piezas": num_piezas,
                    "Costo unitario": round(costo_unitario, 2),
                    "Costo total": round(costo_total, 2),
                    "Tratamiento": tratamiento_texto  # 👈 si usas tratamiento
                }

                # Buscar si ya existe ese id en la partida
                ids_existentes = [i["id"] for i in partida["items"]]
                if item_id in ids_existentes:
                    # Actualizar existente
                    idx_existente = ids_existentes.index(item_id)
                    partida["items"][idx_existente] = nuevo_item
                    st.success(f"🔄 Placa {idx+1} actualizada en {partida['nombre']}")
                else:
                    # Agregar si no existía
                    partida["items"].append(nuevo_item)
                    st.success(f"✅ Placa {idx+1} agregada a {partida['nombre']}")


            # Botón eliminar
            if st.button(f"❌ Eliminar Placa {idx+1}", key=f"placas_eliminar_{partida_idx}_{idx}"):
                partida["placas"].pop(idx)
                st.rerun()

    # Botón agregar al final
    if st.button("➕ Agregar placa", key=f"placas_agregar_{partida_idx}"):
        partida["placas"].append({})
        st.rerun()

    if partida["placas"]:
        st.markdown(f"## 🔢 Total sección Placas en {partida['nombre']}")
        st.success(f"**Total global de placas: ${total_global:.2f}**")
