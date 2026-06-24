from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers (ajuste conforme seu projeto)
from routers import auth
from routers import usuarios
from routers import dashboard
from routers import despesas
from routers import upload
from routers import websocket

app = FastAPI(
    title="Sistema de Despesas",
    version="1.0.0"
)

# CORS (importante para frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois você pode restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rotas
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(despesas.router, prefix="/despesas", tags=["Despesas"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])


@app.get("/")
def root():
    return {
        "message": "API Sistema de Despesas rodando 🚀"
    }