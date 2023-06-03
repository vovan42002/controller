from envparse import Env

env = Env()

CONTROLLER_API_HOST = env.str(
    "CONTROLLER_API_HOST",
    default=f"localhost",
)
CONTROLLER_API_PORT = env.int(
    "CONTROLLER_API_PORT",
    default=8001,
)

ESPF_API_HOST = env.str(
    "ESPF_API_HOST",
    default=f"localhost",
)
ESPF_API_PORT = env.int(
    "ESPF_API_PORT",
    default=3000,
)

ESPF_URL = f"http://{ESPF_API_HOST}:{ESPF_API_PORT}"

EMAIL = env.str("EMAIL", default="vova@example.com")

TIMEOUT = env.int("TIMEOUT", default=30)
