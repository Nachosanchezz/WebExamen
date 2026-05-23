# 📚 App de estudio — Examen Preparación

Sistema interactivo de tests para preparar el examen de **Planificación y Gestión de Proyectos** (Finanzas + Gestión de Proyectos).

---

## ✨ Funcionalidades

- ✅ **Tres modos de test**: Solo Finanzas, Solo Gestión de Proyectos, o Mixto.
- 🎯 **Filtro por dificultad**: fácil, medio o difícil.
- 📊 **Configura el número de preguntas** (de 5 a 50).
- 🔁 **Modo Repaso**: revisa solo las preguntas que has fallado en tests anteriores.
- 👁️ **Dos modos de revisión**:
  - **Examen real**: ver respuestas al final.
  - **Aprendizaje**: ver respuesta tras cada pregunta.
- 💾 **Guardado automático del progreso** (historial, falladas, acertadas).
- 📈 **Estadísticas** en la barra lateral.
- 💡 **Explicaciones detalladas** de cada respuesta.

---

## ⚙️ Instrucciones de instalación

### Requisitos previos
- **Python 3.8+** instalado en el sistema.
- Conexión a internet (solo la primera vez para instalar Streamlit).

### Paso 1: Instalar Streamlit

Abre una terminal (PowerShell, CMD o Bash) y ejecuta:

```bash
pip install streamlit
```

Si te dice "pip no se reconoce", prueba:

```bash
python -m pip install streamlit
```

### Paso 2: Navegar a la carpeta del proyecto

```bash
cd "C:\Users\1cnac\OneDrive\Documentos\INGENIERIA MATEMATICA\Planifiacion y Gestion de Proyectos\Preparación Examen\SistemaEstudio\app"
```

### Paso 3: Ejecutar la app

```bash
streamlit run app.py
```

La app se abrirá automáticamente en tu navegador en la URL `http://localhost:8501`.

### Paso 4 (opcional): Detener la app

Pulsa `Ctrl + C` en la terminal donde está corriendo.

---

## 📁 Estructura de archivos

```
app/
├── app.py                              # Aplicación principal
├── README.md                           # Este archivo
├── progreso.json                       # Generado automáticamente con tu historial
└── data/
    ├── preguntas_finanzas.json         # 80 preguntas de Finanzas
    ├── preguntas_gestion_proyectos.json  # 110 preguntas de Gestión
    └── preguntas_mixtas.json           # 60 preguntas mixtas
```

> 💡 Total: **250 preguntas** disponibles para estudiar.

---

## 🎯 Cómo usar la app de forma óptima

### Estrategia recomendada (3 días antes del examen)

**Día 1 — Diagnóstico:**
- Modo: **Mixto**
- Dificultad: **Fácil + Medio**
- Preguntas: **30**
- Revisión: **Después de cada pregunta** (aprendizaje)

**Día 2 — Profundización por bloque:**
- 1 test **Solo Finanzas** (20 preguntas, todas dificultades)
- 1 test **Solo Gestión de Proyectos** (30 preguntas, todas dificultades)
- Revisión: **Después de cada pregunta**

**Día 3 — Simulacro y refuerzo:**
- 1 test **Mixto, todas dificultades**, 40 preguntas, **revisión al final** (simula examen real)
- 1 test **Repaso: solo preguntas falladas** para corregir errores
- Revisar los simulacros en `/Simulacros/` para complementar

### Consejos

1. **No te desesperes si fallas las primeras veces.** La app está diseñada para que aprendas de cada error.
2. **Lee las explicaciones**, especialmente las de preguntas falladas.
3. **Repite el modo "Solo falladas"** hasta vaciarlo. Esto es lo que mejor consolida el conocimiento.
4. **Antes del examen**, haz una pasada en modo "Examen real" (sin ver respuestas hasta el final).

---

## 🔧 Solución de problemas

### Error: "streamlit: command not found"
- Asegúrate de haber ejecutado `pip install streamlit`.
- Prueba con `python -m streamlit run app.py`.

### Error: "No se encontraron preguntas"
- Verifica que la carpeta `data/` existe y contiene los 3 archivos JSON.
- Si has movido la app, mantén la estructura `app.py` + `data/*.json`.

### La app no se abre en el navegador
- Copia manualmente la URL que muestra la terminal (típicamente `http://localhost:8501`).

### Quiero resetear mi progreso
- En la barra lateral de la app: botón **"🗑️ Borrar progreso"**.
- O elimina el archivo `progreso.json` manualmente.

---

## 📊 Información sobre las preguntas

- **Preguntas de Gestión de Proyectos**: extraídas de los 5 tests reales del profesor + preguntas inspiradas en los apuntes PMBoK.
- **Preguntas de Finanzas**: generadas a partir de los 4 temas de Javier (presupuestos, costes, P&L, asignación de costes).
- **Preguntas Mixtas**: combinación de conceptos compartidos entre ambos bloques.

Cada pregunta incluye:
- Enunciado claro
- 4 opciones (A, B, C, D)
- Respuesta correcta
- Explicación detallada
- Tema al que pertenece
- Nivel de dificultad

---

## 🚀 ¡Suerte en el examen!

Si dominas estas 250 preguntas, estarás más que preparado/a.

*Sistema de estudio generado a partir de los apuntes oficiales del curso.*
