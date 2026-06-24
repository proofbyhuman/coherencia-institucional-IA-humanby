# Coherencia Institucional

Sistema de publicación de noticias con frontend estático, panel de administración y backend en Python/Flask que genera noticias actuales automáticamente.

## Estructura del Proyecto

```
/workspace
├── app.py              # Backend Flask (servidor principal)
├── index.html          # Frontend público (archivo estático original)
├── admin.html          # Panel de administración (archivo estático original)
├── requirements.txt    # Dependencias de Python
└── README.md           # Este archivo
```

## Características

- **Frontend Público**: Sitio web de noticias con diseño responsive
- **Panel Admin**: Interfaz para gestionar noticias (aprobar/rechazar)
- **Generador de Noticias**: Sistema automático que crea noticias actuales por categoría
- **API REST**: Endpoints para consumir noticias programáticamente

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar el servidor:
```bash
python app.py
```

## Endpoints Disponibles

| URL | Descripción |
|-----|-------------|
| `http://localhost:5000/` | Frontend público |
| `http://localhost:5000/admin` | Panel de administración |
| `http://localhost:5000/api/news` | API para obtener noticias (GET) |
| `http://localhost:5000/api/generate-news` | Generar nuevas noticias (POST) |
| `http://localhost:5000/api/news/<id>/approve` | Aprobar noticia (POST) |
| `http://localhost:5000/api/news/<id>/reject` | Rechazar noticia (POST) |

## Categorías de Noticias

- **Política**: Transparencia institucional, reforma electoral, políticas públicas
- **Cultura**: Expresiones artísticas, patrimonio histórico, industrias creativas
- **Economía**: Mercados emergentes, innovación tecnológica, comercio internacional
- **Geopolítica**: Cooperación regional, seguridad energética, diplomacia multilateral

## Flujo de Trabajo

1. El sistema genera noticias automáticamente al iniciar
2. Las noticias pasan por estados: `draft` → `approved` o `rejected`
3. El panel admin permite auditar, aprobar o rechazar noticias
4. El frontend público muestra solo noticias aprobadas

## Tecnologías

- **Backend**: Python 3, Flask
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Fuentes**: IBM Plex Mono, Source Serif 4 (Google Fonts)
