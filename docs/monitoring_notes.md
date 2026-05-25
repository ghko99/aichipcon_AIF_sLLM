# Monitoring Notes

Monitor retrieval, generation, and service health separately for the LH recommendation and chatbot stack.

## Service Signals

- Request count and error rate by endpoint.
- End-to-end latency and model-serving latency.
- Retrieval latency and number of returned chunks.
- Token generation throughput.
- Empty or low-score retrieval results.

## Quality Signals

Sample production-like queries and save retrieved chunk ids, final context, and model responses. Review failures by category: stale announcement data, weak retrieval, prompt issue, or generation error.

## Incident Record

For incidents, keep the request id, timestamp, model endpoint, vector index version, announcement snapshot, and relevant logs in one folder.
