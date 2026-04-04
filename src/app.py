# src/app.py

from fastapi import FastAPI
from src.api import fetch_user, fetch_repos
from src.transform import analyze_repos, top_starred_repos

app = FastAPI()


@app.get("/")
def root():
    return {"message": "GitHub Pipeline API is running"}


@app.get("/user/{username}")
def get_user(username: str):
    return fetch_user(username)


@app.get("/repos/{username}")
def get_repos(username: str):
    return fetch_repos(username)


@app.get("/analytics/{username}")
def get_analytics(username: str):
    repos = fetch_repos(username)
    return analyze_repos(repos)


@app.get("/top-repos/{username}")
def get_top_repos(username: str):
    repos = fetch_repos(username)
    return top_starred_repos(repos, limit=5)
