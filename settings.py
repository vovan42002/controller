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
    default=8001,
)

EMAIL = env.str("EMAIL", default="user2@example.com")

TIMEOUT = env.int("TIMEOUT", default=3)
