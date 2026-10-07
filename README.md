# Chaski Pe

Aplicacion inclusiva para facilitar la comunicacion entre personas usuarias de
**Lengua de Señas Peruana (LSP)** y personas oyentes.

> **Estado actual: FASE 10 — reconocimiento del abecedario estatico de la LSP.**
> "Senas a texto" deletrea con las 24 letras estaticas (92 % de acierto en
> imagenes reservadas). Las senas con movimiento aun no tienen dataset real y
> el avatar no representa senas reales. Ver [Estado actual](#estado-actual).

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
| Backend       | Python, FastAPI, SQLAlchemy, Alembic         |
| IA            | Python, MediaPipe, TensorFlow/Keras (entreno) |
| Base de datos | PostgreSQL 16 (Docker)                       |
| Avatar        | Three.js (Blender + GLB en la FASE 10b)       |
| Control de versiones | Git                                  |
| Gestor de paquetes   | npm, pip                             |

---

## Estructura del repositorio

```
CHASKI PE/
├── frontend/    # aplicacion React + TS + Vite
├── backend/     # FastAPI + PostgreSQL (cuentas, historial, vocabulario, dataset)
├── ai/          # scripts de dataset y entrenamiento (letras y senas)
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

La app funciona **con o sin backend**. Para perfil e historial persistentes,
levanta tambien el backend (ver siguiente seccion).

Otros comandos:

```bash
npm run build    # verificacion de tipos + build de produccion
npm run preview  # servir el build
npm run lint
npm test         # paridad Python <-> TypeScript del modelo de letras
```

---

## Como ejecutar el backend (opcional)

Requisitos: Python 3.11 o 3.12, y Docker (para PostgreSQL).

```bash
# 1. Base de datos (desde la raiz del repo)
docker compose up -d db

# 2. Backend
cd backend
py -m venv .venv
.venv\Scripts\activate            # Windows
pip install -r requirements.txt
alembic upgrade head              # crea el esquema
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000 · Docs: http://127.0.0.1:8000/docs
- Persistencia en **PostgreSQL** (Docker). En desarrollo, sin BD el backend
  igual arranca (memoria); `GET /health` indica cual esta en uso. En
  produccion (`CHASKIPE_ENVIRONMENT=production`) exige BD y `SECRET_KEY`.
- Si no levantas el backend, el frontend usa datos de ejemplo.
- **Desde el celular**: `npm run dev` sirve por HTTPS en la red local; pon
  `VITE_API_URL=/backend` en `frontend/.env` para usar el proxy de Vite.
- **Despliegue en Dokploy**: ver `backend/README.md`.

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
- La sena confirmada pasa a la pantalla de resultado (con voz) y se guarda en
  el historial via la API.

**FASE 7 — Backend FastAPI**

- API REST (`backend/`, FastAPI + Uvicorn): perfil (GET/PUT), historial
  (GET/POST/DELETE), frases rapidas (GET), `/health`, `/docs`.
- El frontend conecta con **fallback a mock**: funciona con o sin backend
  (`VITE_API_URL`, `src/services/api.ts`).

**FASE 8 — PostgreSQL**

- Persistencia real en **PostgreSQL 16** (Docker, `docker-compose.yml`).
- SQLAlchemy 2.0 (`app/db/base.py`) + Alembic (`backend/alembic/`).
- Patron repositorio: `SqlRepository` con **fallback a `MemoryRepository`** si
  la BD no responde; `/health` indica cual esta activo.
- El perfil y el historial **sobreviven al reinicio del backend**.
- 15 pruebas (`pytest`), incluye integracion real con PostgreSQL.

**FASE 9 — Avatar 3D**

- Escena **Three.js** en "Texto a senas": avatar **geometrico** (no un GLB) que
  respira, parpadea y reproduce un **gesto DEMO**.
- `components/avatar/` (rig, animation, scene, Avatar3D). Carga diferida
  (`React.lazy`): el chunk de Three.js solo se baja en esa pantalla.
- El gesto **no representa ninguna sena real**; la pantalla lo avisa.

**Autenticacion**

- Cuentas reales (bcrypt + JWT), modo invitado y datos aislados por usuario.

**FASE 10 — Abecedario de la LSP**

- **Modelo de letras estaticas** (24 letras, sin J/Ñ/Z) entrenado con el
  dataset publico *Static Hand Gestures of the Peruvian Sign Language
  Alphabet* (CC BY-SA 4.0): 3575 manos extraidas con MediaPipe.
  92 % de acierto en imagenes reservadas; M, N y Q son las mas debiles.
- "Senas a texto" con modo **Abecedario** (deletreo letra por letra hasta
  formar una palabra) y modo **Senas** (con movimiento).
- Funciona con cualquier mano y con la camara frontal o trasera (mano
  canonica); world landmarks de MediaPipe, independientes del video.
- Pruebas de paridad Python ↔ TypeScript (`npm test`).
- Ver `ai/README.md`.

**Backend: vocabulario y dataset**

- `GET /signs`: vocabulario LSP (33 entradas) como dato, con `validated`.
- `POST /dataset/samples`: la herramienta `/dev/dataset` **envia las
  grabaciones al servidor** desde el celular; `GET /dataset/export` las
  descarga en zip para entrenar.
- `POST /recognition/reports`: boton "No era esto" en el resultado.
- Lista para Dokploy: acepta la URL `postgresql://` de Dokploy, falla al
  arrancar en produccion sin BD o sin `SECRET_KEY`, registra en los logs
  el motivo de un fallo de conexion.

### **No** implementado todavia

- **Senas con movimiento** (HOLA, GRACIAS, J, Ñ, Z...): falta grabar el
  dataset real (`/dev/dataset` → Enviar al servidor) y entrenar.
- **El avatar no representa senas** — gesto DEMO. GLB + animaciones LSP
  validadas es la FASE 10b.
- Validacion del abecedario y de las senas con personas usuarias de LSP o
  interpretes.
- Conversion texto -> secuencia LSP.
- Pose y rostro (MediaPipe) — solo manos por ahora.

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
| 6    | Integracion del modelo                      | Hecho (tiempo real) |
| 7    | Backend FastAPI                             | Hecho       |
| 8    | PostgreSQL                                  | Hecho       |
| 9    | Avatar 3D                                   | Hecho (basico, gesto DEMO) |
| 10   | Abecedario LSP (letras estaticas)           | **Actual** (92 %, falta validar con LSP) |
| 10b  | Senas con movimiento + animaciones validadas | Pendiente   |
| 11   | Integracion completa                        | Pendiente   |
