import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

# Convert env vars
port = int(os.getenv("PORT"))
reload = os.getenv("RELOAD", "False").lower() == "true"
use_https = os.getenv("USE_HTTPS", "False").lower() == "true"
ssl_keyfile = os.getenv("SSL_KEYFILE")
ssl_certfile = os.getenv("SSL_CERTFILE")

uvicorn_args = {
    "app": "src.main:app",
    "host": os.getenv("HOST", "127.0.0.1"),
    "port": port,
    "reload": reload,
    
    "log_level": os.getenv("LOG_LEVEL", "info")
}
# Add SSL if enabled
if use_https:
    uvicorn_args["ssl_keyfile"] = ssl_keyfile
    uvicorn_args["ssl_certfile"] = ssl_certfile

if __name__ == "__main__":
    uvicorn.run(**uvicorn_args)