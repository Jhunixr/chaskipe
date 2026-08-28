# Base de datos — Chaski Pe

> Estado: **no iniciado**. Carpeta preparada para fases futuras.

## Motor previsto

- **PostgreSQL**

## Arquitectura

React **no** se conecta directamente a PostgreSQL:

```
React  →  FastAPI  →  PostgreSQL
```

## Estructura

```
database/
├── migrations/   # cambios de esquema versionados
├── seeds/        # datos iniciales (catalogos, frases base)
└── README.md
```

> Todavia **no** existe un `schema.sql` definitivo.

## Entidades futuras (borrador)

| Entidad              | Proposito                                              |
| -------------------- | ----------------------------------------------------- |
| `usuarios`           | Cuentas de la aplicacion                              |
| `preferencias_usuario` | Accesibilidad y ajustes por usuario                 |
| `senas`              | Catalogo de señas LSP validadas                       |
| `frases`             | Frases rapidas por categoria                          |
| `frase_sena`         | Relacion N:M entre frases y señas                     |
| `animaciones_sena`   | Referencia a los clips de avatar por seña             |
| `historial_traduccion` | Registro de traducciones (con consentimiento)       |

## Consideraciones importantes

- El **dataset de entrenamiento de IA no** se guarda en PostgreSQL.
  Vive en `../ai/data/raw/` y `../ai/data/processed/`.
- No se guardan videos de personas sin consentimiento explicito.
- Las señas del catalogo deben estar validadas con personas usuarias de LSP o
  interpretes antes de marcarse como definitivas.

## Pendiente

- [ ] Definir `schema.sql` inicial.
- [ ] Elegir herramienta de migraciones (Alembic u otra).
- [ ] Crear seeds de frases base.

Nada de esto se implementa en la FASE 1.
