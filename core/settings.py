import environ

env = environ.Env(API_PATH=(str, "https://localhost:8000"))
environ.Env.read_env()

API_PATH = env("API_PATH")
