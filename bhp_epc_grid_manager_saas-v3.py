import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BHP ENC-3430 | Control de Cubicaciones, Precios y Fabricantes",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.0rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .stMetric label {
        font-weight: 600 !important;
        color: #374151 !important;
    }
    .highlight-card {
        background-color: #F3F4F6;
        border-left: 5px solid #2563EB;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATASET INITIALIZATION
# -----------------------------------------------------------------------------
@st.cache_data
def load_cubicaciones_precios_data():
    # 1. Resumen por Área
    summary_data = [
        {"Area": "S/E EGP 220/33 kV (GIS)", "Costo_Equipos_USD": 35158330.0, "Volumen_Hormigon_m3": 1090.8, "Peso_Acero_kg": 263722.0, "Volumen_Excavacion_m3": 7638.7, "Num_Equipos_Mayores": 8},
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Costo_Equipos_USD": 8845200.0, "Volumen_Hormigon_m3": 450.0, "Peso_Acero_kg": 5270.0, "Volumen_Excavacion_m3": 2100.0, "Num_Equipos_Mayores": 33},
        {"Area": "Línea Transmisión 2x220 kV", "Costo_Equipos_USD": 16248350.0, "Volumen_Hormigon_m3": 1206.5, "Peso_Acero_kg": 1054948.0, "Volumen_Excavacion_m3": 6622.7, "Num_Equipos_Mayores": 84}
    ]
    summary_df = pd.DataFrame(summary_data)

    # 2. Listado Maestro de Cubicaciones y Precios
    mto_data = [
        # --- SUBESTACIÓN EGP 220/33 kV ---
        {"Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Equipos Mayores", "Item": "Switchgear GIS 245 kV (Suministro y Montaje)", "Unidad": "Gl", "Cantidad": 1.0, "Precio_Unitario_USD": 14500000.0, "Costo_Total_USD": 14500000.0, "Tipo": "Suministro Electromecánico"},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Equipos Mayores", "Item": "Transformador de Poder 220/33 kV (125 MVA)", "Unidad": "c/u", "Cantidad": 3.0, "Precio_Unitario_USD": 3800000.0, "Costo_Total_USD": 11400000.0, "Tipo": "Suministro Electromecánico"},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Equipos Mayores", "Item": "Ductos de Barras GIL 220 kV (Conexión GIS - Trafo)", "Unidad": "Gl", "Cantidad": 1.0, "Precio_Unitario_USD": 3200000.0, "Costo_Total_USD": 3200000.0, "Tipo": "Suministro Electromecánico"},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Infraestructura", "Item": "Galpón Prefabricado GIS (31,5x22,7x14 m)", "Unidad": "Gl", "Cantidad": 1.0, "Precio_Unitario_USD": 1850000.0, "Costo_Total_USD": 1850000.0, "Tipo": "Obras Civiles / Edificación"},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Equipos Mayores", "Item": "Sala Prefabricada SS/GG y Control (15,7x13,7 m)", "Unidad": "Gl", "Cantidad": 1.0, "Precio_Unitario_USD": 1200000.0, "Costo_Total_USD": 1200000.0, "Tipo": "Equipos de Control"},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Equipos Auxiliares", "Item": "Grupo Generador Emergencia MT (4,16 kV - 2.750 kVA)", "Unidad": "c/u", "Cantidad": 1.0, "Precio_Unitario_USD": 950000.0, "Costo_Total_USD": 950000.0, "Tipo": "Suministro Electromecánico"},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Equipos Auxiliares", "Item": "Subestaciones Unitarias 7,5 MVA (33/4,16 kV)", "Unidad": "c/u", "Cantidad": 3.0, "Precio_Unitario_USD": 420000.0, "Costo_Total_USD": 1260000.0, "Tipo": "Suministro Electromecánico"},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Equipos Auxiliares", "Item": "Resistencia Puesta a Tierra NGR y Auxiliares", "Unidad": "c/u", "Cantidad": 3.0, "Precio_Unitario_USD": 85000.0, "Costo_Total_USD": 255000.0, "Tipo": "Suministro Electromecánico"},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Materiales Civiles", "Item": "Hormigón Estructural G35 (Pedestales y Muros)", "Unidad": "m³", "Cantidad": 798.8, "Precio_Unitario_USD": 458.5, "Costo_Total_USD": 366264.0, "Tipo": "Materiales de Construcción"},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Materiales Civiles", "Item": "Armadura Acero de Refuerzo A630-420H", "Unidad": "kg", "Cantidad": 252183.0, "Precio_Unitario_USD": 2.60, "Costo_Total_USD": 655675.8, "Tipo": "Materiales de Construcción"},
        {"Area": "S/E EGP 220/33 kV (GIS)", "Categoria": "Materiales Civiles", "Item": "Excavaciones Estructurales (Suelo T1 - T4)", "Unidad": "m³", "Cantidad": 7638.7, "Precio_Unitario_USD": 28.3, "Costo_Total_USD": 216554.0, "Tipo": "Movimiento de Tierras"},

        # --- SUBESTACIÓN MONTE MINA 220 kV ---
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Categoria": "Equipos Mayores", "Item": "Interruptor Tanque Muerto SF6 220 kV 3150A 50kA", "Unidad": "c/u", "Cantidad": 3.0, "Precio_Unitario_USD": 220000.0, "Costo_Total_USD": 660000.0, "Tipo": "Suministro Electromecánico"},
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Categoria": "Equipos Mayores", "Item": "Transformador de Potencial Capacitivo (TPC) 220 kV", "Unidad": "c/u", "Cantidad": 10.0, "Precio_Unitario_USD": 42000.0, "Costo_Total_USD": 420000.0, "Tipo": "Suministro Electromecánico"},
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Categoria": "Equipos Mayores", "Item": "Desconectador Tripolar Apertura Central s/p/t 220 kV", "Unidad": "c/u", "Cantidad": 8.0, "Precio_Unitario_USD": 38000.0, "Costo_Total_USD": 304000.0, "Tipo": "Suministro Electromecánico"},
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Categoria": "Equipos Mayores", "Item": "Desconectador Tripolar Apertura Central c/p/t 220 kV", "Unidad": "c/u", "Cantidad": 2.0, "Precio_Unitario_USD": 45000.0, "Costo_Total_USD": 90000.0, "Tipo": "Suministro Electromecánico"},
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Categoria": "Equipos Auxiliares", "Item": "Pararrayos 220 kV con Contador de Descargas", "Unidad": "c/u", "Cantidad": 6.0, "Precio_Unitario_USD": 12500.0, "Costo_Total_USD": 75000.0, "Tipo": "Suministro Electromecánico"},
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Categoria": "Equipos Auxiliares", "Item": "Trampa de Ondas 220 kV (0.2 mH, 2000A)", "Unidad": "c/u", "Cantidad": 4.0, "Precio_Unitario_USD": 28000.0, "Costo_Total_USD": 112000.0, "Tipo": "Suministro Electromecánico"},
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Categoria": "Suministros Aislados", "Item": "Cable Aislado XLPE 220 kV 3000 mm²", "Unidad": "m", "Cantidad": 1800.0, "Precio_Unitario_USD": 450.0, "Costo_Total_USD": 810000.0, "Tipo": "Cables Subterráneos"},
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Categoria": "Suministros Aislados", "Item": "Mufas de Transición Aire/Cable XLPE 220 kV", "Unidad": "c/u", "Cantidad": 12.0, "Precio_Unitario_USD": 35000.0, "Costo_Total_USD": 420000.0, "Tipo": "Cables Subterráneos"},
        {"Area": "S/E Monte Mina 220 kV (AIS)", "Categoria": "Materiales Civiles", "Item": "Obras Civiles, Fundaciones y Malla de Tierra", "Unidad": "Gl", "Cantidad": 1.0, "Precio_Unitario_USD": 5954200.0, "Costo_Total_USD": 5954200.0, "Tipo": "Obras Civiles / Malla Tierra"},

        # --- LÍNEA DE TRANSMISIÓN 2x220 kV ---
        {"Area": "Línea Transmisión 2x220 kV", "Categoria": "Estructuras LAT", "Item": "Torres de Suspensión Reticuladas 22AD.1M3 (66 Torres)", "Unidad": "kg", "Cantidad": 662580.0, "Precio_Unitario_USD": 4.20, "Costo_Total_USD": 2782836.0, "Tipo": "Estructuras de Acero"},
        {"Area": "Línea Transmisión 2x220 kV", "Categoria": "Estructuras LAT", "Item": "Torres de Anclaje/Remate 22CD/22DD (18 Torres)", "Unidad": "kg", "Cantidad": 372300.0, "Precio_Unitario_USD": 4.50, "Costo_Total_USD": 1675350.0, "Tipo": "Estructuras de Acero"},
        {"Area": "Línea Transmisión 2x220 kV", "Categoria": "Estructuras LAT", "Item": "Marcos de Línea 2x220 kV (2 estructuras)", "Unidad": "kg", "Cantidad": 20064.0, "Precio_Unitario_USD": 4.80, "Costo_Total_USD": 96307.2, "Tipo": "Estructuras de Acero"},
        {"Area": "Línea Transmisión 2x220 kV", "Categoria": "Conductores / Cables", "Item": "Conductor de Fase AAAC Flint 740.8 MCM (25.7 km)", "Unidad": "m", "Cantidad": 312000.0, "Precio_Unitario_USD": 14.50, "Costo_Total_USD": 4524000.0, "Tipo": "Conductores de Línea"},
        {"Area": "Línea Transmisión 2x220 kV", "Categoria": "Conductores / Cables", "Item": "Cable de Guardia OPGW 24 Fibras Ópticas", "Unidad": "m", "Cantidad": 27000.0, "Precio_Unitario_USD": 8.50, "Costo_Total_USD": 229500.0, "Tipo": "Conductores de Línea"},
        {"Area": "Línea Transmisión 2x220 kV", "Categoria": "Conductores / Cables", "Item": "Cable de Guardia Acero Galvanizado EHS 3/8 in", "Unidad": "m", "Cantidad": 27000.0, "Precio_Unitario_USD": 4.20, "Costo_Total_USD": 113400.0, "Tipo": "Conductores de Línea"},
        {"Area": "Línea Transmisión 2x220 kV", "Categoria": "Aisladores / Herrajes", "Item": "Cadenas de Aisladores Poliméricos 220 kV", "Unidad": "Juego", "Cantidad": 504.0, "Precio_Unitario_USD": 850.0, "Costo_Total_USD": 428400.0, "Tipo": "Accesorios de Línea"},
        {"Area": "Línea Transmisión 2x220 kV", "Categoria": "Aisladores / Herrajes", "Item": "Herrajes y Amortiguadores de Vibración", "Unidad": "Gl", "Cantidad": 1.0, "Precio_Unitario_USD": 380000.0, "Costo_Total_USD": 380000.0, "Tipo": "Accesorios de Línea"},
        {"Area": "Línea Transmisión 2x220 kV", "Categoria": "Materiales Civiles", "Item": "Fundaciones de Hormigón G35 Torres LAT", "Unidad": "m³", "Cantidad": 1206.5, "Precio_Unitario_USD": 420.0, "Costo_Total_USD": 506730.0, "Tipo": "Materiales de Construcción"},
        {"Area": "Línea Transmisión 2x220 kV", "Categoria": "Materiales Civiles", "Item": "Excavaciones Obras Civiles LAT (S1 a S4)", "Unidad": "m³", "Cantidad": 6622.7, "Precio_Unitario_USD": 28.5, "Costo_Total_USD": 188746.95, "Tipo": "Movimiento de Tierras"}
    ]
    mto_df = pd.DataFrame(mto_data)

    # 3. Comparativa de Fabricantes (Benchmarking de Oferta)
    vendor_data = [
        # Switchgear GIS 245 kV
        {"Item": "Switchgear GIS 245 kV (Suministro y Montaje)", "Fabricante": "Hitachi Energy (ABB)", "Origen": "Suiza / Japón", "Precio_Unitario_USD": 14500000.0, "Lead_Time_Meses": 14, "Estado": "Seleccionado (Base)", "Cumplimiento_Tech": "100%", "Garantia_Anos": 5},
        {"Item": "Switchgear GIS 245 kV (Suministro y Montaje)", "Fabricante": "Siemens Energy", "Origen": "Alemania", "Precio_Unitario_USD": 15200000.0, "Lead_Time_Meses": 15, "Estado": "Oferta Valida", "Cumplimiento_Tech": "98%", "Garantia_Anos": 5},
        {"Item": "Switchgear GIS 245 kV (Suministro y Montaje)", "Fabricante": "GE Vernova", "Origen": "Francia / EEUU", "Precio_Unitario_USD": 14850000.0, "Lead_Time_Meses": 13, "Estado": "Oferta Valida", "Cumplimiento_Tech": "97%", "Garantia_Anos": 3},
        {"Item": "Switchgear GIS 245 kV (Suministro y Montaje)", "Fabricante": "Hyosung Heavy Industries", "Origen": "Corea del Sur", "Precio_Unitario_USD": 13900000.0, "Lead_Time_Meses": 12, "Estado": "Descalificado por Specs", "Cumplimiento_Tech": "91%", "Garantia_Anos": 3},

        # Transformador 125 MVA
        {"Item": "Transformador de Poder 220/33 kV (125 MVA)", "Fabricante": "Siemens Energy", "Origen": "Brasil / Alemania", "Precio_Unitario_USD": 3800000.0, "Lead_Time_Meses": 12, "Estado": "Seleccionado (Base)", "Cumplimiento_Tech": "100%", "Garantia_Anos": 5},
        {"Item": "Transformador de Poder 220/33 kV (125 MVA)", "Fabricante": "Hitachi Energy", "Origen": "Brasil / Suecia", "Precio_Unitario_USD": 3950000.0, "Lead_Time_Meses": 13, "Estado": "Oferta Valida", "Cumplimiento_Tech": "100%", "Garantia_Anos": 5},
        {"Item": "Transformador de Poder 220/33 kV (125 MVA)", "Fabricante": "Hyundai Electric", "Origen": "Corea del Sur", "Precio_Unitario_USD": 3650000.0, "Lead_Time_Meses": 11, "Estado": "Oferta Valida", "Cumplimiento_Tech": "95%", "Garantia_Anos": 3},
        {"Item": "Transformador de Poder 220/33 kV (125 MVA)", "Fabricante": "WEG Transformers", "Origen": "Brasil", "Precio_Unitario_USD": 3720000.0, "Lead_Time_Meses": 12, "Estado": "Oferta Valida", "Cumplimiento_Tech": "96%", "Garantia_Anos": 3},

        # Cable XLPE 220 kV
        {"Item": "Cable Aislado XLPE 220 kV 3000 mm²", "Fabricante": "Prysmian Group", "Origen": "Italia / Holanda", "Precio_Unitario_USD": 450.0, "Lead_Time_Meses": 8, "Estado": "Seleccionado (Base)", "Cumplimiento_Tech": "100%", "Garantia_Anos": 5},
        {"Item": "Cable Aislado XLPE 220 kV 3000 mm²", "Fabricante": "Nexans", "Origen": "Francia / Bélgica", "Precio_Unitario_USD": 475.0, "Lead_Time_Meses": 9, "Estado": "Oferta Valida", "Cumplimiento_Tech": "100%", "Garantia_Anos": 5},
        {"Item": "Cable Aislado XLPE 220 kV 3000 mm²", "Fabricante": "NKT Cables", "Origen": "Dinamarca / Alemania", "Precio_Unitario_USD": 460.0, "Lead_Time_Meses": 8, "Estado": "Oferta Valida", "Cumplimiento_Tech": "98%", "Garantia_Anos": 4},
        {"Item": "Cable Aislado XLPE 220 kV 3000 mm²", "Fabricante": "LS Cable & System", "Origen": "Corea del Sur", "Precio_Unitario_USD": 435.0, "Lead_Time_Meses": 7, "Estado": "Oferta Valida", "Cumplimiento_Tech": "94%", "Garantia_Anos": 3},

        # Interruptor SF6
        {"Item": "Interruptor Tanque Muerto SF6 220 kV 3150A 50kA", "Fabricante": "Hitachi Energy (ABB)", "Origen": "EEUU / Suiza", "Precio_Unitario_USD": 220000.0, "Lead_Time_Meses": 7, "Estado": "Seleccionado (Base)", "Cumplimiento_Tech": "100%", "Garantia_Anos": 5},
        {"Item": "Interruptor Tanque Muerto SF6 220 kV 3150A 50kA", "Fabricante": "Siemens Energy", "Origen": "Alemania / EEUU", "Precio_Unitario_USD": 235000.0, "Lead_Time_Meses": 8, "Estado": "Oferta Valida", "Cumplimiento_Tech": "99%", "Garantia_Anos": 5},
        {"Item": "Interruptor Tanque Muerto SF6 220 kV 3150A 50kA", "Fabricante": "GE Vernova", "Origen": "EEUU", "Precio_Unitario_USD": 228000.0, "Lead_Time_Meses": 7, "Estado": "Oferta Valida", "Cumplimiento_Tech": "97%", "Garantia_Anos": 3},

        # Conductor AAAC Flint
        {"Item": "Conductor de Fase AAAC Flint 740.8 MCM (25.7 km)", "Fabricante": "Prysmian / General Cable", "Origen": "Chile / Brasil", "Precio_Unitario_USD": 14.50, "Lead_Time_Meses": 5, "Estado": "Seleccionado (Base)", "Cumplimiento_Tech": "100%", "Garantia_Anos": 3},
        {"Item": "Conductor de Fase AAAC Flint 740.8 MCM (25.7 km)", "Fabricante": "Midal Cables", "Origen": "Baréin", "Precio_Unitario_USD": 13.90, "Lead_Time_Meses": 6, "Estado": "Oferta Valida", "Cumplimiento_Tech": "96%", "Garantia_Anos": 3},
        {"Item": "Conductor de Fase AAAC Flint 740.8 MCM (25.7 km)", "Fabricante": "Southwire", "Origen": "EEUU", "Precio_Unitario_USD": 15.10, "Lead_Time_Meses": 5, "Estado": "Oferta Valida", "Cumplimiento_Tech": "99%", "Garantia_Anos": 3}
    ]
    vendor_df = pd.DataFrame(vendor_data)

    return summary_df, mto_df, vendor_df

summary_df, mto_df, vendor_df = load_cubicaciones_precios_data()

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION & FILTERS
# -----------------------------------------------------------------------------
st.sidebar.markdown("## BHP ENC-3430")
st.sidebar.markdown("**Control de Cubicaciones y Equipamiento**")
st.sidebar.markdown("---")

module = st.sidebar.radio(
    "Módulos de la Plataforma:",
    [
        "📊 Resumen de Cubicaciones y Costos",
        "📦 Matriz de Cubicaciones y Precios",
        "⚡ Precios de Equipamientos Mayores",
        "🏢 Comparativa de Fabricantes",
        "🧮 Simulador de Cantidades y Precios",
        "📤 Exportación de Datos (Excel/CSV)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filtro por Instalación:")
selected_areas = st.sidebar.multiselect(
    "Seleccionar Áreas:",
    options=mto_df["Area"].unique(),
    default=mto_df["Area"].unique()
)

filtered_mto = mto_df[mto_df["Area"].isin(selected_areas)]

# -----------------------------------------------------------------------------
# MODULE 1: RESUMEN DE CUBICACIONES Y COSTOS
# -----------------------------------------------------------------------------
if module == "📊 Resumen de Cubicaciones y Costos":
    st.markdown('<div class="main-header">Resumen de Cubicaciones y Precios de Equipamiento</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Consolidado General del Proyecto Escondida Concentrator (ENC-3430)</div>', unsafe_allow_html=True)

    # Key KPI Cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    total_cost = filtered_mto["Costo_Total_USD"].sum()
    total_concrete = filtered_mto[filtered_mto["Unidad"] == "m³"]["Cantidad"].sum()
    total_steel = filtered_mto[filtered_mto["Unidad"] == "kg"]["Cantidad"].sum()
    total_items = len(filtered_mto)

    with kpi1:
        st.metric("Costo Total Equipos y Materiales", f"${total_cost:,.2f} USD")
    with kpi2:
        st.metric("Volumen Hormigón Total", f"{total_concrete:,.1f} m³")
    with kpi3:
        st.metric("Peso Estructuras y Acero", f"{total_steel:,.0f} kg")
    with kpi4:
        st.metric("Partidas / Ítems Totales", f"{total_items} Partidas")

    st.markdown("---")

    # Column layout for Charts
    c1, c2 = st.columns([6, 4])

    with c1:
        st.subheader("Costo Total de Equipamiento y Materiales por Área (USD)")
        area_costs = filtered_mto.groupby("Area")["Costo_Total_USD"].sum().reset_index()
        fig_area = px.bar(
            area_costs,
            x="Area",
            y="Costo_Total_USD",
            text_auto=".2s",
            color="Area",
            color_discrete_sequence=["#1E3A8A", "#2563EB", "#60A5FA"],
            labels={"Costo_Total_USD": "Costo Total (USD)", "Area": "Instalación"}
        )
        fig_area.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig_area, use_container_width=True)

    with c2:
        st.subheader("Distribución de Costo por Categoría")
        cat_costs = filtered_mto.groupby("Categoria")["Costo_Total_USD"].sum().reset_index()
        fig_cat = px.pie(
            cat_costs,
            values="Costo_Total_USD",
            names="Categoria",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        fig_cat.update_layout(height=380)
        st.plotly_chart(fig_cat, use_container_width=True)

    st.subheader("Desglose de Costo por Tipo de Suministro")
    fig_treemap = px.treemap(
        filtered_mto,
        path=["Area", "Categoria", "Item"],
        values="Costo_Total_USD",
        color="Costo_Total_USD",
        color_continuous_scale="Blues"
    )
    fig_treemap.update_layout(height=420)
    st.plotly_chart(fig_treemap, use_container_width=True)

# -----------------------------------------------------------------------------
# MODULE 2: MATRIZ DE CUBICACIONES Y PRECIOS
# -----------------------------------------------------------------------------
elif module == "📦 Matriz de Cubicaciones y Precios":
    st.markdown('<div class="main-header">Matriz Detallada de Cubicaciones y Precios Unitarios</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Listado Completo de Quantities (MTO), Precios Unitarios y Totales en USD</div>', unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns([4, 4, 4])
    with col_f1:
        selected_cat = st.multiselect("Filtrar por Categoría:", options=mto_df["Categoria"].unique(), default=mto_df["Categoria"].unique())
    with col_f2:
        selected_tipo = st.multiselect("Filtrar por Tipo:", options=mto_df["Tipo"].unique(), default=mto_df["Tipo"].unique())
    with col_f3:
        search_query = st.text_input("🔍 Buscar Ítem o Equipamiento:", "")

    # Apply filters
    df_display = filtered_mto[
        (filtered_mto["Categoria"].isin(selected_cat)) &
        (filtered_mto["Tipo"].isin(selected_tipo))
    ]
    if search_query:
        df_display = df_display[df_display["Item"].str.contains(search_query, case=False, na=False)]

    st.markdown(f"**Registros encontrados:** {len(df_display)}")

    # Format table for visual output
    st.dataframe(
        df_display.style.format({
            "Cantidad": "{:,.1f}",
            "Precio_Unitario_USD": "${:,.2f}",
            "Costo_Total_USD": "${:,.2f}"
        }),
        use_container_width=True,
        height=450
    )

    subtotal = df_display["Costo_Total_USD"].sum()
    st.info(f"💡 **Subtotal Seleccionado:** ${subtotal:,.2f} USD")

# -----------------------------------------------------------------------------
# MODULE 3: PRECIOS DE EQUIPAMIENTOS MAYORES
# -----------------------------------------------------------------------------
elif module == "⚡ Precios de Equipamientos Mayores":
    st.markdown('<div class="main-header">Ficha de Precios de Equipamientos Mayores</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Análisis Específico de los Equipos Estratégicos del Proyecto</div>', unsafe_allow_html=True)

    equipos_mayores_df = mto_df[mto_df["Categoria"].isin(["Equipos Mayores", "Equipos Auxiliares", "Suministros Aislados"])].copy()

    st.dataframe(
        equipos_mayores_df[["Area", "Item", "Unidad", "Cantidad", "Precio_Unitario_USD", "Costo_Total_USD"]].style.format({
            "Cantidad": "{:,.1f}",
            "Precio_Unitario_USD": "${:,.2f}",
            "Costo_Total_USD": "${:,.2f}"
        }),
        use_container_width=True,
        height=350
    )

    st.subheader("Comparativa de Precios Unitarios de Equipos Principales (USD)")
    
    # Filter items with per unit pricing for direct bar comparison
    unit_equip_df = equipos_mayores_df[equipos_mayores_df["Unidad"].isin(["c/u", "Gl"])].sort_values(by="Precio_Unitario_USD", ascending=True)
    
    fig_unit_price = px.bar(
        unit_equip_df,
        x="Precio_Unitario_USD",
        y="Item",
        orientation="h",
        text_auto=".2s",
        color="Area",
        labels={"Precio_Unitario_USD": "Precio Unitario (USD)", "Item": "Equipamiento Mayor"}
    )
    fig_unit_price.update_layout(height=450)
    st.plotly_chart(fig_unit_price, use_container_width=True)

# -----------------------------------------------------------------------------
# MODULE 4: COMPARATIVA DE FABRICANTES (NEW MODULE)
# -----------------------------------------------------------------------------
elif module == "🏢 Comparativa de Fabricantes":
    st.markdown('<div class="main-header">Tabla Comparativa de Precios por Fabricante</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Benchmarking de Ofertas Económicas y Plazos para Equipos Mayores del Proyecto</div>', unsafe_allow_html=True)

    # Equipment Selector
    equip_options = vendor_df["Item"].unique()
    selected_equip = st.selectbox("Seleccionar Equipamiento para Análisis de Ofertas:", equip_options)

    # Filter vendor data for selected equipment
    equip_vendor_df = vendor_df[vendor_df["Item"] == selected_equip].copy()

    # Find baseline selected price
    base_row = equip_vendor_df[equip_vendor_df["Estado"].str.contains("Seleccionado")]
    if not base_row.empty:
        base_price = base_row.iloc[0]["Precio_Unitario_USD"]
        base_vendor = base_row.iloc[0]["Fabricante"]
    else:
        base_price = equip_vendor_df.iloc[0]["Precio_Unitario_USD"]
        base_vendor = equip_vendor_df.iloc[0]["Fabricante"]

    equip_vendor_df["Dif_vs_Base_%"] = ((equip_vendor_df["Precio_Unitario_USD"] - base_price) / base_price) * 100.0

    # Key Metrics for Selected Item
    v_col1, v_col2, v_col3, v_col4 = st.columns(4)
    min_price = equip_vendor_df["Precio_Unitario_USD"].min()
    max_price = equip_vendor_df["Precio_Unitario_USD"].max()
    avg_price = equip_vendor_df["Precio_Unitario_USD"].mean()

    with v_col1:
        st.metric("Fabricante Adjudicado / Base", base_vendor)
    with v_col2:
        st.metric("Precio Base Seleccionado", f"${base_price:,.2f} USD")
    with v_col3:
        st.metric("Rango de Ofertas (Min - Máx)", f"${min_price:,.0f} - ${max_price:,.0f} USD")
    with v_col4:
        st.metric("Promedio de Mercado", f"${avg_price:,.2f} USD")

    st.markdown("---")

    v_left, v_right = st.columns([6, 4])

    with v_left:
        st.subheader(f"Tabla de Licicitación: {selected_equip}")
        st.dataframe(
            equip_vendor_df[["Fabricante", "Origen", "Precio_Unitario_USD", "Dif_vs_Base_%", "Lead_Time_Meses", "Cumplimiento_Tech", "Garantia_Anos", "Estado"]].style.format({
                "Precio_Unitario_USD": "${:,.2f}",
                "Dif_vs_Base_%": "{:+.1f}%",
                "Lead_Time_Meses": "{} meses",
                "Garantia_Anos": "{} años"
            }),
            use_container_width=True,
            height=280
        )

    with v_right:
        st.subheader("Comparativa Gráfica de Precios Unitarios")
        fig_vendor_bar = px.bar(
            equip_vendor_df,
            x="Fabricante",
            y="Precio_Unitario_USD",
            text_auto=".2s",
            color="Estado",
            color_discrete_map={
                "Seleccionado (Base)": "#1E3A8A",
                "Oferta Valida": "#3B82F6",
                "Descalificado por Specs": "#EF4444"
            },
            labels={"Precio_Unitario_USD": "Precio Unitario ($USD)"}
        )
        fig_vendor_bar.update_layout(showlegend=True, height=300)
        st.plotly_chart(fig_vendor_bar, use_container_width=True)

    st.markdown("---")
    st.subheader("🌐 Consolidado General de Todos los Fabricantes Evaluados")
    st.dataframe(
        vendor_df.style.format({
            "Precio_Unitario_USD": "${:,.2f}",
            "Lead_Time_Meses": "{} m"
        }),
        use_container_width=True,
        height=320
    )

# -----------------------------------------------------------------------------
# MODULE 5: SIMULADOR DE CANTIDADES Y PRECIOS
# -----------------------------------------------------------------------------
elif module == "🧮 Simulador de Cantidades y Precios":
    st.markdown('<div class="main-header">Simulador de Sensibilidad: Cantidades y Precios</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Ajuste Dinámico de Variación de Cubicaciones y Precios Unitarios de Mercado</div>', unsafe_allow_html=True)

    sim_col1, sim_col2 = st.columns([5, 5])

    with sim_col1:
        st.subheader("⚙️ Controles de Sensibilidad")
        price_factor = st.slider("Variación Global de Precios de Equipamiento (%):", -20.0, 30.0, 0.0, step=1.0)
        qty_factor = st.slider("Ajuste de Cubicaciones de Campo (%):", -15.0, 25.0, 0.0, step=1.0)

        st.markdown("""
        **Notas de Simulación:**
        - El ajuste de precios simula fluctuaciones en el mercado de materias primas (cobre, acero, GIS).
        - El ajuste de cubicaciones refleja variaciones en mediciones reales durante la ejecución de obras civiles.
        """)

    with sim_col2:
        st.subheader("📊 Presupuesto Recalculado")
        
        base_total = filtered_mto["Costo_Total_USD"].sum()
        sim_total = base_total * (1 + price_factor / 100.0) * (1 + qty_factor / 100.0)
        diff_total = sim_total - base_total

        st.metric(
            "Costo Recalculado Proyecto",
            f"${sim_total:,.2f} USD",
            delta=f"${diff_total:,.2f} USD ({((sim_total/base_total)-1)*100:+.1f}%)"
        )

        # Comparative dataframe
        sim_df = filtered_mto.copy()
        sim_df["Cantidad_Simulada"] = sim_df["Cantidad"] * (1 + qty_factor / 100.0)
        sim_df["Precio_Unitario_Simulado"] = sim_df["Precio_Unitario_USD"] * (1 + price_factor / 100.0)
        sim_df["Costo_Total_Simulado"] = sim_df["Cantidad_Simulada"] * sim_df["Precio_Unitario_Simulado"]

        st.dataframe(
            sim_df[["Item", "Cantidad", "Cantidad_Simulada", "Precio_Unitario_USD", "Precio_Unitario_Simulado", "Costo_Total_USD", "Costo_Total_Simulado"]].head(6).style.format({
                "Cantidad": "{:,.1f}",
                "Cantidad_Simulada": "{:,.1f}",
                "Precio_Unitario_USD": "${:,.2f}",
                "Precio_Unitario_Simulado": "${:,.2f}",
                "Costo_Total_USD": "${:,.2f}",
                "Costo_Total_Simulado": "${:,.2f}"
            }),
            use_container_width=True
        )

# -----------------------------------------------------------------------------
# MODULE 6: EXPORTACIÓN DE DATOS
# -----------------------------------------------------------------------------
elif module == "📤 Exportación de Datos (Excel/CSV)":
    st.markdown('<div class="main-header">Centro de Exportación de Cubicaciones y Precios</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Descarga de Archivos de Datos para Integración con Sistemas ERP / Estimaciones</div>', unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)

    with d1:
        st.subheader("📥 Cubicaciones MTO (CSV)")
        csv_mto = mto_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar MTO Cubicaciones",
            data=csv_mto,
            file_name="BHP_ENC3430_Cubicaciones_Precios.csv",
            mime="text/csv"
        )

    with d2:
        st.subheader("📊 Resumen por Área (CSV)")
        csv_summary = summary_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Resumen Áreas",
            data=csv_summary,
            file_name="BHP_ENC3430_Resumen_Equipamiento.csv",
            mime="text/csv"
        )

    with d3:
        st.subheader("🏢 Comparativa Fabricantes (CSV)")
        csv_vendor = vendor_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Ofertas Fabricantes",
            data=csv_vendor,
            file_name="BHP_ENC3430_Comparativa_Fabricantes.csv",
            mime="text/csv"
        )

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 BHP | Control de Cubicaciones y Precios - Project ENC-3430")
