# Backend — Chaski Pe

> Estado: **FASE 7 — API REST con persistencia EN MEMORIA**.
> La base de datos real (PostgreSQL) es la FASE 8.

## Tecnologias

- **Python 3.11 / 3.12**
- **FastAPI** + **Uvicorn**
- **Pydantic v2**

## Arquitectura

```
React  →  FastAPI  →  (FASE 8: PostgreSQL)
```

El frontend **no** se conecta a la base de datos. En la FASE 7 el backend guarda
todo en memoria (`app/services/store.py`); esa capa se reemplazara por un
repositorio contra PostgreSQL manteniendo la misma interfaz.

- **Sin autenticacion** todavia (un unico usuario).
- **Sin endpoint de inferencia**: el modelo de reconocimiento corre en el
  navegador (FASE 5/6).

## Instalacion y ejecucion

```bash
cd backend
py -m venv .venv
.venv\Scripts\activate            # Windows   (source .venv/bin/activate en Unix)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Docs interactivas: http://127.0.0.1:8000/docs
- Healthcheck: http://127.0.0.1:8000/health

## Estructura

```
backend/
├── app/
│   ├── main.py            # FastAPI, CORS, /health, routers
│   ├── api/               # profile.py, history.py, phrases.py
│   ├── schemas/           # modelos Pydantic (entrada/salida)
│   ├── services/store.py  # almacen EN MEMORIA (semilla incluida)
│   └── core/config.py     # settings (env CHASKIPE_*)
├── tests/                 # pytest (TestClient)
└── requirements.txt
```

## Endpoints (`/api/v1`)

| Metodo | Ruta | Descripcion |
| ------ | ---- | ----------- |
| GET    | `/profile` | Perfil del usuario |
| PUT    | `/profile` | Actualiza nombre y correo |
| GET    | `/history` | Historial (orden reciente-primero; `?limit=N`) |
| POST   | `/history` | Anade una entrada |
| DELETE | `/history/{id}` | Borra una entrada (404 si no existe) |
| DELETE | `/history` | Vacia el historial |
| GET    | `/phrases` | Frases rapidas por categoria |
| GET    | `/health` | Estado del servicio (sin prefijo) |

## Pruebas

```bash
cd backend
.venv\Scripts\activate
pytest -q
```

## Notas de datos

- Todo lo relacionado con senas LSP viaja con `is_demo: true`: no esta validado
  con personas usuarias de LSP ni interpretes.
- Los datos semilla (perfil "Andersson", 3 entradas de historial, frases) son de
  ejemplo y se reinician al reiniciar el proceso.

## Pendiente (FASE 8)

- [ ] Modelos SQLAlchemy + migraciones (Alembic).
- [ ] Reemplazar `MemoryStore` por un repositorio contra PostgreSQL.
- [ ] Autenticacion / usuarios.
