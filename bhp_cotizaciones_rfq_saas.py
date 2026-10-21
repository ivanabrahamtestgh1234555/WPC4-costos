import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Cox Chile | Portal de Cotizaciones y Gestión de Proveedores",
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
        # --- EQUIPOS 220 KV (AMPLIACION S/E MONTEMINA 220 kV) ---
        {"ID": "MM-001", "Area": "Ampliación S/E Monte Mina 220 kV", "Categoria": "Equipos 220 kV", "Equipo": "INTERRUPTOR DE PODER TANQUE MUERTO, SF6, 245 kV, CON TTCC TIPO BUSHING, ACCIONAMIENTO MONOPOLAR; Ir: 4000 A; Icc: 50 kA; BIL: 1050 kVcr. @ 3200 m.s.n.m.", "Cantidad": 4.0, "Unidad": "c/u", "Presupuesto_USD": 880000.0, "Cotizado": True, "Fecha": "2026-09-18", "Proveedor_Lider": "Hitachi Energy"},
        {"ID": "MM-002", "Area": "Ampliación S/E Monte Mina 220 kV", "Categoria": "Equipos 220 kV", "Equipo": "TRANSFORMADOR DE POTENCIAL CAPACITIVO CL. 245 kV; BIL 1050 kVcr; 230: √3 / 0,115: √3 / 0,115: √3 S1 y S2: CL 0,2/3P - 15 VA; Df 31 mm/kV.", "Cantidad": 10.0, "Unidad": "c/u", "Presupuesto_USD": 420000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "MM-003", "Area": "Ampliación S/E Monte Mina 220 kV", "Categoria": "Equipos 220 kV", "Equipo": "DESCONECTADOR TRIPOLAR DE APERTURA CENTRAL SPT 220 kV, CL 245 kV; BIL 1175 kVcr @ 3200 m.s.n.m. In 3150 A; Icc 50 kA 3s.", "Cantidad": 8.0, "Unidad": "c/u", "Presupuesto_USD": 304000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "MM-004", "Area": "Ampliación S/E Monte Mina 220 kV", "Categoria": "Equipos 220 kV", "Equipo": "DESCONECTADOR TRIPOLAR DE APERTURA CENTRAL CPT 220 kV, CL 245 kV; BIL 1175 kVcr @ 3200 m.s.n.m. In 3150 A; Icc 50 kA 3s.", "Cantidad": 2.0, "Unidad": "c/u", "Presupuesto_USD": 90000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "MM-005", "Area": "Ampliación S/E Monte Mina 220 kV", "Categoria": "Equipos 220 kV", "Equipo": "TRAMPA DE ONDA. 0,2 mH, 220 kV, 2000 A, 50 kA.", "Cantidad": 4.0, "Unidad": "c/u", "Presupuesto_USD": 112000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "MM-006", "Area": "Ampliación S/E Monte Mina 220 kV", "Categoria": "Equipos 220 kV", "Equipo": "AISLADOR DE PEDESTAL PORCELANA CL.: 245 kV, BIL 1050 @ 3200 m.s.n.m.; Df: 9300 mm/kV; 10 kN", "Cantidad": 6.0, "Unidad": "c/u", "Presupuesto_USD": 24000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "MM-007", "Area": "Ampliación S/E Monte Mina 220 kV", "Categoria": "Equipos 220 kV", "Equipo": "PARARRAYOS 220 kV; Uc: 154 kV; In: 20 kA; Is: 65 KA", "Cantidad": 6.0, "Unidad": "c/u", "Presupuesto_USD": 75000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},

        # --- EQUIPOS 220 KV (PATIO DE MUFAS 220 kV) ---
        {"ID": "PM-001", "Area": "Patio de Mufas 220 kV", "Categoria": "Equipos 220 kV", "Equipo": "PARARRAYOS 220 kV; Uc: 154 kV; In: 20 kA; Is: 65 KA", "Cantidad": 12.0, "Unidad": "c/u", "Presupuesto_USD": 150000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "PM-002", "Area": "Patio de Mufas 220 kV", "Categoria": "Equipos 220 kV", "Equipo": "AISLADOR DE PEDESTAL PORCELANA CL.: 245 kV, BIL 1050 @ 3200 m.s.n.m.; Df: 9300 mm/kV; 10 kN", "Cantidad": 12.0, "Unidad": "c/u", "Presupuesto_USD": 48000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "PM-003", "Area": "Patio de Mufas 220 kV", "Categoria": "Cables y Conectores", "Equipo": "MUFA (CONECTOR DE TRANSICIÓN) AIRE / CABLE AISLADO XLPE 3000 mm2 / 220 kV", "Cantidad": 32.0, "Unidad": "c/u", "Presupuesto_USD": 1120000.0, "Cotizado": True, "Fecha": "2026-09-28", "Proveedor_Lider": "Prysmian Group"},
        {"ID": "PM-004", "Area": "Patio de Mufas 220 kV", "Categoria": "Cables y Conectores", "Equipo": "MUFA (CONECTOR DE TRANSICIÓN) AIRE / CABLE AISLADO XLPE 3000 mm2 / 220 kV", "Cantidad": 8.0, "Unidad": "c/u", "Presupuesto_USD": 280000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "PM-005", "Area": "Patio de Mufas 220 kV", "Categoria": "Equipos 220 kV", "Equipo": "DESCONECTADOR MONOPOLAR", "Cantidad": 16.0, "Unidad": "c/u", "Presupuesto_USD": 192000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "PM-006", "Area": "Patio de Mufas 220 kV", "Categoria": "Equipos 220 kV", "Equipo": "BARRA AUXILIAR 245 Kv", "Cantidad": 4.0, "Unidad": "c/u", "Presupuesto_USD": 120000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "PM-007", "Area": "Patio de Mufas 220 kV", "Categoria": "Cables y Conectores", "Equipo": "CONDUCTOR AISLACIÓN XLPE 3000 mm2, 220 Kv", "Cantidad": 6000.0, "Unidad": "m", "Presupuesto_USD": 2700000.0, "Cotizado": True, "Fecha": "2026-09-28", "Proveedor_Lider": "Prysmian Group"},
        {"ID": "PM-008", "Area": "Patio de Mufas 220 kV", "Categoria": "Cables y Conectores", "Equipo": "CONECTOR ENCHUFABLE PARA CABLE XLPE 3000 mm2 / 220 kV", "Cantidad": 40.0, "Unidad": "c/u", "Presupuesto_USD": 320000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "PM-009", "Area": "Patio de Mufas 220 kV", "Categoria": "Cables y Conectores", "Equipo": "LINK BOX", "Cantidad": 32.0, "Unidad": "c/u", "Presupuesto_USD": 160000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},

        # --- EQUIPOS S/E EGP 220/33 KV ---
        {"ID": "EGP-001", "Area": "S/E EGP 220/33 kV", "Categoria": "Protecciones y Medición", "Equipo": "PARARRAYOS DE LINEA CON CONTADOR DE DESCARGA 220 kV", "Cantidad": 15.0, "Unidad": "c/u", "Presupuesto_USD": 187500.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "EGP-002", "Area": "S/E EGP 220/33 kV", "Categoria": "Protecciones y Medición", "Equipo": "TRANSFORMADOR DE POTENCIAL CAPACITIVO 230/√3 : 0.115/√3 : 0.115/√3 kV", "Cantidad": 4.0, "Unidad": "c/u", "Presupuesto_USD": 168000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "EGP-003", "Area": "S/E EGP 220/33 kV", "Categoria": "Aisladores y Soportes", "Equipo": "AISLADOR DE PEDESTAL PORCELANA CL.: 245 kV, BIL 1050 @ 3200 m.s.n.m.; Df: 9300 mm/kV; 10 kN", "Cantidad": 18.0, "Unidad": "c/u", "Presupuesto_USD": 72000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "EGP-004", "Area": "S/E EGP 220/33 kV", "Categoria": "Protecciones y Medición", "Equipo": "TRANSFORMADOR DE POTENCIAL CARGABLE 230/√3/0.4 kV", "Cantidad": 6.0, "Unidad": "c/u", "Presupuesto_USD": 210000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "EGP-005", "Area": "S/E EGP 220/33 kV", "Categoria": "Generación y Servicios Auxiliares", "Equipo": "GRUPO GENERADOR DE EMERGENCIA, 400-231 V, 50 Hz., 200 kVA", "Cantidad": 1.0, "Unidad": "c/u", "Presupuesto_USD": 85000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "EGP-006", "Area": "S/E EGP 220/33 kV", "Categoria": "Generación y Servicios Auxiliares", "Equipo": "GRUPO GENERADOR 4,16 kV; 2750 MVA @ 3200 m.s.n.m.", "Cantidad": 6.0, "Unidad": "c/u", "Presupuesto_USD": 5700000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "EGP-007", "Area": "S/E EGP 220/33 kV", "Categoria": "Telecomunicaciones / Onda", "Equipo": "TRAMPA DE ONDA. 0,2 mH, 220 kV, 2000 A, 50 kA.", "Cantidad": 4.0, "Unidad": "c/u", "Presupuesto_USD": 112000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "EGP-008", "Area": "S/E EGP 220/33 kV", "Categoria": "Transformadores y Subestaciones", "Equipo": "SUBESTACIÓN UNITARIA 7,5 MVA (KNAN, 65°C) a 3200 m.s.n.m. 4,16/33 kV", "Cantidad": 3.0, "Unidad": "c/u", "Presupuesto_USD": 1260000.0, "Cotizado": True, "Fecha": "2026-10-05", "Proveedor_Lider": "WEG Chile"},
        {"ID": "EGP-009", "Area": "S/E EGP 220/33 kV", "Categoria": "Calidad de Energía", "Equipo": "FILTRO DE ARMÓNICOS 33 kV Y DE COMPENSACIÓN DE REACTIVOS 33 kV", "Cantidad": 3.0, "Unidad": "c/u", "Presupuesto_USD": 1800000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "EGP-010", "Area": "S/E EGP 220/33 kV", "Categoria": "Maniobras y Desconexión", "Equipo": "DESCONECTADOR TRIPOLAR 33 kV CPT MOTORIZADO", "Cantidad": 6.0, "Unidad": "c/u", "Presupuesto_USD": 180000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"},
        {"ID": "EGP-011", "Area": "S/E EGP 220/33 kV", "Categoria": "Protecciones y Medición", "Equipo": "PARARRAYOS TIPO ESTACIÓN 33 kV", "Cantidad": 18.0, "Unidad": "c/u", "Presupuesto_USD": 108000.0, "Cotizado": False, "Fecha": "-", "Proveedor_Lider": "Pendiente"}
    ]
    st.session_state.equipos_db = pd.DataFrame(initial_equipos)

if "vendedores_db" not in st.session_state:
    initial_vendedores = [
        {"ID": "MM-001", "Equipo": "INTERRUPTOR DE PODER TANQUE MUERTO, SF6, 245 kV", "Empresa": "Hitachi Energy (ABB)", "Precio_USD": 220000.0, "Lead_Time_Meses": 14, "Garantia_Años": 3, "Estado": "Adjudicada Base", "Archivo": None},
        {"ID": "MM-001", "Equipo": "INTERRUPTOR DE PODER TANQUE MUERTO, SF6, 245 kV", "Empresa": "Siemens Energy", "Precio_USD": 235000.0, "Lead_Time_Meses": 15, "Garantia_Años": 2, "Estado": "En Evaluación", "Archivo": None},
        {"ID": "PM-003", "Equipo": "MUFA AIRE / CABLE AISLADO XLPE 3000 mm2 / 220 kV", "Empresa": "Prysmian Group", "Precio_USD": 35000.0, "Lead_Time_Meses": 8, "Garantia_Años": 5, "Estado": "Adjudicada Base", "Archivo": None},
        {"ID": "EGP-008", "Equipo": "SUBESTACIÓN UNITARIA 7,5 MVA 4,16/33 kV", "Empresa": "WEG Chile", "Precio_USD": 420000.0, "Lead_Time_Meses": 10, "Garantia_Años": 3, "Estado": "Adjudicada Base", "Archivo": None}
    ]
    st.session_state.vendedores_db = pd.DataFrame(initial_vendedores)

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
# Logo Cox Chile
st.sidebar.markdown("""
<div style="text-align: center; padding: 10px 0px;">
    <h1 style="color: #1E3A8A; font-weight: 900; margin: 0; font-size: 2.2rem; letter-spacing: 2px;">COX</h1>
    <p style="color: #2563EB; font-weight: 600; margin: 0; font-size: 0.95rem; letter-spacing: 1px;">Área de Estudios - Cox Chile</p>
</div>
""", unsafe_allow_html=True)
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
st.sidebar.caption("Área de Estudios - Cox Chile")

# -----------------------------------------------------------------------------
# MODULE 1: DASHBOARD DE COTIZACIONES Y RFQ
# -----------------------------------------------------------------------------
if module == "📊 Dashboard de Cotizaciones & RFQ":
    st.markdown('<div class="main-header">Control Ejecutivo de Cotizaciones y Licitaciones (RFQ)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Estado de Avance de Compras y Cotizaciones Pendientes - Área de Estudios Cox Chile</div>', unsafe_allow_html=True)

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

    filter_area = st.selectbox("Filtrar por Área de Proyecto:", ["Todas las Áreas"] + list(st.session_state.equipos_db["Area"].unique()))
    
    df_view = st.session_state.equipos_db.copy()
    if filter_area != "Todas las Áreas":
        df_view = df_view[df_view["Area"] == filter_area]

    st.markdown("#### Lista de Equipos y Control de Estado de Licitación:")
    
    for idx, row in df_view.iterrows():
        c_check, c_info, c_supplier, c_date = st.columns([1.5, 5.5, 3, 2])
        
        chk_key = f"chk_{row['ID']}"
        
        is_checked = c_check.checkbox(
            f"✅ {row['ID']}",
            value=bool(row["Cotizado"]),
            key=chk_key
        )
        
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
            st.caption(f"Categoría: {row['Categoria']} | Cantidad: {row['Cantidad']:,.1f} {row['Unidad']} | Presupuesto Est.: ${row['Presupuesto_USD']:,.2f} USD")

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
    st.markdown('<div class="sub-header">Gestión de Ofertas por Proveedor, Archivos Adjuntos y Adquisiciones del Proyecto</div>', unsafe_allow_html=True)

    col_select, col_add = st.columns([5, 5])

    with col_select:
        st.subheader("1. Seleccionar Equipamiento por Analizar")
        equipo_lista = st.session_state.equipos_db["Equipo"].unique()
        selected_eq_name = st.selectbox("Seleccionar Equipo / Suministro:", equipo_lista)
        
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
            
            uploaded_file = st.file_uploader("📄 Adjuntar documento de cotización (PDF, Excel, Word):", type=["pdf", "xlsx", "xls", "doc", "docx"])
            
            submit_vendor = st.form_submit_button("➕ Registrar Cotización de Empresa")
            
            if submit_vendor and v_empresa:
                file_bytes = None
                file_name = None
                if uploaded_file is not None:
                    file_bytes = uploaded_file.getvalue()
                    file_name = uploaded_file.name
                
                new_v_row = {
                    "ID": eq_id,
                    "Equipo": selected_eq_name,
                    "Empresa": v_empresa,
                    "Precio_USD": v_precio,
                    "Lead_Time_Meses": v_lead,
                    "Garantia_Años": v_garantia,
                    "Estado": v_estado,
                    "Archivo": file_name,
                    "File_Bytes": file_bytes
                }
                st.session_state.vendedores_db = pd.concat([st.session_state.vendedores_db, pd.DataFrame([new_v_row])], ignore_index=True)
                
                st.session_state.equipos_db.loc[st.session_state.equipos_db["ID"] == eq_id, "Cotizado"] = True
                st.session_state.equipos_db.loc[st.session_state.equipos_db["ID"] == eq_id, "Fecha"] = pd.Timestamp.now().strftime("%Y-%m-%d")
                if v_estado == "Adjudicada Base":
                    st.session_state.equipos_db.loc[st.session_state.equipos_db["ID"] == eq_id, "Proveedor_Lider"] = v_empresa
                
                st.success(f"✅ Cotización de {v_empresa} registrada e integrada exitosamente!")
                st.rerun()

    st.markdown("---")
    st.subheader(f"📊 Tabla Comparativa de Ofertas Recibidas para: '{selected_eq_name}'")

    offers_df = st.session_state.vendedores_db[st.session_state.vendedores_db["ID"] == eq_id]

    if len(offers_df) > 0:
        display_cols = ["Empresa", "Precio_USD", "Lead_Time_Meses", "Garantia_Años", "Estado", "Archivo"]
        st.dataframe(
            offers_df[display_cols].style.format({
                "Precio_USD": "${:,.2f}",
                "Lead_Time_Meses": "{:d} meses",
                "Garantia_Años": "{:d} años"
            }).highlight_min(axis=0, subset=["Precio_USD"], color="#D1FAE5"),
            use_container_width=True
        )

        # Download buttons for attached files
        for idx_v, row_v in offers_df.iterrows():
            if "File_Bytes" in row_v and row_v["File_Bytes"] is not None:
                st.download_button(
                    label=f"📥 Descargar Cotización: {row_v['Empresa']} ({row_v['Archivo']})",
                    data=row_v["File_Bytes"],
                    file_name=row_v["Archivo"],
                    key=f"dl_{idx_v}"
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
    st.markdown('<div class="sub-header">Registro Maestro MTO y Estado de Licitación - Área de Estudios Cox Chile</div>', unsafe_allow_html=True)

    c_f1, c_f2, c_f3 = st.columns(3)
    with c_f1:
        f_area = st.multiselect("Filtrar Área:", options=st.session_state.equipos_db["Area"].unique(), default=st.session_state.equipos_db["Area"].unique())
    with c_f2:
        f_status = st.multiselect("Estado Cotización:", [True, False], format_func=lambda x: "Cotizado ✅" if x else "Pendiente ⏳", default=[True, False])
    with c_f3:
        f_search = st.text_input("🔍 Buscar Equipo / Ítem:", "")

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
        height=500
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
            file_name="CoxChile_Estado_Cotizaciones.csv",
            mime="text/csv"
        )

    with d2:
        st.subheader("🏢 Exportar Ofertas de Empresas Proveedoras")
        csv_vendors = st.session_state.vendedores_db.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Matriz de Empresas (CSV)",
            data=csv_vendors,
            file_name="CoxChile_Ofertas_Proveedores.csv",
            mime="text/csv"
        )
