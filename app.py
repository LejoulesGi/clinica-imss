import streamlit as st
import math
from datetime import date, datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Asistente Clínico IMSS", layout="wide")

# --- BASE DE DATOS ECE (ESTRUCTURA MEJORADA) ---
# Clave: Nombre Fármaco
# Valor: [Piezas por caja, Límite envases por receta, Texto Presentación, MG por unidad (para cálculo)]
ece_db = {
    "Alprazolam 2 mg": [30, 1, "30 tabletas", 2.0],
    "Alprazolam 0.5 mg": [30, 1, "30 tabletas", 0.5],
    "Alprazolam 0.25 mg": [30, 2, "30 tabletas", 0.25],
    "Amitriptilina 25 mg": [30, 3, "30 tabletas", 25.0],
    "Anfebutamona 150 mg": [30, 2, "30 tabletas", 150.0],
    "Biperideno 2 mg": [50, 2, "50 tabletas", 2.0],
    "Bromazepam 3 mg": [30, 2, "30 tabletas", 3.0],
    "Carbamazepina 200 mg": [20, 6, "20 tabletas", 200.0],
    "Citalopram 20 mg": [14, 2, "14 tabletas", 20.0],
    "Diazepam 10 mg": [20, 2, "20 tabletas", 10.0],
    "Escitalopram 10 mg": [28, 2, "28 tabletas", 10.0],
    "Fluoxetina 20 mg": [14, 2, "14 tabletas", 20.0],
    "Gabapentina 300 mg": [15, 4, "15 tabletas", 300.0],
    "Haloperidol 5 mg": [20, 4, "20 tabletas", 5.0],
    "Hidroxizina 10 mg": [30, 1, "30 tabletas", 10.0],
    "Imipramina 25 mg": [20, 3, "20 tabletas", 25.0],
    "Lamotrigina 25 mg": [28, 2, "28 tabletas", 25.0],
    "Lamotrigina 100 mg": [28, 2, "28 tabletas", 100.0],
    "Litio 300 mg": [50, 2, "50 tabletas", 300.0],
    "Levomepromazina 25 mg": [20, 2, "20 tabletas", 25.0],
    "Lorazepam 1 mg": [40, 1, "40 tabletas", 1.0],
    "Metilfenidato 10 mg": [30, 5, "30 tabletas", 10.0],
    "Olanzapina 10 mg": [28, 2, "28 tabletas", 10.0],
    "Paroxetina 20 mg": [10, 6, "10 tabletas", 20.0],
    "Primidona 250 mg": [50, 2, "50 tabletas", 250.0],
    "Quetiapina 100 mg": [60, 3, "60 tabletas", 100.0],
    "Risperidona 2 mg": [40, 1, "40 tabletas", 2.0],
    "Sertralina 50 mg": [14, 2, "14 tabletas", 50.0],
    "Topiramato 100 mg": [60, 2, "60 tabletas", 100.0],
    "Topiramato 25 mg": [60, 1, "60 tabletas", 25.0],
    "Trifluoperazina 20 mg": [20, 3, "20 tabletas", 20.0],
    "Trihexifenidilo 5 mg": [50, 1, "50 tabletas", 5.0],
    "Valproato Mag 200 mg": [40, 6, "40 tabletas", 200.0],
    "Valproato Mag 600 mg": [30, 3, "30 tabletas", 600.0],
    "Valproato Semi 250 mg": [30, 3, "30 tabletas", 250.0],
    "Venlafaxina 75 mg": [10, 6, "10 tabletas", 75.0],
    "Pregabalina 75 mg": [28, 1, "28 cápsulas", 75.0],
    "Pregabalina 150 mg": [28, 1, "28 cápsulas", 150.0],
    "Oxcarbazepina 600 mg": [30, 3, "30 tabletas", 600.0]
}

# --- FUNCIONES ---
def generar_examen_mental(seccion):
    st.markdown(f"### 🧠 Examen Mental ({seccion})")
    col1, col2, col3 = st.columns(3)
    with col1:
        somatotipo = st.selectbox("Somatotipo", ["mesomorfo", "endomorfo", "ectomorfo"], key=f"soma_{seccion}")
        higiene = st.selectbox("Higiene", ["adecuado", "regular", "malo"], key=f"hig_{seccion}")
        actitud = st.selectbox("Actitud", ["cooperador", "hostil", "indiferente"], key=f"act_{seccion}")
    with col2:
        discurso = st.selectbox("Discurso", ["coherente", "disgregado"], key=f"disc_{seccion}")
        pensamiento = st.selectbox("Pensamiento", ["lógico", "desorganizado"], key=f"pens_{seccion}")
        contenido = st.text_input("Contenido", value="niega delirios", key=f"cont_{seccion}")
    with col3:
        animo = st.text_input("Ánimo (entre comillas)", value="tranquilo", key=f"anim_{seccion}")
        impresion = st.selectbox("Impresión", ["eutímico", "disfórico", "ansioso"], key=f"imp_{seccion}")
        juicio = st.selectbox("Juicio", ["conservado", "desviado"], key=f"jui_{seccion}")
        conciencia = st.selectbox("Conciencia", ["adecuada", "parcial"], key=f"conc_{seccion}")
    
    # Plantilla EXACTA del prompt
    return f"Paciente de edad aparente similar a la cronológica con somatotipo {somatotipo}, con {higiene} estado de higiene; sin movimientos anormales. Alerta, {actitud}, reactivo. Orientado en 3 esferas. Discurso {discurso}. Pensamiento {pensamiento}. Contenido: {contenido}. Niega ideación suicida. Ánimo “{animo}”, impresiona {impresion}. Juicio {juicio}. Conciencia enfermedad {conciencia}."

# --- INTERFAZ ---
st.title("🏥 Asistente Clínico IMSS (Regla ECE)")

with st.sidebar:
    st.header("Datos Paciente")
    nombre = st.text_input("Nombre Completo", "NOMBRE PACIENTE")
    edad = st.number_input("Edad", 18)
    fecha_ingreso = st.date_input("Fecha Ingreso (Día 0)")
    
    # Cálculo días estancia
    hoy = date.today()
    dias = (hoy - fecha_ingreso).days
    st.metric("Días Estancia", f"{dias} días")
    
    dx = st.text_area("Diagnóstico (Separar con +)", "F200 Esquizofrenia paranoide + F102 Trastorno por consumo de alcohol")

tab1, tab2, tab3 = st.tabs(["🟦 NOTA INGRESO", "🟦 NOTA EVOLUCIÓN", "🟦 NOTA EGRESO (CÁLCULO)"])

# --- TAB 1: INGRESO ---
with tab1:
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        hora_ingreso = st.time_input("Hora", value=datetime.now().time())
        motivo = st.text_area("Motivo de Consulta")
        pad = st.text_area("Padecimiento Actual (Narrativa técnica)")
    with col_i2:
        ant = st.text_area("Antecedentes (Heredofamiliares, Patológicos, Toxis)")
        
    ment1 = generar_examen_mental("ingreso")
    ana1 = st.text_area("Análisis (Justificación riesgo/internamiento)")
    plan1 = st.text_area("Plan Inicial (Labs y medidas)")
    
    if st.button("Generar Nota Ingreso", key="btn_ingreso"):
        nota_ingreso = f"""
**Nota de Ingreso a Psiquiatría.**
Fecha: {fecha_ingreso.strftime('%d/%m/%Y')} | Hora: {hora_ingreso.strftime('%H:%M')}
Paciente: {nombre} | Edad: {edad}
Motivo: {motivo} | DX: {dx}

**PADECIMIENTO ACTUAL:**
{pad}

**ANTECEDENTES:**
{ant}

**EXAMEN MENTAL:**
{ment1}

**ANÁLISIS:**
{ana1}

**PLAN INICIAL:**
{plan1}
"""
        st.code(nota_ingreso, language="markdown")

# --- TAB 2: EVOLUCIÓN ---
with tab2:
    st.info(f"Nota para el día: {hoy.strftime('%d/%m/%Y')}")
    col_ev1, col_ev2 = st.columns(2)
    with col_ev1:
        subj = st.text_area("Subjetivo (Prosa clínica)")
    with col_ev2:
        obj = st.text_input("Objetivo: Signos", "TA: 120/80, FC: 70, FR: 18, Temp: 36.5")
    
    ment2 = generar_examen_mental("evolucion")
    ana2 = st.text_area("Análisis (Evolución, tolerancia)")
    
    st.write("Plan:")
    p_dieta = st.text_input("1. Dieta y cuidados", "Dieta Normal.")
    p_meds = st.text_input("2. Medicamentos (Línea separada por +)", "Sin cambios")
    p_seguridad = st.text_input("3. Medidas seguridad", "Vigilancia estrecha")

    if st.button("Generar Nota Evolución", key="btn_evol"):
        nota_evol = f"""
**NOTA DE EVOLUCIÓN del día {hoy.strftime('%d/%m/%Y')}**
Paciente {nombre} |de {edad} años, cursando el {dias} día de estancia, con diagnósticos: {dx}.

**SUBJETIVO:**
{subj}

**OBJETIVO:**
Signos: {obj}

**EXAMEN MENTAL:**
{ment2}

**ANÁLISIS:**
{ana2}

**PLAN:**
1. {p_dieta}
2. Medicamentos: {p_meds}
3. {p_seguridad}
"""
        st.code(nota_evol, language="markdown")

# --- TAB 3: EGRESO Y CÁLCULO ECE ---
with tab3:
    st.warning("⚠️ REGLA DE ORO: 1 MEDICAMENTO = 1 RECETA FÍSICA")
    resumen = st.text_area("Resumen (Síntesis ingreso-egreso)")
    ment3 = generar_examen_mental("egreso")
    ana3 = st.text_area("Análisis (Criterios de alta)")

    st.markdown("---")
    st.subheader("💊 Calculadora de Abasto ECE")
    
    if 'meds_egreso' not in st.session_state: st.session_state.meds_egreso = []

    with st.form("ece_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            fco_select = st.selectbox("Fármaco Base ECE", list(ece_db.keys()))
        with c2:
            dosis_diaria = st.number_input("Dosis diaria total (mg)", min_value=0.0, step=0.5)
        with c3:
            frecuencia_txt = st.text_input("Frecuencia (texto)", "cada 24 horas")
            
        add_btn = st.form_submit_button("Agregar a Receta")

        if add_btn:
            # DATOS DE LA BASE ECE
            data = ece_db[fco_select]
            piezas_caja = data[0]
            limite_receta = data[1]
            pres_txt = data[2]
            mg_unitario = data[3] # Dato numérico exacto para evitar errores de parseo

            # ALGORITMO MATEMÁTICO DEL PROMPT
            # Paso 1: Consumo mensual
            # Primero calculamos cuántas pastillas al día. Ej: 4mg dosis / 2mg tab = 2 tabs.
            if mg_unitario > 0:
                tabs_diarias = dosis_diaria / mg_unitario
            else:
                tabs_diarias = 0
            
            total_tabletas_mes = tabs_diarias * 30
            
            # Paso 2: Cajas (Redondeo hacia arriba)
            total_cajas_mes = math.ceil(total_tabletas_mes / piezas_caja)
            
            # Paso 3: Recetas
            total_recetas = math.ceil(total_cajas_mes / limite_receta)

            # Formato de salida estricto
            # [NOMBRE] [DOSIS] [PRESENTACIÓN] VO a razón de [FRECUENCIA] ([TOTAL TABS]/mes) por 12 meses ([TOTAL CAJAS] cajas/mes; [TOTAL RECETAS] recetas mensuales).
            linea_receta = (
                f"- **{fco_select} {pres_txt} VO a razón de {frecuencia_txt} "
                f"({int(total_tabletas_mes)} tabletas/mes) por 12 meses "
                f"({total_cajas_mes} cajas/mes; {total_recetas} recetas mensuales).**"
            )
            
            st.session_state.meds_egreso.append(linea_receta)
            st.rerun()

    if st.session_state.meds_egreso:
        st.markdown("##### Previsualización Tratamiento:")
        for m in st.session_state.meds_egreso:
            st.markdown(m)
        if st.button("Borrar Tratamiento", key="del_trat"):
            st.session_state.meds_egreso = []
            st.rerun()

    if st.button("Generar Nota Egreso Final", key="btn_egreso_final"):
        bloque_recetas = "\n".join(st.session_state.meds_egreso)
        if not bloque_recetas: bloque_recetas = "[DATO PENDIENTE - AGREGAR FÁRMACOS]"
        
        nota_egreso = f"""
**Nota de Egreso Hospitalario.**
Fecha: {hoy.strftime('%d/%m/%Y')}
Paciente: {nombre} | Estancia total: {dias} días
Diagnóstico Final: {dx}

**RESUMEN:**
{resumen}

**EXAMEN MENTAL AL ALTA:**
{ment3}

**ANÁLISIS:**
{ana3}

**TRATAMIENTO DE SOSTÉN (LOGÍSTICA DE RECETAS):**
*Instrucción para MF: Elaborar una receta individual por cada psicofármaco.*

{bloque_recetas}

**PLAN DE ALTA:**
1. ALTA PSIQUIATRÍA HOSPITALIZACIÓN.
2. CONTINUA CON APOYO DE SU MÉDICO FAMILIAR PARA TRASCRIPCIÓN.
3. ENVÍO A CONSULTA EXTERNA (FORMATO 4-30-8) EN 1-2 MESES.
4. URGENCIAS SI: Ideas suicidas/homicidas, psicosis, agresividad o efectos adversos graves.
5. Este documento es únicamente para uso interno del IMSS y carece de valor para su uso externo y para fines legales.
"""
        st.code(nota_egreso, language="markdown")
        
