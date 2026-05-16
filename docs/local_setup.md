# Local Setup Notes

This project combines a Next.js frontend, FastAPI/RAG services, LH OpenAPI collection scripts, and model-serving components.

## Environment variables

Create a local `.env` from `.env.example` and fill in the service keys needed for the workflow you are running.

```bash
cp .env.example .env
```

## Node dependencies

```bash
npm install
```

## LH API collection scripts

The scripts under `LHAPI/collect_DATA/` use `SERVICE_KEY` from the environment. Avoid committing generated CSV files, downloaded notices, or local absolute paths.

## Python services

Install Python service dependencies in a virtual environment for each backend component. Keep model weights, vector indexes, parsed PDFs, and generated datasets outside Git unless they are small examples.
