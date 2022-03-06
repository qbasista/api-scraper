import environ

env = environ.Env(API_PATH=(str, "https://localhost:8000"), IO_REQUEST_LIMIT=(int, 100))
environ.Env.read_env()

API_URL = env("API_URL")
ASSETS_DIR = "assets"
IO_REQUEST_LIMIT = env("IO_REQUEST_LIMIT")
