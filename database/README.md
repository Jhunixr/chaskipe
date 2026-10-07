# Base de datos — Chaski Pe

> Estado: **PostgreSQL 16 en Docker** (local: `docker compose`; produccion:
> servicio `chaskipe-db` de Dokploy, tambien un contenedor Docker).
> El esquema y las migraciones viven en `backend/` (SQLAlchemy + Alembic).

## Motor

- **PostgreSQL 16** (contenedor Docker, ver `../docker-compose.yml`).

## Arquitectura

React **no** se conecta directamente a PostgreSQL:

```
React  →  FastAPI  →  PostgreSQL
```

En desarrollo, si PostgreSQL no responde, el backend cae a persistencia
**en memoria** y lo avisa en `/health` (`persistence: memory`). En produccion
(`CHASKIPE_ENVIRONMENT=production`) no arranca sin base de datos.

## Levantar / detener

```bash
# desde la raiz del repo
docker compose up -d db      # levantar
docker compose down          # detener (conserva los datos)
docker compose down -v       # detener y BORRAR los datos
```

Datos de conexion (por defecto):
`postgresql+psycopg://chaskipe:chaskipe@localhost:5432/chaskipe`

Se puede cambiar con `CHASKIPE_DATABASE_URL` (variable de entorno del backend).
Acepta tambien el formato `postgresql://...` que muestra Dokploy.

## Esquema y migraciones

Definidos en el backend con **SQLAlchemy 2.0** (`backend/app/db/base.py`) y
**Alembic** (`backend/alembic/`).

```bash
cd backend
.venv\Scripts\activate
alembic upgrade head                       # aplicar migraciones
alembic revision --autogenerate -m "..."   # nueva migracion tras cambiar modelos
alembic downgrade -1                        # revertir la ultima
```

> Al arrancar, el backend tambien hace `create_all()` (crea las tablas que
> falten). Alembic es el metodo recomendado para cambios de esquema.

## Entidades

| Tabla                        | Contenido |
| ---------------------------- | --------- |
| `usuarios`                   | Cuentas (nombre, correo, contrasena hasheada). |
| `preferencias_accesibilidad` | Preferencias por usuario. |
| `frases`                     | Frases rapidas por categoria. `es_demo=true` (senas no validadas). |
| `historial_traduccion`       | Traducciones por usuario: direccion, texto, fecha, `es_demo`. |
| `senas`                      | Vocabulario LSP (33 al sembrar: palabras, frases, abecedario). `validada` solo tras revision con LSP. |
| `muestras_sena`              | Registro de grabaciones subidas (el archivo con los landmarks vive en disco). |
| `modelos_reconocimiento`     | Versiones de modelos y su exactitud (`letras-v1`). |
| `reportes_reconocimiento`    | Avisos "No era esa sena" enviados desde la app. |
| `alembic_version`            | Control de versiones de Alembic. |

## Consideraciones importantes

- El **dataset de entrenamiento de IA no** se guarda en PostgreSQL.
  Vive en `../ai/data/raw/` y `../ai/data/processed/`.
- No se guardan videos de personas sin consentimiento explicito.
- Las senas del catalogo (futura tabla `senas`) deben estar validadas con
  personas usuarias de LSP o interpretes antes de marcarse como definitivas.
- Las carpetas `migrations/` y `seeds/` de aqui quedan como referencia; las
  migraciones reales estan en `backend/alembic/versions/` y la semilla en
  `backend/app/services/repository.py`.
