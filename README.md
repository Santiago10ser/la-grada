# La Grada – Sitio web

## Requisitos
- Python 3.8+

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecutar el servidor

```bash
cd lagrada
uvicorn main:app --reload
```

Luego abrir en el navegador: http://localhost:8000

## Estructura
```
lagrada/
├── main.py              # Servidor FastAPI
├── requirements.txt     # Dependencias
├── templates/
│   ├── index.html       # Página principal (hero)
│   └── productos.html   # Catálogo de productos
└── static/              # Archivos estáticos (CSS, JS, imágenes)
```

## Páginas
- `/`           → Página principal con hero "La Grada"
- `/productos`  → Catálogo con filtros por categoría
