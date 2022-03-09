import environ

env = environ.Env(
    API_URL=(str, "https://jsonplaceholder.typicode.com"),
    IO_REQUEST_LIMIT=(int, 100),
    CLIENT_TIMEOUT=(int, 1000),
)
environ.Env.read_env()

API_URL = env("API_URL")
IO_REQUEST_LIMIT = env("IO_REQUEST_LIMIT")
CLIENT_TIMEOUT = 10000

ASSETS_DIR = "assets"
