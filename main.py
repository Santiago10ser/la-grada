from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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
    try:
        if categoria == "Todos":
            response = supabase.table("productos").select("*").execute()
        else:
            response = supabase.table("productos").select("*").eq("category", categoria).execute()
        products = response.data
    except Exception as e:
        products = []
        print(f"Error fetching products: {e}")

    return templates.TemplateResponse(request, "productos.html", {
        "products": products,
        "categorias": categorias,
        "categoria_actual": categoria,
        "total": len(products)
    })
