import streamlit as st
import pandas as pd

# Configuración básica de la APP
st.set_page_config(layout="wide", page_title="APP de Cotizaciones")

@st.cache_data
def cargar_datos_cotizacion():
    # 1. Leer los datos base desde el archivo Excel
    archivo_excel = 'Cotizar Eq. primarios 220 kV.xlsx'
    df = pd.read_excel(archivo_excel, sheet_name='Eq. primarios ')
    
    # Limpiar y formatear las columnas usando la estructura del archivo original
    df_clean = df[['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5']].dropna(subset=['Unnamed: 2'])
    df_clean = df_clean[df_clean['Unnamed: 2'].apply(lambda x: str(x).isdigit())]
    df_clean.columns = ['Item', 'Descripción', 'Unidad', 'Cantidad']
    
    # 2. Agregar los equipos adicionales desde los documentos del Proyecto (S/E Monte Mina)
    nuevos_equipos = pd.DataFrame([
        {'Item': 'Adic. 1', 'Descripción': 'Interruptores de Poder 220 KV (Tags: 3430-CB-00200 @ 00203)', 'Unidad': 'c/u', 'Cantidad': 4},
        {'Item': 'Adic. 2', 'Descripción': 'Transformadores de Potencial 220 kV (Tags: 3430-TX-00200@00205, 3430-TX-00206@00209)', 'Unidad': 'c/u', 'Cantidad': 10},
        {'Item': 'Adic. 3', 'Descripción': 'Unidad externa aire acondicionado (Tag: 3430-HAC-20202@20203)', 'Unidad': 'c/u', 'Cantidad': 2},
        {'Item': 'Adic. 4', 'Descripción': 'Sistema de extinción de incendio', 'Unidad': 'c/u', 'Cantidad': 1},
        {'Item': 'Adic. 5', 'Descripción': 'Armario de Multiplexores Línea "Monte Mina - S/E EGP"', 'Unidad': 'c/u', 'Cantidad': 1},
        {'Item': 'Adic. 6', 'Descripción': 'Armario de OPLAT Línea "Monte Mina - S/E EGP"', 'Unidad': 'c/u', 'Cantidad': 1},
        {'Item': 'Repuestos', 'Descripción': 'Repuestos esenciales: Aisladores, Juego de contactos, Moto-Ventilador, Conjunto de embalaje y Elementos de control', 'Unidad': 'Lote', 'Cantidad': 1}
    ])
    
    # Consolidar todos los equipos en un solo DataFrame
    df_final = pd.concat([df_clean, nuevos_equipos], ignore_index=True)
    
    # 3. Agregar columnas lógicas para el checklist interactivo
    df_final['Incluir en Cotización'] = True
    df_final['Estado de Cotización'] = 'Pendiente'
    df_final['Observaciones Proveedor'] = ''
    
    return df_final

st.title("📊 APP de Cotizaciones - Equipos y Suministros")

# Inicializar los datos en el session_state para que los cambios del checklist persistan
if 'datos_app' not in st.session_state:
    st.session_state.datos_app = cargar_datos_cotizacion()

# Crear el diseño de pestañas (Tabs)
tab1, tab2 = st.tabs(["📋 Listado General de Equipos", "📝 Pestaña de Checklist Editable"])

# PESTAÑA 1: Visualización estática
with tab1:
    st.subheader("Equipos consolidados (Excel Base + Especificaciones Técnicas)")
    st.dataframe(st.session_state.datos_app[['Item', 'Descripción', 'Unidad', 'Cantidad']], use_container_width=True, hide_index=True)

# PESTAÑA 2: Edición interactiva del Checklist
with tab2:
    st.subheader("Checklist de Cotización")
    st.info("💡 Haz doble clic en las celdas de 'Incluir', 'Estado' u 'Observaciones' para editarlas.")
    
    # Configuración de los tipos de columna para la edición interactiva
    columnas_configuradas = {
        "Incluir en Cotización": st.column_config.CheckboxColumn("¿Cotizar?", default=True),
        "Estado de Cotización": st.column_config.SelectboxColumn(
            "Estado", 
            options=["Pendiente", "Consultado", "Cotización Recibida", "Descartado"]
        ),
        "Observaciones Proveedor": st.column_config.TextColumn("Observaciones (Ej. Tiempos de entrega, marcas)")
    }
    
    # Implementación del st.data_editor para habilitar la edición de la tabla
    df_editado = st.data_editor(
        st.session_state.datos_app,
        column_config=columnas_configuradas,
        disabled=["Item", "Descripción", "Unidad", "Cantidad"], # Se bloquean los requerimientos técnicos
        use_container_width=True,
        hide_index=True,
        key="editor_interactivo"
    )
    
    # Botón para guardar las modificaciones realizadas por el usuario en el checklist
    if st.button("Guardar Cambios del Checklist"):
        st.session_state.datos_app = df_editado
        st.success("¡Los estados del checklist han sido guardados y actualizados correctamente!")
