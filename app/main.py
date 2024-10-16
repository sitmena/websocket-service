from fastapi import FastAPI
from .apis import trigger, manager


app = FastAPI()

app.include_router(trigger)


@app.get("/", status_code=200)
def root():
    return {
        "message": "notification proof of concept",
    }
