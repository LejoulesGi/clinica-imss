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
def generar_examen_mental():
    st.subheader("🧠 Examen Mental")
    col1, col2, col3 = st.columns(3)
    with col1:
        somatotipo = st.selectbox("Somatotipo", ["mesomorfo", "endomorfo", "ectomorfo"])
        higiene = st.selectbox("Higiene", ["adecuado", "regular", "malo"])
        actitud = st.selectbox("Actitud", ["cooperador", "hostil", "indiferente"])
    with col2:
        discurso = st.selectbox("Discurso", ["coherente", "disgregado"])
        pensamiento = st.selectbox("Pensamiento", ["lógico", "desorganizado"])
        contenido = st.text_input("Contenido", value="niega delirios")
    with col3:
        animo = st.text_input("Ánimo", value="tranquilo")
        impresion = st.selectbox("Impresión", ["eutímico", "disfórico", "ansioso"])
        juicio = st.selectbox("Juicio", ["conservado", "desviado"])
        conciencia = st.selectbox("Conciencia", ["adecuada", "parcial", "nula"])
    return f"Paciente de edad aparente similar a la cronológica con somatotipo {somatotipo}, con {higiene} estado de higiene; sin movimientos anormales. Alerta, {actitud}, reactivo. Orientado en 3 esferas. Discurso {discurso}. Pensamiento {pensamiento}. Contenido: {contenido}. Niega ideación suicida. Ánimo “{animo}”, impresiona {impresion}. Juicio {juicio}. Conciencia enfermedad {conciencia}."

# --- INTERFAZ ---
st.title("🏥 Gestión Clínica IMSS")

with st.sidebar:
    nombre = st.text_input("Paciente", "Nombre Apellido")
    edad = st.number_input("Edad", 18)
    fecha_ingreso = st.date_input("Ingreso")
    dias = (date.today() - fecha_ingreso).days
    st.metric("Estancia", f"{dias} días")
    dx = st.text_area("Diagnóstico", "F200...")

tab1, tab2, tab3 = st.tabs(["Ingreso", "Evolución", "Egreso/Recetas"])

with tab1:
    motivo = st.text_area("Motivo")
    pad = st.text_area("Padecimiento")
    ant = st.text_area("Antecedentes")
    ment1 = generar_examen_mental()
    ana1 = st.text_area("Análisis Ingreso")
    plan1 = st.text_area("Plan Ingreso")
    if st.button("Generar Nota Ingreso"):
        st.code(f"NOTA DE INGRESO\nPaciente: {nombre}\nMotivo: {motivo}\nDX: {dx}\nPADECIMIENTO: {pad}\nANTECEDENTES: {ant}\nEXAMEN MENTAL: {ment1}\nANÁLISIS: {ana1}\nPLAN: {plan1}")

with tab2:
    subj = st.text_area("Subjetivo")
    obj = st.text_input("Signos", "TA: 120/80...")
    ment2 = generar_examen_mental()
    ana2 = st.text_area("Análisis Evol")
    plan_txt = st.text_area("Plan (1. Dieta, 2. Meds, 3. Seguridad)")
    if st.button("Generar Nota Evolución"):
        st.code(f"NOTA EVOLUCIÓN\nPaciente: {nombre} ({dias} días)\nSUBJETIVO: {subj}\nOBJETIVO: {obj}\nMENTAL: {ment2}\nANÁLISIS: {ana2}\nPLAN: {plan_txt}")

with tab3:
    resumen = st.text_area("Resumen")
    ment3 = generar_examen_mental()
    ana3 = st.text_area("Análisis Alta")
    
    st.subheader("💊 Calculadora ECE")
    if 'meds' not in st.session_state: st.session_state.meds = []
    
    with st.form("calc"):
        m = st.selectbox("Fármaco", list(ece_db.keys()))
        d = st.number_input("Dosis (mg)", 0.0)
        f = st.text_input("Frecuencia", "cada 24 h")
        if st.form_submit_button("Agregar"):
            info = ece_db[m]
            try: mg_f = float([x for x in m.split() if x.replace('.','',1).isdigit()][0])
            except: mg_f = 1
            cajas = math.ceil((d/mg_f*30)/info[0])
            recetas = math.ceil(cajas/info[1])
            st.session_state.meds.append(f"{m} {info[2]} VO {f} ({int(d/mg_f*30)} tabs/mes) ({cajas} cajas, {recetas} recetas)")
            st.rerun()
            
    if st.session_state.meds:
        for i in st.session_state.meds: st.write(f"- {i}")
        if st.button("Borrar Todo"):
            st.session_state.meds = []
            st.rerun()

    if st.button("Generar Egreso"):
        recetas_txt = "\n".join(st.session_state.meds)
        st.code(f"NOTA EGRESO\nResumen: {resumen}\nMental: {ment3}\nAnálisis: {ana3}\nRECETAS:\n{recetas_txt}\nPLAN ALTA:\n1. Alta Psiquiatría\n2. Control MF\n3. Urgencias SOS")

