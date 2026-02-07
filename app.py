import streamlit as st
import math
from datetime import date, datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Asistente Clínico IMSS", layout="wide")

# --- BASE DE DATOS ECE ---
ece_db = {
    "Alprazolam 2 mg": [30, 1, "30 tabletas"],
    "Alprazolam 0.5 mg": [30, 1, "30 tabletas"],
    "Alprazolam 0.25 mg": [30, 2, "30 tabletas"],
    "Amitriptilina 25 mg": [30, 3, "30 tabletas"],
    "Anfebutamona 150 mg": [30, 2, "30 tabletas"],
    "Biperideno 2 mg": [50, 2, "50 tabletas"],
    "Bromazepam 3 mg": [30, 2, "30 tabletas"],
    "Carbamazepina 200 mg": [20, 6, "20 tabletas"],
    "Citalopram 20 mg": [14, 2, "14 tabletas"],
    "Diazepam 10 mg": [20, 2, "20 tabletas"],
    "Escitalopram 10 mg": [28, 2, "28 tabletas"],
    "Fluoxetina 20 mg": [14, 2, "14 tabletas"],
    "Gabapentina 300 mg": [15, 4, "15 tabletas"],
    "Haloperidol 5 mg": [20, 4, "20 tabletas"],
    "Hidroxizina 10 mg": [30, 1, "30 tabletas"],
    "Imipramina 25 mg": [20, 3, "20 tabletas"],
    "Lamotrigina 25 mg": [28, 2, "28 tabletas"],
    "Lamotrigina 100 mg": [28, 2, "28 tabletas"],
    "Litio 300 mg": [50, 2, "50 tabletas"],
    "Levomepromazina 25 mg": [20, 2, "20 tabletas"],
    "Lorazepam 1 mg": [40, 1, "40 tabletas"],
    "Metilfenidato 10 mg": [30, 5, "30 tabletas"],
    "Olanzapina 10 mg": [28, 2, "28 tabletas"],
    "Paroxetina 20 mg": [10, 6, "10 tabletas"],
    "Primidona 250 mg": [50, 2, "50 tabletas"],
    "Quetiapina 100 mg": [60, 3, "60 tabletas"],
    "Risperidona 2 mg": [40, 1, "40 tabletas"],
    "Sertralina 50 mg": [14, 2, "14 tabletas"],
    "Topiramato 100 mg": [60, 2, "60 tabletas"],
    "Topiramato 25 mg": [60, 1, "60 tabletas"],
    "Trifluoperazina 20 mg": [20, 3, "20 tabletas"],
    "Trihexifenidilo 5 mg": [50, 1, "50 tabletas"],
    "Valproato Mag 200 mg": [40, 6, "40 tabletas"],
    "Valproato Mag 600 mg": [30, 3, "30 tabletas"],
    "Valproato Semi 250 mg": [30, 3, "30 tabletas"],
    "Venlafaxina 75 mg": [10, 6, "10 tabletas"],
    "Pregabalina 75 mg": [28, 1, "28 cápsulas"],
    "Pregabalina 150 mg": [28, 1, "28 cápsulas"],
    "Oxcarbazepina 600 mg": [30, 3, "30 tabletas"]
}

# --- FUNCIONES ---
# La corrección está aquí: añadimos 'seccion' para crear IDs únicos
def generar_examen_mental(seccion):
    st.subheader(f"🧠 Examen Mental ({seccion})")
    col1, col2, col3 = st.columns(3)
    with col1:
        # Usamos key=f"nombre_{seccion}" para que no choquen
        somatotipo = st.selectbox("Somatotipo", ["mesomorfo", "endomorfo", "ectomorfo"], key=f"soma_{seccion}")
        higiene = st.selectbox("Higiene", ["adecuado", "regular", "malo"], key=f"hig_{seccion}")
        actitud = st.selectbox("Actitud", ["cooperador", "hostil", "indiferente"], key=f"act_{seccion}")
    with col2:
        discurso = st.selectbox("Discurso", ["coherente", "disgregado"], key=f"disc_{seccion}")
        pensamiento = st.selectbox("Pensamiento", ["lógico", "desorganizado"], key=f"pens_{seccion}")
        contenido = st.text_input("Contenido", value="niega delirios", key=f"cont_{seccion}")
    with col3:
        animo = st.text_input("Ánimo", value="tranquilo", key=f"anim_{seccion}")
        impresion = st.selectbox("Impresión", ["eutímico", "disfórico", "ansioso"], key=f"imp_{seccion}")
        juicio = st.selectbox("Juicio", ["conservado", "desviado"], key=f"jui_{seccion}")
        conciencia = st.selectbox("Conciencia", ["adecuada", "parcial", "nula"], key=f"conc_{seccion}")
    
    return f"Paciente de edad aparente similar a la cronológica con somatotipo {somatotipo}, con {higiene} estado de higiene; sin movimientos anormales. Alerta, {actitud}, reactivo. Orientado en 3 esferas. Discurso {discurso}. Pensamiento {pensamiento}. Contenido: {contenido}. Niega ideación suicida. Ánimo “{animo}”, impresiona {impresion}. Juicio {juicio}. Conciencia enfermedad {conciencia}."

# --- INTERFAZ ---
st.title("🏥 Gestión Clínica IMSS")

with st.sidebar:
    st.header("Datos Paciente")
    nombre = st.text_input("Nombre Completo", "Nombre Apellido")
    edad = st.number_input("Edad", 18)
    fecha_ingreso = st.date_input("Fecha Ingreso")
    dias = (date.today() - fecha_ingreso).days
    st.metric("Días Estancia", f"{dias} días")
    dx = st.text_area("Diagnósticos", "F200 Esquizofrenia paranoide + F102 Alcoholismo")

tab1, tab2, tab3 = st.tabs(["Ingreso", "Evolución", "Egreso/Recetas"])

# --- TAB 1: INGRESO ---
with tab1:
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        motivo = st.text_area("Motivo Consulta")
        pad = st.text_area("Padecimiento Actual")
    with col_i2:
        ant = st.text_area("Antecedentes")
    
    # Llamamos a la función con la llave "ingreso"
    ment1 = generar_examen_mental("ingreso")
    
    ana1 = st.text_area("Análisis Ingreso")
    plan1 = st.text_area("Plan Inicial")
    
    if st.button("Generar Nota Ingreso", key="btn_ingreso"):
        nota = f"""
**NOTA DE INGRESO**
Fecha: {date.today()}
Paciente: {nombre} | Edad: {edad}
Motivo: {motivo} | DX: {dx}

**PADECIMIENTO:** {pad}
**ANTECEDENTES:** {ant}
**MENTAL:** {ment1}
**ANÁLISIS:** {ana1}
**PLAN:** {plan1}
"""
        st.code(nota, language="markdown")

# --- TAB 2: EVOLUCIÓN ---
with tab2:
    subj = st.text_area("Subjetivo")
    obj = st.text_input("Signos Vitales", "TA: 120/80 FC: 80 FR: 20 T: 36.5")
    
    # Llamamos a la función con la llave "evolucion"
    ment2 = generar_examen_mental("evolucion")
    
    ana2 = st.text_area("Análisis Evolución")
    plan_txt = st.text_area("Plan (Dieta, Meds, Seguridad)")
    
    if st.button("Generar Nota Evolución", key="btn_evol"):
        nota = f"""
**NOTA EVOLUCIÓN**
Paciente: {nombre} | Estancia: {dias} días
**SUBJETIVO:** {subj}
**OBJETIVO:** {obj}
**MENTAL:** {ment2}
**ANÁLISIS:** {ana2}
**PLAN:** {plan_txt}
"""
        st.code(nota, language="markdown")

# --- TAB 3: EGRESO ---
with tab3:
    resumen = st.text_area("Resumen Clínico")
    
    # Llamamos a la función con la llave "egreso"
    ment3 = generar_examen_mental("egreso")
    
    ana3 = st.text_area("Análisis Alta")
    
    st.subheader("💊 Calculadora ECE")
    if 'meds' not in st.session_state: st.session_state.meds = []
    
    with st.form("calc_form"):
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            m = st.selectbox("Fármaco", list(ece_db.keys()))
        with col_c2:
            d = st.number_input("Dosis (mg)", 0.0)
        with col_c3:
            f = st.text_input("Frecuencia", "cada 24 h")
            
        add = st.form_submit_button("Agregar Medicamento")
        
        if add:
            info = ece_db[m]
            try: mg_f = float([x for x in m.split() if x.replace('.','',1).isdigit()][0])
            except: mg_f = 1
            
            # Cálculo
            total_tabs = (d / mg_f) * 30
            cajas = math.ceil(total_tabs / info[0])
            recetas = math.ceil(cajas / info[1])
            
            # Guardar
            texto_med = f"{m} ({info[2]}) VO {f} ({int(total_tabs)} tabs/mes) ({cajas} cajas/mes, {recetas} recetas)"
            st.session_state.meds.append(texto_med)
            st.rerun()
            
    if st.session_state.meds:
        st.write("---")
        st.write("**Esquema Actual:**")
        for i in st.session_state.meds: st.write(f"- {i}")
        if st.button("Borrar Lista", key="btn_clear"):
            st.session_state.meds = []
            st.rerun()

    if st.button("Generar Nota Egreso", key="btn_egreso"):
        recetas_txt = "\n".join([f"- {x}" for x in st.session_state.meds])
        nota = f"""
**NOTA DE EGRESO**
Paciente: {nombre} | Estancia: {dias} días
DX: {dx}

**RESUMEN:** {resumen}
**MENTAL ALTA:** {ment3}
**ANÁLISIS:** {ana3}

**TRATAMIENTO (RECETAS):**
{recetas_txt if recetas_txt else "[SIN FÁRMACOS]"}

**PLAN ALTA:**
1. Alta a domicilio.
2. Control MF.
3. Urgencias por datos de alarma.
"""
        st.code(nota, language="markdown")
        
