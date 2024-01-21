from fastapi import FastAPI
import uvicorn

from router import router_menu


app = FastAPI(
    title='Menu app'
)

app.include_router(router_menu)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
