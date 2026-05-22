# RAG Evaluation Notes

Use this checklist when evaluating the LH announcement retrieval and chatbot pipeline.

## Retrieval Record

- Source announcement snapshot or crawl date.
- Document parser version and chunking rule.
- Embedding model name and revision.
- Vector index build date.
- Lexical, title, and element similarity weights.
- Passage filtering threshold.

## Answer Evaluation

Track answer quality separately from retrieval quality. Save the question set, retrieved chunk ids, final context, model response, and evaluator output. This makes it easier to distinguish bad retrieval from weak generation.

## Load Testing

When reporting TPS or latency, include hardware, model serving backend, batch size, streaming mode, and concurrent user count. Keep raw Locust exports with the summary chart.
