from fastapi import FastAPI, Request, Form, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
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

ADMIN_USER = "admin"
ADMIN_PASS = "LagradaPy_10"
ADMIN_TOKEN = "lagrada_admin_secret_token"

categorias = ["Todos", "Selecciones", "Paraguay"]

def is_admin(request: Request):
    return request.cookies.get("admin_token") == ADMIN_TOKEN

# ── TIENDA ──────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/novedades", response_class=HTMLResponse)
async def novedades(request: Request):
    try:
        destacado_res = supabase.table("novedades_banners").select("*").eq("tipo", "destacado").limit(1).execute()
        promo_res = supabase.table("novedades_banners").select("*").eq("tipo", "promo").limit(1).execute()
        cards_res = supabase.table("novedades_cards").select("*").order("orden").execute()
        destacado = destacado_res.data[0] if destacado_res.data else None
        promo = promo_res.data[0] if promo_res.data else None
        cards = cards_res.data
    except Exception as e:
        destacado, promo, cards = None, None, []
        print(f"Error: {e}")
    return templates.TemplateResponse(request, "novedades.html", {
        "destacado": destacado,
        "promo": promo,
        "cards": cards
    })

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
            response = supabase.table("productos").select("*").order("orden").execute()
        else:
            response = supabase.table("productos").select("*").eq("category", categoria).order("orden").execute()
        products = response.data
    except Exception as e:
        products = []
        print(f"Error: {e}")
    return templates.TemplateResponse(request, "productos.html", {
        "products": products,
        "categorias": categorias,
        "categoria_actual": categoria,
        "total": len(products)
    })

# ── ADMIN AUTH ──────────────────────────────────────────────

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    if is_admin(request):
        return RedirectResponse("/admin", status_code=302)
    return templates.TemplateResponse(request, "admin_login.html", {"error": None})

@app.post("/admin/login")
async def admin_login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USER and password == ADMIN_PASS:
        response = RedirectResponse("/admin", status_code=302)
        response.set_cookie("admin_token", ADMIN_TOKEN, httponly=True, max_age=86400)
        return response
    return templates.TemplateResponse(request, "admin_login.html", {"error": "Usuario o contraseña incorrectos"})

@app.get("/admin/logout")
async def admin_logout():
    response = RedirectResponse("/admin/login", status_code=302)
    response.delete_cookie("admin_token")
    return response

# ── ADMIN PANEL ─────────────────────────────────────────────

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    if not is_admin(request):
        return RedirectResponse("/admin/login", status_code=302)
    return templates.TemplateResponse(request, "admin.html")

# ── ADMIN API ───────────────────────────────────────────────

@app.get("/admin/api/productos")
async def api_get_productos(request: Request):
    if not is_admin(request):
        return JSONResponse({"error": "No autorizado"}, status_code=401)
    res = supabase.table("productos").select("*").execute()
    return JSONResponse(res.data)

@app.post("/admin/api/productos/reorder")
async def api_reorder_productos(request: Request):
    if not is_admin(request):
        return JSONResponse({"error": "No autorizado"}, status_code=401)
    updates = await request.json()
    for item in updates:
        supabase.table("productos").update({"orden": item["orden"]}).eq("id", item["id"]).execute()
    return JSONResponse({"ok": True})

@app.post("/admin/api/productos")
async def api_add_producto(request: Request):
    if not is_admin(request):
        return JSONResponse({"error": "No autorizado"}, status_code=401)
    data = await request.json()
    res = supabase.table("productos").insert(data).execute()
    return JSONResponse(res.data)

@app.put("/admin/api/productos/{id}")
async def api_update_producto(id: int, request: Request):
    if not is_admin(request):
        return JSONResponse({"error": "No autorizado"}, status_code=401)
    data = await request.json()
    res = supabase.table("productos").update(data).eq("id", id).execute()
    return JSONResponse(res.data)

@app.delete("/admin/api/productos/{id}")
async def api_delete_producto(id: int, request: Request):
    if not is_admin(request):
        return JSONResponse({"error": "No autorizado"}, status_code=401)
    supabase.table("productos").delete().eq("id", id).execute()
    return JSONResponse({"ok": True})

# ── ADMIN API: NOVEDADES (unificado) ────────────────────────

@app.get("/admin/api/novedades")
async def api_get_novedades(request: Request):
    if not is_admin(request):
        return JSONResponse({"error": "No autorizado"}, status_code=401)
    banners_res = supabase.table("novedades_banners").select("*").execute()
    cards_res = supabase.table("novedades_cards").select("*").order("orden").execute()
    return JSONResponse({"banners": banners_res.data, "cards": cards_res.data})

@app.post("/admin/api/novedades/banner")
async def api_update_novedades_banner(request: Request):
    if not is_admin(request):
        return JSONResponse({"error": "No autorizado"}, status_code=401)
    data = await request.json()
    tipo = data.get("tipo")
    existing = supabase.table("novedades_banners").select("id").eq("tipo", tipo).limit(1).execute()
    if existing.data:
        res = supabase.table("novedades_banners").update(data).eq("tipo", tipo).execute()
    else:
        res = supabase.table("novedades_banners").insert(data).execute()
    return JSONResponse(res.data)

@app.post("/admin/api/novedades/cards")
async def api_add_novedades_card(request: Request):
    if not is_admin(request):
        return JSONResponse({"error": "No autorizado"}, status_code=401)
    data = await request.json()
    res = supabase.table("novedades_cards").insert(data).execute()
    return JSONResponse(res.data)

@app.put("/admin/api/novedades/cards/{id}")
async def api_update_novedades_card(id: int, request: Request):
    if not is_admin(request):
        return JSONResponse({"error": "No autorizado"}, status_code=401)
    data = await request.json()
    res = supabase.table("novedades_cards").update(data).eq("id", id).execute()
    return JSONResponse(res.data)

@app.delete("/admin/api/novedades/cards/{id}")
async def api_delete_novedades_card(id: int, request: Request):
    if not is_admin(request):
        return JSONResponse({"error": "No autorizado"}, status_code=401)
    supabase.table("novedades_cards").delete().eq("id", id).execute()
    return JSONResponse({"ok": True})

@app.post("/admin/api/novedades/cards/reorder")
async def api_reorder_novedades_cards(request: Request):
    if not is_admin(request):
        return JSONResponse({"error": "No autorizado"}, status_code=401)
    updates = await request.json()
    for item in updates:
        supabase.table("novedades_cards").update({"orden": item["orden"]}).eq("id", item["id"]).execute()
    return JSONResponse({"ok": True})

# ── ADMIN API: NOVEDADES CARDS (legacy, sin usar) ───────────
