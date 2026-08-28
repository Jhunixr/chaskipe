# Chaski Pe

Aplicacion inclusiva para facilitar la comunicacion entre personas usuarias de
**Lengua de Señas Peruana (LSP)** y personas oyentes.

> **Estado actual: FASE 1 (estructura base + frontend).**
> Muchas funcionalidades todavia **no** existen. Ver [Estado actual](#estado-actual).

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

Abrir http://localhost:5173

Otros comandos:

```bash
npm run build    # verificacion de tipos + build de produccion
npm run preview  # servir el build
npm run lint
```

---

## Estado actual

### Implementado (FASE 1)

- Estructura de carpetas de todo el proyecto.
- Frontend React + TypeScript (estricto) + Vite + React Router.
- Diseño mobile-first con identidad visual (crema, rojo, tarjetas blancas).
- Navegacion inferior y 11 pantallas de interfaz.
- Datos de ejemplo (mock) marcados como DEMO.
- Lectura por voz mediante la Web Speech API del navegador.

### **No** implementado todavia

- Acceso real a la camara.
- MediaPipe y extraccion de landmarks.
- Dataset y modelo de IA / reconocimiento de señas.
- Backend FastAPI y endpoints.
- Base de datos PostgreSQL.
- Avatar 3D (Three.js) y animaciones de LSP.
- Persistencia de perfil, historial y preferencias.

Las equivalencias texto ↔ seña mostradas en la app son **demostrativas** y no
han sido validadas con personas usuarias de LSP ni interpretes.

---

## Roadmap

| Fase | Contenido                                   | Estado      |
| ---- | ------------------------------------------- | ----------- |
| 1    | Frontend y estructura base                  | **Actual**  |
| 2    | Camara                                      | Pendiente   |
| 3    | MediaPipe                                   | Pendiente   |
| 4    | Dataset                                     | Pendiente   |
| 5    | Modelo de IA                                | Pendiente   |
| 6    | Integracion del modelo                      | Pendiente   |
| 7    | Backend FastAPI                             | Pendiente   |
| 8    | PostgreSQL                                  | Pendiente   |
| 9    | Avatar 3D                                   | Pendiente   |
| 10   | Animaciones LSP validadas                   | Pendiente   |
| 11   | Integracion completa                        | Pendiente   |
