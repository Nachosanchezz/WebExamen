"""
APP DE ESTUDIO — Examen Planificación y Gestión de Proyectos
Sistema de tests para Finanzas (Javier) + Gestión de Proyectos (Gustavo)

Ejecutar:
    streamlit run app.py

Requisitos:
    pip install streamlit
"""

import streamlit as st
import json
import os
import random
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

st.set_page_config(
    page_title="Examen Preparación",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_DIR = Path(__file__).parent / "data"
PROGRESS_FILE = Path(__file__).parent / "progreso.json"

# ============================================================================
# CARGA DE DATOS
# ============================================================================

@st.cache_data
def cargar_preguntas(archivo):
    """Carga las preguntas desde un archivo JSON."""
    ruta = DATA_DIR / archivo
    if not ruta.exists():
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def cargar_todas_preguntas():
    """Carga todos los bancos de preguntas."""
    finanzas = cargar_preguntas("preguntas_finanzas.json")
    gp = cargar_preguntas("preguntas_gestion_proyectos.json")
    mixtas = cargar_preguntas("preguntas_mixtas.json")

    # Etiquetar el bloque de cada pregunta
    for p in finanzas:
        p["bloque"] = "Finanzas"
    for p in gp:
        p["bloque"] = "Gestión de Proyectos"
    for p in mixtas:
        p["bloque"] = "Mixto"

    return finanzas, gp, mixtas


# ============================================================================
# PERSISTENCIA DE PROGRESO
# ============================================================================

def cargar_progreso():
    """Carga el progreso del usuario desde disco."""
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "historial": [],          # Lista de tests realizados
        "preguntas_falladas": [],  # IDs de preguntas falladas
        "preguntas_acertadas": [], # IDs de preguntas acertadas
    }


def guardar_progreso(progreso):
    """Guarda el progreso en disco."""
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(progreso, f, ensure_ascii=False, indent=2)
    except IOError as e:
        st.warning(f"No se pudo guardar el progreso: {e}")


# ============================================================================
# ESTADO DE SESIÓN
# ============================================================================

def inicializar_estado():
    """Inicializa el estado de Streamlit."""
    defaults = {
        "test_activo": False,
        "preguntas_actuales": [],
        "indice_actual": 0,
        "respuestas_usuario": {},  # {id_pregunta: indice_respuesta}
        "test_finalizado": False,
        "progreso": cargar_progreso(),
        "config_test": {},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


inicializar_estado()


# ============================================================================
# FUNCIONES DE LÓGICA
# ============================================================================

def filtrar_preguntas(preguntas, dificultades=None, solo_falladas=False, ids_falladas=None):
    """Aplica filtros al banco de preguntas."""
    resultado = preguntas.copy()
    if dificultades:
        resultado = [p for p in resultado if p["dificultad"] in dificultades]
    if solo_falladas and ids_falladas:
        resultado = [p for p in resultado if p["id"] in ids_falladas]
    return resultado


def iniciar_test(preguntas, num_preguntas, config):
    """Inicia un nuevo test con preguntas aleatorias."""
    if len(preguntas) == 0:
        st.error("No hay preguntas disponibles con esos filtros.")
        return

    n = min(num_preguntas, len(preguntas))
    seleccionadas = random.sample(preguntas, n)

    st.session_state.preguntas_actuales = seleccionadas
    st.session_state.indice_actual = 0
    st.session_state.respuestas_usuario = {}
    st.session_state.test_activo = True
    st.session_state.test_finalizado = False
    st.session_state.config_test = config


def finalizar_test():
    """Marca el test como finalizado y actualiza el progreso."""
    st.session_state.test_finalizado = True
    st.session_state.test_activo = False

    # Actualizar progreso persistente
    progreso = st.session_state.progreso
    aciertos = 0
    total = len(st.session_state.preguntas_actuales)
    ids_falladas_test = []
    ids_acertadas_test = []

    for pregunta in st.session_state.preguntas_actuales:
        id_p = pregunta["id"]
        respuesta = st.session_state.respuestas_usuario.get(id_p)
        if respuesta is not None and respuesta == pregunta["correcta"]:
            aciertos += 1
            ids_acertadas_test.append(id_p)
            if id_p in progreso["preguntas_falladas"]:
                progreso["preguntas_falladas"].remove(id_p)
            if id_p not in progreso["preguntas_acertadas"]:
                progreso["preguntas_acertadas"].append(id_p)
        else:
            ids_falladas_test.append(id_p)
            if id_p not in progreso["preguntas_falladas"]:
                progreso["preguntas_falladas"].append(id_p)

    # Añadir al historial
    progreso["historial"].append({
        "fecha": datetime.now().isoformat(),
        "config": st.session_state.config_test,
        "aciertos": aciertos,
        "total": total,
        "porcentaje": round(aciertos / total * 100, 1) if total > 0 else 0,
    })
    guardar_progreso(progreso)


def reiniciar_test():
    """Resetea el estado para empezar un test nuevo."""
    st.session_state.test_activo = False
    st.session_state.test_finalizado = False
    st.session_state.preguntas_actuales = []
    st.session_state.indice_actual = 0
    st.session_state.respuestas_usuario = {}


# ============================================================================
# UI: SIDEBAR
# ============================================================================

with st.sidebar:
    st.title("📚 Examen Prep")
    st.markdown("**Planificación y Gestión de Proyectos**")
    st.markdown("---")

    if st.session_state.test_activo or st.session_state.test_finalizado:
        if st.button("🔄 Volver al menú", use_container_width=True):
            reiniciar_test()
            st.rerun()

    st.markdown("### 📊 Estadísticas")
    progreso = st.session_state.progreso
    n_acertadas = len(progreso["preguntas_acertadas"])
    n_falladas = len(progreso["preguntas_falladas"])
    n_total = n_acertadas + n_falladas

    if n_total > 0:
        st.metric("Preguntas vistas", n_total)
        st.metric("Acertadas (únicas)", n_acertadas)
        st.metric("Falladas pendientes", n_falladas)
        if len(progreso["historial"]) > 0:
            ult = progreso["historial"][-1]
            st.metric("Última nota", f"{ult['porcentaje']}%",
                     f"{ult['aciertos']}/{ult['total']}")
    else:
        st.info("Haz tu primer test para ver estadísticas")

    if st.button("🗑️ Borrar progreso", use_container_width=True):
        st.session_state.progreso = {
            "historial": [],
            "preguntas_falladas": [],
            "preguntas_acertadas": [],
        }
        guardar_progreso(st.session_state.progreso)
        st.success("Progreso borrado")
        st.rerun()


# ============================================================================
# UI: MENÚ PRINCIPAL
# ============================================================================

if not st.session_state.test_activo and not st.session_state.test_finalizado:
    st.title("📚 Sistema de estudio para el examen")
    st.markdown("*Planificación y Gestión de Proyectos — Finanzas (Javier) + Gestión (Gustavo)*")

    # Cargar bancos
    finanzas, gp, mixtas = cargar_todas_preguntas()
    total_disponibles = len(finanzas) + len(gp) + len(mixtas)

    if total_disponibles == 0:
        st.error("⚠️ No se encontraron preguntas. Verifica que los archivos JSON existan en `data/`.")
        st.stop()

    col1, col2, col3 = st.columns(3)
    col1.metric("Finanzas", len(finanzas))
    col2.metric("Gestión Proyectos", len(gp))
    col3.metric("Mixtas", len(mixtas))

    st.markdown("---")
    st.markdown("### ⚙️ Configura tu test")

    col1, col2 = st.columns(2)

    with col1:
        modo = st.selectbox(
            "🎯 Tipo de test",
            options=[
                "Mixto (Finanzas + Gestión)",
                "Solo Finanzas",
                "Solo Gestión de Proyectos",
                "Repaso: solo preguntas falladas",
            ],
        )

        dificultades = st.multiselect(
            "📊 Dificultad",
            options=["facil", "medio", "dificil"],
            default=["facil", "medio", "dificil"],
            format_func=lambda x: {"facil": "Fácil", "medio": "Medio", "dificil": "Difícil"}[x],
        )

    with col2:
        num_preguntas = st.slider("📝 Nº de preguntas", 5, 50, 20, 5)

        modo_revision = st.radio(
            "👁️ Cuándo ver la respuesta",
            options=[
                "Al final del test",
                "Después de cada pregunta",
            ],
            help="'Al final' simula un examen real. 'Después de cada' es modo aprendizaje."
        )

    st.markdown("---")

    # Construir banco según modo
    if modo == "Solo Finanzas":
        banco = finanzas
    elif modo == "Solo Gestión de Proyectos":
        banco = gp
    elif modo == "Repaso: solo preguntas falladas":
        todas = finanzas + gp + mixtas
        ids_falladas = progreso["preguntas_falladas"]
        banco = [p for p in todas if p["id"] in ids_falladas]
        if not banco:
            st.info("🎉 ¡No tienes preguntas falladas pendientes! Haz un test normal primero.")
    else:  # Mixto
        banco = finanzas + gp + mixtas

    # Aplicar filtro de dificultad
    banco_filtrado = filtrar_preguntas(banco, dificultades=dificultades)

    if len(banco_filtrado) > 0:
        st.success(f"📋 **{len(banco_filtrado)}** preguntas disponibles con los filtros actuales")
    else:
        st.warning("⚠️ No hay preguntas con esos filtros. Ajusta la dificultad.")

    if st.button("🚀 Comenzar test", type="primary", use_container_width=True,
                 disabled=len(banco_filtrado) == 0):
        config = {
            "modo": modo,
            "dificultades": dificultades,
            "num_preguntas": num_preguntas,
            "modo_revision": modo_revision,
        }
        iniciar_test(banco_filtrado, num_preguntas, config)
        st.rerun()

    # Sección de progreso histórico
    if len(progreso["historial"]) > 0:
        st.markdown("---")
        with st.expander("📈 Historial de tests"):
            for i, t in enumerate(reversed(progreso["historial"][-10:])):
                fecha = datetime.fromisoformat(t["fecha"]).strftime("%d/%m %H:%M")
                emoji = "🟢" if t["porcentaje"] >= 70 else "🟡" if t["porcentaje"] >= 50 else "🔴"
                st.write(f"{emoji} **{fecha}** — {t['config']['modo']} — "
                        f"{t['aciertos']}/{t['total']} ({t['porcentaje']}%)")


# ============================================================================
# UI: TEST EN CURSO
# ============================================================================

elif st.session_state.test_activo:
    preguntas = st.session_state.preguntas_actuales
    idx = st.session_state.indice_actual
    total = len(preguntas)
    pregunta = preguntas[idx]

    # Barra de progreso
    st.progress((idx + 1) / total, text=f"Pregunta {idx + 1} de {total}")

    # Información lateral
    col_meta1, col_meta2, col_meta3 = st.columns(3)
    col_meta1.caption(f"🏷️ **Bloque**: {pregunta.get('bloque', '-')}")
    col_meta2.caption(f"📚 **Tema**: {pregunta['tema']}")
    col_meta3.caption(f"📊 **Dificultad**: {pregunta['dificultad'].capitalize()}")

    st.markdown("---")
    st.markdown(f"### {pregunta['pregunta']}")

    # Opciones
    opciones = pregunta["opciones"]
    respuesta_actual = st.session_state.respuestas_usuario.get(pregunta["id"])

    labels = [f"**{chr(65+i)})** {opt}" for i, opt in enumerate(opciones)]

    eleccion = st.radio(
        "Selecciona tu respuesta:",
        options=range(len(opciones)),
        format_func=lambda i: labels[i],
        index=respuesta_actual if respuesta_actual is not None else None,
        key=f"radio_{pregunta['id']}",
        label_visibility="collapsed",
    )

    if eleccion is not None:
        st.session_state.respuestas_usuario[pregunta["id"]] = eleccion

    # Modo aprendizaje: mostrar explicación después de responder
    modo_revision = st.session_state.config_test.get("modo_revision", "Al final del test")
    if modo_revision == "Después de cada pregunta" and eleccion is not None:
        st.markdown("---")
        if eleccion == pregunta["correcta"]:
            st.success(f"✅ **Correcto** — {chr(65 + pregunta['correcta'])}) {opciones[pregunta['correcta']]}")
        else:
            st.error(f"❌ **Incorrecto**. La respuesta correcta es **{chr(65 + pregunta['correcta'])})** {opciones[pregunta['correcta']]}")
        with st.expander("💡 Explicación"):
            st.write(pregunta["explicacion"])

    # Navegación
    st.markdown("---")
    col_n1, col_n2, col_n3 = st.columns([1, 1, 1])

    with col_n1:
        if idx > 0:
            if st.button("⬅️ Anterior", use_container_width=True):
                st.session_state.indice_actual -= 1
                st.rerun()

    with col_n3:
        if idx < total - 1:
            if st.button("Siguiente ➡️", use_container_width=True, type="primary"):
                st.session_state.indice_actual += 1
                st.rerun()
        else:
            n_respondidas = len(st.session_state.respuestas_usuario)
            if st.button(f"🏁 Finalizar test ({n_respondidas}/{total} respondidas)",
                         use_container_width=True, type="primary"):
                finalizar_test()
                st.rerun()


# ============================================================================
# UI: RESULTADOS
# ============================================================================

elif st.session_state.test_finalizado:
    preguntas = st.session_state.preguntas_actuales
    respuestas = st.session_state.respuestas_usuario

    # Calcular nota
    aciertos = sum(
        1 for p in preguntas
        if respuestas.get(p["id"]) is not None and respuestas[p["id"]] == p["correcta"]
    )
    total = len(preguntas)
    porcentaje = (aciertos / total * 100) if total > 0 else 0
    nota_10 = porcentaje / 10

    # Determinar emoji y mensaje
    if porcentaje >= 90:
        emoji, msg = "🏆", "¡Excelente!"
        color = "green"
    elif porcentaje >= 70:
        emoji, msg = "🎉", "¡Muy bien!"
        color = "green"
    elif porcentaje >= 50:
        emoji, msg = "✅", "Aprobado"
        color = "orange"
    else:
        emoji, msg = "💪", "Hay que estudiar más"
        color = "red"

    st.title(f"{emoji} Resultados del test")
    st.markdown(f"### {msg}")

    col_r1, col_r2, col_r3 = st.columns(3)
    col_r1.metric("Aciertos", f"{aciertos} / {total}")
    col_r2.metric("Porcentaje", f"{porcentaje:.1f}%")
    col_r3.metric("Nota", f"{nota_10:.1f} / 10")

    st.markdown("---")

    # Revisión pregunta a pregunta
    st.markdown("### 📝 Revisión")

    filtro = st.radio(
        "Mostrar:",
        ["Todas", "Solo falladas", "Solo acertadas"],
        horizontal=True,
    )

    for i, pregunta in enumerate(preguntas):
        respuesta = respuestas.get(pregunta["id"])
        es_correcta = respuesta is not None and respuesta == pregunta["correcta"]

        if filtro == "Solo falladas" and es_correcta:
            continue
        if filtro == "Solo acertadas" and not es_correcta:
            continue

        emoji_p = "✅" if es_correcta else "❌"
        bloque = pregunta.get("bloque", "")

        with st.expander(f"{emoji_p} **Pregunta {i+1}** — {bloque} | {pregunta['tema']}"):
            st.markdown(f"**{pregunta['pregunta']}**")
            st.markdown("")
            for j, opt in enumerate(pregunta["opciones"]):
                letra = chr(65 + j)
                if j == pregunta["correcta"]:
                    st.markdown(f"✔️ **{letra}) {opt}** *(correcta)*")
                elif j == respuesta:
                    st.markdown(f"❌ **{letra}) {opt}** *(tu respuesta)*")
                else:
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{letra}) {opt}")
            st.markdown("")
            st.info(f"💡 **Explicación**: {pregunta['explicacion']}")

    st.markdown("---")
    col_f1, col_f2 = st.columns(2)

    with col_f1:
        if st.button("🔄 Otro test", use_container_width=True, type="primary"):
            reiniciar_test()
            st.rerun()

    with col_f2:
        if st.button("🎯 Repasar solo falladas", use_container_width=True):
            falladas = [p for p in preguntas
                        if respuestas.get(p["id"]) != p["correcta"]]
            if falladas:
                config = st.session_state.config_test.copy()
                config["modo"] = "Repaso falladas del test anterior"
                iniciar_test(falladas, len(falladas), config)
                st.rerun()
            else:
                st.success("¡No tienes preguntas falladas en este test!")
