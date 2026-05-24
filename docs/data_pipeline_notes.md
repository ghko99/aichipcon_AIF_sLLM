# Data Pipeline Notes

Keep each data pipeline stage traceable for recommendation and RAG experiments.

## Stages

- Source announcement collection.
- Document parsing and markdown conversion.
- Chunk creation and metadata tagging.
- Embedding generation.
- Vector index build.
- Evaluation question set generation.

## Metadata

Record crawl date, parser version, chunking rule, embedding model revision, index build time, and filtering thresholds. This makes retrieval changes easier to separate from generation changes.

## Artifacts

Keep raw PDFs, parsed documents, embeddings, and vector indexes outside normal Git history. Commit only small examples and documentation.
