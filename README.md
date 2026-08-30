# Chaski Pe

Aplicacion inclusiva para facilitar la comunicacion entre personas usuarias de
**Lengua de Señas Peruana (LSP)** y personas oyentes.

> **Estado actual: FASE 6 (el modelo reconoce senas en "Senas a texto").**
> El modelo es de prueba (datos sinteticos); aun no reconoce senas reales.
> Ver [Estado actual](#estado-actual).

---

## Objetivo

Ofrecer una herramienta movil que permita comunicacion en dos sentidos:

### Flujo 1 — Señas a texto y voz

```
persona hace una seña → camara → MediaPipe (manos, cuerpo, rostro)
→ landmarks → modelo de IA → seña reconocida → texto → voz
```

Ejemplo: la persona realiza la seña de **AYUDA** → la app muestra
"Necesito ayuda" y permite reproducirlo por voz.

### Flujo 2 — Texto/voz a señas

```
persona escribe o habla → texto → procesamiento
→ secuencia de LSP → avatar humano → el avatar reproduce las señas
```

### Principios

- La gramatica del espanol y la de LSP **no** son iguales.
- **No se inventan señas reales.** Durante el prototipo puede haber datos o
  animaciones **DEMO**, siempre identificados como demostrativos hasta ser
  validados con personas usuarias de LSP o interpretes.
- No se graban videos de personas sin consentimiento.

---

## Arquitectura

```
React (frontend)  →  FastAPI (backend)  →  PostgreSQL (base de datos)

                     MediaPipe + modelo de IA  (reconocimiento de señas)
                     Blender + Three.js        (avatar 3D, GLB/glTF)
```

El frontend **nunca** se conecta directamente a PostgreSQL.
El dataset de IA vive en `ai/data/`, **no** en la base de datos.

---

## Tecnologias

| Area          | Stack                                        |
| ------------- | -------------------------------------------- |
| Frontend      | React, TypeScript, Vite, React Router, CSS   |
| Backend       | Python, FastAPI *(futuro)*                   |
| IA            | Python, MediaPipe *(futuro)*                 |
| Base de datos | PostgreSQL *(futuro)*                        |
| Avatar        | Blender, Three.js, GLB/glTF *(futuro)*       |
| Control de versiones | Git                                  |
| Gestor de paquetes   | npm                                  |

---

## Estructura del repositorio

```
CHASKI PE/
├── frontend/    # aplicacion React + TS + Vite (unica area desarrollada)
├── backend/     # FastAPI — solo README por ahora
├── ai/          # MediaPipe + modelo — solo estructura y README
├── avatar/      # Blender + Three.js — solo estructura y README
├── database/    # PostgreSQL — solo estructura y README
├── docs/        # documentacion del proyecto
├── .gitignore
└── README.md
```

Cada README de subcarpeta explica lo que llegara en fases posteriores.

---

## Como ejecutar el frontend

Requisitos: Node.js 20+ y npm.

```bash
cd frontend
npm install
npm run dev
```

Abrir http://localhost:5173 (la app abre en `/` con la pantalla de carga y
avanza a la bienvenida).

Otros comandos:

```bash
npm run build    # verificacion de tipos + build de produccion
npm run preview  # servir el build
npm run lint
```

---

## Estado actual

### Implementado

**FASE 1 — Frontend y estructura**

- Estructura de carpetas de todo el proyecto.
- Frontend React + TypeScript (estricto) + Vite + React Router.
- Diseño mobile-first con identidad visual (crema, rojo, tarjetas blancas,
  tipografia Nunito, mascota del chaski, montanas y cenefa andina sutiles).
- 16 pantallas: splash, onboarding, login, registro y las 12 pantallas de la app.
- Navegacion inferior (Inicio / Conversacion / Historial / Perfil).
- Datos de ejemplo (mock) marcados como DEMO.
- Lectura por voz (Web Speech API) y ajuste de tamano de texto global.

**FASE 2 — Camara**

- Acceso a la camara del dispositivo con `getUserMedia` (`useCamera`).
- Video en vivo en "Preparar camara" y "Senas a texto" (`CameraView`).
- Manejo de permisos: pendiente, denegado, sin camara, camara ocupada,
  navegador no compatible, con boton "Reintentar".
- Alternar camara frontal/trasera; la frontal se muestra en espejo.

**FASE 3 — MediaPipe (deteccion de manos)**

- `@mediapipe/tasks-vision` con Hand Landmarker: 21 puntos por mano, hasta 2 manos.
- Assets locales en `frontend/public/mediapipe/` (funciona offline).
- `useHandLandmarker` + `HandOverlay`: landmarks dibujados sobre el video en vivo.
- Estados en pantalla: "Cargando detector...", "Muestra las manos",
  "1/2 manos detectadas".

**FASE 4 — Dataset**

- Formato definido en `ai/data/DATASET_FORMAT.md` (1 JSON por grabacion).
- Herramienta de captura en el frontend: `/dev/dataset`. Elegir sena,
  consentimiento, grabar ~2 s, descargar JSON. Solo landmarks, no video.
- Vocabulario inicial: HOLA, GRACIAS, AYUDA, SI, NO.
- `ai/scripts/inspect_dataset.py`: resumen y validacion del dataset (stdlib).

**FASE 5 — Modelo de IA**

- Pipeline Python completo en `ai/scripts/`: `synth_dataset` → `preprocess` →
  `train` → `evaluate` → `export_tfjs`. Ver `ai/README.md`.
- **MLP** (381 features → 128 → 64 → n_clases). Features: estadisticos temporales
  de los landmarks normalizados de cada mano.
- Inferencia **en el navegador**, sin servidor: `frontend/src/services/signModel.ts`
  (implementacion propia, sin TensorFlow.js).
- La extraccion de features de Python y del frontend **coincide** (verificado, < 1e-6).

**FASE 6 — Integracion del modelo (tiempo real)**

- El modelo esta **conectado a "Senas a texto"** y analiza **en tiempo real**:
  ventana deslizante de 2 s, prediccion cada ~300 ms, sin boton de disparo.
- Muestra el candidato en vivo y lo **confirma** cuando se mantiene estable
  ~0.6 s por encima del 60 % de confianza; luego pausa para no repetir.
- La sena confirmada pasa a la pantalla de resultado (con voz).
- Verificado: la logica de confirmacion acierta 5/5 clases con landmarks reales;
  el bucle en vivo corre en el navegador sin errores.

### **No** implementado todavia

- **El modelo no reconoce senas reales** — entrenado con datos sinteticos de
  prueba. La pantalla lo avisa.
- Muestras reales del dataset.
- Pose y rostro (MediaPipe) — solo manos por ahora.
- Autenticacion real (login y registro son de demostracion).
- Backend FastAPI y endpoints.
- Base de datos PostgreSQL.
- Avatar 3D (Three.js) y animaciones de LSP.
- Persistencia de perfil, historial y la mayoria de preferencias.

Las equivalencias texto ↔ seña mostradas en la app son **demostrativas** y no
han sido validadas con personas usuarias de LSP ni interpretes.

---

## Roadmap

| Fase | Contenido                                   | Estado      |
| ---- | ------------------------------------------- | ----------- |
| 1    | Frontend y estructura base                  | Hecho       |
| 2    | Camara                                      | Hecho       |
| 3    | MediaPipe                                   | Hecho       |
| 4    | Dataset                                     | Hecho       |
| 5    | Modelo de IA                                | Hecho (con datos sinteticos) |
| 6    | Integracion del modelo                      | **Actual**  |
| 7    | Backend FastAPI                             | Pendiente   |
| 8    | PostgreSQL                                  | Pendiente   |
| 9    | Avatar 3D                                   | Pendiente   |
| 10   | Animaciones LSP validadas                   | Pendiente   |
| 11   | Integracion completa                        | Pendiente   |
