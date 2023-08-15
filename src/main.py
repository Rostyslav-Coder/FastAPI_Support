"""src/main.py"""

from fastapi import FastAPI

app = FastAPI(title="Support App")


@app.get("/", name="Welcome Page")
def root():
    """Welcome Page"""
    return {"message": "Welcome"}
