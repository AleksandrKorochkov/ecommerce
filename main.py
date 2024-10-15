from fastapi import FastAPI
from routers import category, products, auth, permission, raiting_reviews

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {"messegr": "My e-commerce app"}

app.include_router(category.router)
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(permission.router)
app.include_router(raiting_reviews.router)