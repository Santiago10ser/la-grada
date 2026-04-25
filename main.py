from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

products = [
    # SELECCIONES - Versión Jugador
    {"id": 1,  "name": "Francia 25/26 Local",             "category": "Selecciones", "price": 250000, "tag": "new",  "tallas": "M, L, XL", "version": "Jugador", "color": "#002395", "img": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400&h=530&fit=crop"},
    {"id": 2,  "name": "Argentina 25/26 Local",           "category": "Selecciones", "price": 250000, "tag": "new",  "tallas": "M, L, XL", "version": "Jugador", "color": "#74acdf", "img": "https://images.unsplash.com/photo-1580087256394-dc596e1c8f4f?w=400&h=530&fit=crop"},
    {"id": 3,  "name": "Argentina 25/26 — Messi #10",     "category": "Selecciones", "price": 280000, "tag": None,   "tallas": "M, L, XL", "version": "Jugador", "color": "#74acdf", "img": "https://images.unsplash.com/photo-1518091043644-c1d4457512c6?w=400&h=530&fit=crop"},
    {"id": 4,  "name": "España 25/26 Visitante",          "category": "Selecciones", "price": 250000, "tag": "new",  "tallas": "M, L, XL", "version": "Jugador", "color": "#c60b1e", "img": "https://images.unsplash.com/photo-1571945153237-4929e783af4a?w=400&h=530&fit=crop"},
    {"id": 5,  "name": "Brasil 25/26 Local",              "category": "Selecciones", "price": 250000, "tag": None,   "tallas": "M, L, XL", "version": "Jugador", "color": "#009c3b", "img": "https://images.unsplash.com/photo-1553778263-73a83bab9b0c?w=400&h=530&fit=crop"},
    {"id": 6,  "name": "Portugal 25/26 — Ronaldo #7",     "category": "Selecciones", "price": 280000, "tag": None,   "tallas": "M, L, XL", "version": "Jugador", "color": "#006600", "img": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&h=530&fit=crop"},
    {"id": 7,  "name": "Alemania 25/26 Local",            "category": "Selecciones", "price": 250000, "tag": "new",  "tallas": "M, L, XL", "version": "Jugador", "color": "#ffffff", "img": "https://images.unsplash.com/photo-1562183241-840b8af0721e?w=400&h=530&fit=crop"},
    # PARAGUAY - Versión Fan
    {"id": 8,  "name": "Cerro Porteño 2026 Local",        "category": "Paraguay",    "price": 180000, "tag": None,   "tallas": "M, L, XL", "version": "Fan",     "color": "#0033a0", "img": "https://images.unsplash.com/photo-1591195853828-11db59a44f43?w=400&h=530&fit=crop"},
    {"id": 9,  "name": "Cerro Porteño 2026 Visitante",    "category": "Paraguay",    "price": 180000, "tag": None,   "tallas": "M, L, XL", "version": "Fan",     "color": "#cc0000", "img": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&h=530&fit=crop"},
    {"id": 10, "name": "Olimpia 2026 Local",              "category": "Paraguay",    "price": 180000, "tag": "new",  "tallas": "M, L, XL", "version": "Fan",     "color": "#1a1a1a", "img": "https://images.unsplash.com/photo-1614632537423-1e6c2e7b0427?w=400&h=530&fit=crop"},
]

categorias = ["Todos", "Selecciones", "Paraguay"]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/novedades", response_class=HTMLResponse)
async def novedades(request: Request):
    return templates.TemplateResponse(request, "novedades.html")

@app.get("/encargos", response_class=HTMLResponse)
async def encargos(request: Request):
    return templates.TemplateResponse(request, "encargos.html")

@app.get("/contacto", response_class=HTMLResponse)
async def contacto(request: Request):
    return templates.TemplateResponse(request, "contacto.html")

@app.get("/productos", response_class=HTMLResponse)
async def productos(request: Request, categoria: str = "Todos"):
    filtered = products if categoria == "Todos" else [p for p in products if p["category"] == categoria]
    return templates.TemplateResponse(request, "productos.html", {
        "products": filtered,
        "categorias": categorias,
        "categoria_actual": categoria,
        "total": len(filtered)
    })
