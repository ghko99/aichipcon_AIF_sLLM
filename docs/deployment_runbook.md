# Deployment Runbook

Use this runbook when bringing up the LH recommendation and RAG chatbot stack.

## Before Startup

- Confirm environment variables for API keys and model endpoints.
- Check that embedding, vector index, and announcement data paths are present.
- Verify FastAPI, frontend, and model-serving processes can reach each other.
- Record hardware and serving backend details.

## Smoke Checks

- Load the frontend page.
- Run a recommendation query with a known customer profile.
- Run a chatbot question against a known announcement.
- Confirm retrieved context and final answer are logged.

## Incident Notes

For failures, record the request payload, selected announcement ids, retrieved chunk ids, model endpoint, latency, and server logs.
