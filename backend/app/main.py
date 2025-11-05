from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title="Dashboard Financeiro API",
    description="API Backend para gerenciamento financeiro pessoal",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Dashboard Financeiro API", "version": "0.1.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Importar routers
from app.api import auth, transactions, categories, projections, ai, upload

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(projections.router, prefix="/api/projections", tags=["projections"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
