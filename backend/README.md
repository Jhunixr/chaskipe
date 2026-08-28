# Backend — Chaski Pe

> Estado: **no iniciado**. Esta carpeta queda preparada para fases futuras.

## Tecnologias previstas

- **Python**
- **FastAPI**

## Rol del backend

El frontend (React) **no** se conecta directamente a la base de datos.
La arquitectura prevista es:

```
React  →  FastAPI  →  PostgreSQL
```

El backend expondra una API REST para: perfiles, preferencias, frases,
historial de traduccion y (mas adelante) la orquestacion del modelo de IA.

## Estructura futura

```
backend/
└── app/
    ├── main.py        # punto de entrada FastAPI
    ├── api/           # routers / endpoints
    ├── services/      # logica de negocio
    ├── schemas/       # modelos Pydantic (entrada/salida)
    └── core/          # configuracion, seguridad, dependencias
```

## Pendiente

- [ ] Crear entorno virtual e instalar FastAPI (aun **no** instalado).
- [ ] Definir `app/main.py` y el primer router.
- [ ] Conectar con PostgreSQL (ver `../database/README.md`).

Nada de esto se implementa en la FASE 1.
