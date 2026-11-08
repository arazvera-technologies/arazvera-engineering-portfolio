# Educational, synthetic-only health endpoint; review image digest before deployment.
FROM python:3.12-alpine
WORKDIR /app
COPY health_server.py .
USER 65534:65534
HEALTHCHECK --interval=30s CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8000/health',timeout=2)"
CMD ["python", "health_server.py"]
