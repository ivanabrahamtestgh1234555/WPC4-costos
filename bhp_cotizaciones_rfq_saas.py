import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BHP ENC-3430 | Portal de Cotizaciones y Gestión de Proveedores",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .status-badge-done {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
    }
    .status-badge-pending {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION FOR DYNAMIC DATA
# -----------------------------------------------------------------------------
if "equipos_db" not in st.session_state:
    initial_equipos = [
        {"ID": "EQ-001", "Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Equipos Mayores", "Equipo": "Switchgear GIS 245 kV (Suministro y Montaje)", "Cantidad": 1.0, "Unidad": "Gl", "Presupuesto_USD": 14500000.0, "Cotizado": True, "Fecha": "2026-09-15", "Proveedor_Lider": "Hitachi Energy"},
        {"ID": "EQ-002", "Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Equipos Mayores", "Equipo": "Transformador de Poder 220/33 kV (125 MVA)", "Cantidad": 3.0, "Unidad": "c/u", "Presupuesto_USD": 11400000.0, "Cotizado": True, "Fecha": "2026-09-20", "Proveedor_Lider": "Siemens Energy"},
        {"ID": "EQ-003", "Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Equipos Mayores", "Equipo": "Ductos de Barras GIL 220 kV (Conexión GIS-Trafo)", "Cantidad": 1.0, "Unidad": "Gl", "Presupuesto_USD": 3200000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "EQ-004", "Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Infraestructura", "Equipo": "Galpón Prefabricado GIS (31,5x22,7x14 m)", "Cantidad": 1.0, "Unidad": "Gl", "Presupuesto_USD": 1850000.0, "Cotizado": True, "Fecha": "2026-10-01", "Proveedor_Lider": "Cintec / Resa"},
        {"ID": "EQ-005", "Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Salas Eléctricas", "Equipo": "Sala Prefabricada SS/GG y Control (ERoom)", "Cantidad": 1.0, "Unidad": "Gl", "Presupuesto_USD": 1200000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "EQ-006", "Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Equipos Auxiliares", "Equipo": "Grupo Generador Emergencia MT (4,16 kV - 2.750 kVA)", "Cantidad": 1.0, "Unidad": "c/u", "Presupuesto_USD": 950000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "EQ-007", "Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Equipos Auxiliares", "Equipo": "Subestaciones Unitarias 7,5 MVA (33/4,16 kV)", "Cantidad": 3.0, "Unidad": "c/u", "Presupuesto_USD": 1260000.0, "Cotizado": True, "Fecha": "2026-10-05", "Proveedor_Lider": "WEG Chile"},
        {"ID": "EQ-008", "Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Equipos Auxiliares", "Equipo": "Resistencia Puesta a Tierra NGR y Auxiliares", "Cantidad": 3.0, "Unidad": "c/u", "Presupuesto_USD": 255000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        
        {"ID": "EQ-009", "Area": "S/E Monte Mina 220 kV (AIS)", "Categoria": "Equipos Mayores", "Equipo": "Interruptor Tanque Muerto SF6 220 kV 3150A 50kA", "Cantidad": 3.0, "Unidad": "c/u", "Presupuesto_USD": 660000.0, "Cotizado": True, "Fecha": "2026-09-18", "Proveedor_Lider": "Hitachi Energy"},
        {"ID": "EQ-010", "Area": "S/E Monte Mina 220 kV (AIS)", "Categoria": "Equipos Mayores", "Equipo": "Transformador de Potencial Capacitivo (TPC) 220 kV", "Cantidad": 10.0, "Unidad": "c/u", "Presupuesto_USD": 420000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "EQ-011", "Area": "S/E Monte Mina 220 kV (AIS)", "Categoria": "Equipos Mayores", "Equipo": "Desconectador Tripolar Apertura Central 220 kV", "Cantidad": 10.0, "Unidad": "c/u", "Presupuesto_USD": 394000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "EQ-012", "Area": "S/E Monte Mina 220 kV (AIS)", "Categoria": "Cables Subterráneos", "Equipo": "Cable Aislado XLPE 220 kV 3000 mm²", "Cantidad": 1800.0, "Unidad": "m", "Presupuesto_USD": 810000.0, "Cotizado": True, "Fecha": "2026-09-28", "Proveedor_Lider": "Prysmian Group"},
        {"ID": "EQ-013", "Area": "S/E Monte Mina 220 kV (AIS)", "Categoria": "Cables Subterráneos", "Equipo": "Mufas de Transición Aire/Cable XLPE 220 kV", "Cantidad": 12.0, "Unidad": "c/u", "Presupuesto_USD": 420000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        
        {"ID": "EQ-014", "Area": "Línea Transmisión 2x220 kV", "Categoria": "Estructuras LAT", "Equipo": "Torres Suspensión Reticuladas 22AD.1M3 (66 Torres)", "Cantidad": 662580.0, "Unidad": "kg", "Presupuesto_USD": 2782836.0, "Cotizado": True, "Fecha": "2026-09-12", "Proveedor_Lider": "Metalúrgica SAE"},
        {"ID": "EQ-015", "Area": "Línea Transmisión 2x220 kV", "Categoria": "Estructuras LAT", "Equipo": "Torres Anclaje/Remate 22CD/22DD (18 Torres)", "Cantidad": 372300.0, "Unidad": "kg", "Presupuesto_USD": 1675350.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "EQ-016", "Area": "Línea Transmisión 2x220 kV", "Categoria": "Conductores", "Equipo": "Conductor de Fase AAAC Flint 740.8 MCM (25.7 km)", "Cantidad": 312000.0, "Unidad": "m", "Presupuesto_USD": 4524000.0, "Cotizado": True, "Fecha": "2026-09-25", "Proveedor_Lider": "Prysmian / General Cable"},
        {"ID": "EQ-017", "Area": "Línea Transmisión 2x220 kV", "Categoria": "Conductores", "Equipo": "Cable de Guardia OPGW 24 Fibras Ópticas", "Cantidad": 27000.0, "Unidad": "m", "Presupuesto_USD": 229500.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "EQ-018", "Area": "Línea Transmisión 2x220 kV", "Categoria": "Accesorios LAT", "Equipo": "Cadenas de Aisladores Poliméricos 220 kV", "Cantidad": 504.0, "Unidad": "Juego", "Presupuesto_USD": 428400.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"}
    ]
    st.session_state.equipos_db = pd.DataFrame(initial_equipos)

if "vendedores_db" not in st.session_state:
    initial_vendedores = [
        {"ID": "EQ-001", "Equipo": "Switchgear GIS 245 kV", "Empresa": "Hitachi Energy (ABB)", "Precio_USD": 14500000.0, "Lead_Time_Meses": 14, "Garantia_Años": 3, "Estado": "Adjudicada Base"},
        {"ID": "EQ-001", "Equipo": "Switchgear GIS 245 kV", "Empresa": "Siemens Energy", "Precio_USD": 15200000.0, "Lead_Time_Meses": 15, "Garantia_Años": 2, "Estado": "En Evaluación"},
        {"ID": "EQ-001", "Equipo": "Switchgear GIS 245 kV", "Empresa": "GE Vernova", "Precio_USD": 14850000.0, "Lead_Time_Meses": 14, "Garantia_Años": 2, "Estado": "En Evaluación"},
        {"ID": "EQ-002", "Equipo": "Transformador de Poder 220/33 kV (125 MVA)", "Empresa": "Siemens Energy", "Precio_USD": 3800000.0, "Lead_Time_Meses": 12, "Garantia_Años": 3, "Estado": "Adjudicada Base"},
        {"ID": "EQ-002", "Equipo": "Transformador de Poder 220/33 kV (125 MVA)", "Empresa": "Hitachi Energy", "Precio_USD": 3950000.0, "Lead_Time_Meses": 13, "Garantia_Años": 2, "Estado": "En Evaluación"},
        {"ID": "EQ-002", "Equipo": "Transformador de Poder 220/33 kV (125 MVA)", "Empresa": "Hyundai Electric", "Precio_USD": 3650000.0, "Lead_Time_Meses": 11, "Garantia_Años": 2, "Estado": "En Evaluación"},
        {"ID": "EQ-012", "Equipo": "Cable Aislado XLPE 220 kV 3000 mm²", "Empresa": "Prysmian Group", "Precio_USD": 450.0, "Lead_Time_Meses": 8, "Garantia_Años": 5, "Estado": "Adjudicada Base"},
        {"ID": "EQ-012", "Equipo": "Cable Aislado XLPE 220 kV 3000 mm²", "Empresa": "Nexans", "Precio_USD": 475.0, "Lead_Time_Meses": 9, "Garantia_Años": 5, "Estado": "En Evaluación"},
        {"ID": "EQ-016", "Equipo": "Conductor de Fase AAAC Flint 740.8 MCM", "Empresa": "Prysmian / General Cable", "Precio_USD": 14.50, "Lead_Time_Meses": 6, "Garantia_Años": 3, "Estado": "Adjudicada Base"},
        {"ID": "EQ-016", "Equipo": "Conductor de Fase AAAC Flint 740.8 MCM", "Empresa": "Midal Cables", "Precio_USD": 13.90, "Lead_Time_Meses": 7, "Garantia_Años": 2, "Estado": "En Evaluación"}
    ]
    st.session_state.vendedores_db = pd.DataFrame(initial_vendedores)

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.markdown("## BHP ENC-3430")
st.sidebar.markdown("**Portal de Cotizaciones y Licitationes**")
st.sidebar.markdown("---")

module = st.sidebar.radio(
    "Navegación:",
    [
        "📊 Dashboard de Cotizaciones & RFQ",
        "✅ Checklist de Cotizados (Ticket)",
        "🏢 Cuadro Comparativo por Empresa",
        "📦 Base de Datos Maestra de Equipos",
        "📤 Exportar Reportes de Licitación"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 BHP | Supply Chain & Procurement - ENC-3430")

# -----------------------------------------------------------------------------
# MODULE 1: DASHBOARD DE COTIZACIONES Y RFQ
# -----------------------------------------------------------------------------
if module == "📊 Dashboard de Cotizaciones & RFQ":
    st.markdown('<div class="main-header">Control Ejecutivo de Cotizaciones y Licitationes (RFQ)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Estado de Avance de Compras y Cotizaciones Pendientes - Proyecto ENC-3430</div>', unsafe_allow_html=True)

    df_eq = st.session_state.equipos_db
    
    total_equipos = len(df_eq)
    cotizados_count = len(df_eq[df_eq["Cotizado"] == True])
    pendientes_count = total_equipos - cotizados_count
    pct_avance = (cotizados_count / total_equipos) * 100.0 if total_equipos > 0 else 0.0

    monto_total_presup = df_eq["Presupuesto_USD"].sum()
    monto_cotizado = df_eq[df_eq["Cotizado"] == True]["Presupuesto_USD"].sum()
    monto_pendiente = monto_total_presup - monto_cotizado

    # Top KPI Cards
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Total Equipos por Cotizar", f"{total_equipos} Ítems")
    with k2:
        st.metric("Equipos Cotizados ✅", f"{cotizados_count} Ítems", delta=f"{pct_avance:.1f}% del total")
    with k3:
        st.metric("Cotizaciones Pendientes ⏳", f"{pendientes_count} Ítems", delta=f"-{100-pct_avance:.1f}% pendiente", delta_color="inverse")
    with k4:
        st.metric("Monto Cotizado (USD)", f"${monto_cotizado/1e6:,.2f} M")
    with k5:
        st.metric("Monto Pendiente (USD)", f"${monto_pendiente/1e6:,.2f} M")

    st.markdown("---")

    # Donut Chart & Bar Chart
    c1, c2 = st.columns([4, 6])
    with c1:
        st.subheader("Estado Global de Licitación (RFQ)")
        fig_donut = px.pie(
            names=["Cotizados ✅", "Pendientes ⏳"],
            values=[cotizados_count, pendientes_count],
            color=["Cotizados ✅", "Pendientes ⏳"],
            color_discrete_map={"Cotizados ✅": "#10B981", "Pendientes ⏳": "#EF4444"},
            hole=0.45
        )
        fig_donut.update_layout(height=360, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_donut, use_container_width=True)

    with c2:
        st.subheader("Equipos Cotizados vs. Pendientes por Área")
        area_summary = df_eq.groupby(["Area", "Cotizado"]).size().reset_index(name="Cantidad")
        area_summary["Estado"] = area_summary["Cotizado"].map({True: "Cotizado ✅", False: "Pendiente ⏳"})
        
        fig_bar = px.bar(
            area_summary,
            x="Area",
            y="Cantidad",
            color="Estado",
            color_discrete_map={"Cotizado ✅": "#10B981", "Pendiente ⏳": "#EF4444"},
            barmode="stack",
            text_auto=True
        )
        fig_bar.update_layout(height=360, xaxis_title="Instalación", yaxis_title="N° de Equipos")
        st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------------------------------------------------------
# MODULE 2: CHECKLIST DE COTIZADOS (TICKET)
# -----------------------------------------------------------------------------
elif module == "✅ Checklist de Cotizados (Ticket)":
    st.markdown('<div class="main-header">Checklist Interactivo de Cotizaciones de Equipamiento</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Marque con el Ticket (✅) los equipos cuya cotización haya sido recibida o adjudicada</div>', unsafe_allow_html=True)

    # Filter selector
    filter_area = st.selectbox("Filtrar por Área de Proyecto:", ["Todas las Áreas"] + list(st.session_state.equipos_db["Area"].unique()))
    
    df_view = st.session_state.equipos_db.copy()
    if filter_area != "Todas las Áreas":
        df_view = df_view[df_view["Area"] == filter_area]

    st.markdown("#### Lista de Equipos y Control de Estado de Licitación:")
    
    # Interactive checklist table using data_editor or checkboxes
    for idx, row in df_view.iterrows():
        c_check, c_info, c_supplier, c_date = st.columns([1.5, 5.5, 3, 2])
        
        # Unique key for checkboxes
        chk_key = f"chk_{row['ID']}"
        
        is_checked = c_check.checkbox(
            f"✅ {row['ID']}",
            value=bool(row["Cotizado"]),
            key=chk_key
        )
        
        # Update session state if checkbox changed
        if is_checked != bool(row["Cotizado"]):
            st.session_state.equipos_db.loc[st.session_state.equipos_db["ID"] == row["ID"], "Cotizado"] = is_checked
            if is_checked:
                st.session_state.equipos_db.loc[st.session_state.equipos_db["ID"] == row["ID"], "Fecha"] = pd.Timestamp.now().strftime("%Y-%m-%d")
            else:
                st.session_state.equipos_db.loc[st.session_state.equipos_db["ID"] == row["ID"], "Fecha"] = "-"
                st.session_state.equipos_db.loc[st.session_state.equipos_db["ID"] == row["ID"], "Proveedor_Lider"] = "Pendiente"
            st.rerun()

        with c_info:
            st.markdown(f"**{row['Equipo']}** ({row['Area']})")
            st.caption(f"Categoría: {row['Categoria']} | Cantidad: {row['Cantidad']:,.1f} {row['Unidad']} | Presupuesto: ${row['Presupuesto_USD']:,.2f} USD")

        with c_supplier:
            if is_checked:
                st.success(f"Proveedor: {row['Proveedor_Lider']}")
            else:
                st.error("⏳ Pendiente de Cotización")

        with c_date:
            st.write(f"Fecha: `{row['Fecha']}`")

        st.markdown("<hr style='margin: 4px 0px;'>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MODULE 3: CUADRO COMPARATIVO POR EMPRESA
# -----------------------------------------------------------------------------
elif module == "🏢 Cuadro Comparativo por Empresa":
    st.markdown('<div class="main-header">Tabla Comparativa de Empresas Cotizantes</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Gestión de Ofertas por Proveedor y Adquisiciones del Proyecto</div>', unsafe_allow_html=True)

    col_select, col_add = st.columns([5, 5])

    with col_select:
        st.subheader("1. Seleccionar Equipamiento por Analizar")
        equipo_lista = st.session_state.equipos_db["Equipo"].unique()
        selected_eq_name = st.selectbox("Seleccionar Equipo / Suministro:", equipo_lista)
        
        # Retrieve Equipment Details
        eq_row = st.session_state.equipos_db[st.session_state.equipos_db["Equipo"] == selected_eq_name].iloc[0]
        eq_id = eq_row["ID"]
        
        st.info(f"**ID:** {eq_id} | **Área:** {eq_row['Area']} | **Presupuesto Est.:** ${eq_row['Presupuesto_USD']:,.2f} USD")

    with col_add:
        st.subheader("2. Agregar Nueva Empresa Cotizante")
        with st.form("form_add_vendor", clear_on_submit=True):
            v_empresa = st.text_input("Nombre de Empresa / Proveedor:")
            v_precio = st.number_input("Precio Oferta ($USD):", min_value=0.0, value=float(eq_row["Presupuesto_USD"]), step=5000.0)
            v_lead = st.number_input("Tiempo de Entrega / Lead Time (Meses):", min_value=1, value=12)
            v_garantia = st.number_input("Años de Garantía:", min_value=1, value=2)
            v_estado = st.selectbox("Estado de la Oferta:", ["En Evaluación", "Adjudicada Base", "Desestimada"])
            
            submit_vendor = st.form_submit_button("➕ Registrar Cotización de Empresa")
            
            if submit_vendor and v_empresa:
                new_v_row = {
                    "ID": eq_id,
                    "Equipo": selected_eq_name,
                    "Empresa": v_empresa,
                    "Precio_USD": v_precio,
                    "Lead_Time_Meses": v_lead,
                    "Garantia_Años": v_garantia,
                    "Estado": v_estado
                }
                st.session_state.vendedores_db = pd.concat([st.session_state.vendedores_db, pd.DataFrame([new_v_row])], ignore_index=True)
                
                # Update Equipment state to Cotizado
                st.session_state.equipos_db.loc[st.session_state.equipos_db["ID"] == eq_id, "Cotizado"] = True
                st.session_state.equipos_db.loc[st.session_state.equipos_db["ID"] == eq_id, "Fecha"] = pd.Timestamp.now().strftime("%Y-%m-%d")
                if v_estado == "Adjudicada Base":
                    st.session_state.equipos_db.loc[st.session_state.equipos_db["ID"] == eq_id, "Proveedor_Lider"] = v_empresa
                
                st.success(f"✅ Cotización de {v_empresa} registrada exitosamente!")
                st.rerun()

    st.markdown("---")
    st.subheader(f"📊 Tabla Comparativa de Ofertas Recibidas para: '{selected_eq_name}'")

    offers_df = st.session_state.vendedores_db[st.session_state.vendedores_db["ID"] == eq_id]

    if len(offers_df) > 0:
        st.dataframe(
            offers_df[["Empresa", "Precio_USD", "Lead_Time_Meses", "Garantia_Años", "Estado"]].style.format({
                "Precio_USD": "${:,.2f}",
                "Lead_Time_Meses": "{:d} meses",
                "Garantia_Años": "{:d} años"
            }).highlight_min(axis=0, subset=["Precio_USD"], color="#D1FAE5"),
            use_container_width=True
        )

        fig_offers = px.bar(
            offers_df,
            x="Empresa",
            y="Precio_USD",
            text_auto=".2s",
            color="Empresa",
            title="Comparativa de Precios por Empresa ($USD)"
        )
        st.plotly_chart(fig_offers, use_container_width=True)
    else:
        st.warning("⚠️ No hay empresas cotizantes registradas aún para este equipo. Utilice el formulario superior para agregar la primera cotización.")

# -----------------------------------------------------------------------------
# MODULE 4: BASE DE DATOS MAESTRA DE EQUIPOS
# -----------------------------------------------------------------------------
elif module == "📦 Base de Datos Maestra de Equipos":
    st.markdown('<div class="main-header">Base de Datos de Equipamiento por Cotizar</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Registro Maestro MTO y Estado de Licitación - Proyecto ENC-3430</div>', unsafe_allow_html=True)

    c_f1, c_f2, c_f3 = st.columns(3)
    with c_f1:
        f_area = st.multiselect("Filtrar Área:", options=st.session_state.equipos_db["Area"].unique(), default=st.session_state.equipos_db["Area"].unique())
    with c_f2:
        f_status = st.multiselect("Estado Cotización:", [True, False], format_func=lambda x: "Cotizado ✅" if x else "Pendiente ⏳", default=[True, False])
    with c_f3:
        f_search = st.text_input("🔍 Buscar Equipo / Ítem:", "")

    # Apply filters
    filtered_db = st.session_state.equipos_db[
        (st.session_state.equipos_db["Area"].isin(f_area)) &
        (st.session_state.equipos_db["Cotizado"].isin(f_status))
    ]
    if f_search:
        filtered_db = filtered_db[filtered_db["Equipo"].str.contains(f_search, case=False, na=False)]

    st.dataframe(
        filtered_db[["ID", "Area", "Categoria", "Equipo", "Cantidad", "Unidad", "Presupuesto_USD", "Cotizado", "Fecha", "Proveedor_Lider"]].style.format({
            "Cantidad": "{:,.1f}",
            "Presupuesto_USD": "${:,.2f}"
        }),
        use_container_width=True,
        height=450
    )

# -----------------------------------------------------------------------------
# MODULE 5: EXPORTAR REPORTES DE LICITACIÓN
# -----------------------------------------------------------------------------
elif module == "📤 Exportar Reportes de Licitación":
    st.markdown('<div class="main-header">Centro de Exportación de Datos de Licitación</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Descarga de Bases de Datos de Cotizaciones y Ofertas de Proveedores (CSV)</div>', unsafe_allow_html=True)

    d1, d2 = st.columns(2)
    with d1:
        st.subheader("📥 Exportar Estado de Equipos (MTO / Cotizados)")
        csv_eq = st.session_state.equipos_db.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Registro de Cotizaciones (CSV)",
            data=csv_eq,
            file_name="BHP_ENC3430_Estado_Cotizaciones.csv",
            mime="text/csv"
        )

    with d2:
        st.subheader("🏢 Exportar Ofertas de Empresas Proveedoras")
        csv_vendors = st.session_state.vendedores_db.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Matriz de Empresas (CSV)",
            data=csv_vendors,
            file_name="BHP_ENC3430_Ofertas_Proveedores.csv",
            mime="text/csv"
        )
