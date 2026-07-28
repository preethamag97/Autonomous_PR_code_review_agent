#used for hashing data and verifying the integrity of the data received from GitHub webhooks. It ensures that the data has not been tampered with during transmission.  
import hashlib
import hmac

#httpx is an asynchronous HTTP client for Python that allows making HTTP requests to external services. In this case, it is used to forward the GitHub webhook payload to another service (webhook) for further processing.
import httpx
#fastapi is a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints. It is used to create the API endpoints for health checks and GitHub webhook handling. 
from fastapi import FastAPI, HTTPException, Request
from prometheus_fastapi_instrumentator import Instrumentator

from models import Settings

settings = Settings()
app = FastAPI()

#prometheus_fastapi_instrumentator is a library that provides Prometheus metrics for FastAPI applications. It instruments the FastAPI app to collect metrics such as request counts, response times, and other relevant information for monitoring and observability purposes. It is initialized and exposed to the FastAPI app to enable Prometheus metrics collection.
Instrumentator().instrument(app).expose(app)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/webhook/github")
async def github_webhook(request: Request):
    body = await request.body()
    signature_header = request.headers.get("X-Hub-Signature-256", "")
#recreating the signature using the webhook secret and the request body to verify that the request is indeed from GitHub. It uses HMAC (Hash-based Message Authentication Code) with SHA-256 hashing algorithm to generate the expected signature. The generated signature is then compared with the signature received in the request header to ensure authenticity.
    expected = (
        "sha256="
        + hmac.new(
            settings.github_webhook_secret.encode(),
            body,
            hashlib.sha256,
        ).hexdigest()
    )

    if not hmac.compare_digest(expected, signature_header):
        raise HTTPException(status_code=401, detail="Invalid signature")

#sending the verified webhook payload to another service (webhook) for further processing. It uses httpx.AsyncClient to make an asynchronous HTTP POST request to the specified URL (http://webhook:8001/events) with the request body and appropriate headers. The response is checked for success, and if successful, a JSON response indicating "status": "ok" is returned.
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://webhook:8001/events",
            content=body,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()

    return {"status": "ok"}
