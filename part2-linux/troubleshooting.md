# Linux / Docker Troubleshooting and Production Readiness Notes

## Dockerfile Design Summary

For the Flask application, I implemented a multi-stage Docker build to separate build-time and runtime dependencies. The builder stage uses `python:3.11-slim` and installs any required system packages such as `build-essential`, `gcc`, and `libffi-dev` to support Python packages with native extensions. Dependencies are installed into an isolated directory and copied into the runtime image. The final production image also uses `python:3.11-slim`, but only contains the runtime artifacts and the application code, reducing the final image size and attack surface.

To harden the container for production use, the application runs as a non-root user, exposes only the application port, and uses a lightweight health check against the `/health` endpoint. The startup command uses **Gunicorn** instead of Flask’s built-in development server so that the application can handle concurrent requests and run reliably in a production environment. This design improves security, portability, and operational readiness.
