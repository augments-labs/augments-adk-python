# Memory

Extracted, searchable knowledge carried across sessions.

## Core

- `augments.adk.memory.Memory`
- `augments.adk.memory.MemoryConfig`
- `augments.adk.memory.MemoryInjectionPosition`

## Entries and search

- `augments.adk.memory.MemoryEntry`
- `augments.adk.memory.MemoryKind`
- `augments.adk.memory.MemoryMetadata`
- `augments.adk.memory.MemorySource`
- `augments.adk.memory.MemorySearchFilter`
- `augments.adk.memory.MemorySearchResult`

## Implementations

- `augments.adk.memory.TemporaryMemory`
- `augments.adk.memory.SQLiteMemory`
- `augments.adk.memory.VectorMemory`

## Vector stores

- `augments.adk.memory.VectorStore`
- `augments.adk.memory.VectorRecord`
- `augments.adk.memory.VectorQueryResult`
- `augments.adk.memory.InMemoryVectorStore`

## Extraction

- `augments.adk.memory.MemoryExtractor`
- `augments.adk.memory.LLMExtractor`
- `augments.adk.memory.ExtractionResult`
- `augments.adk.memory.distill_to_semantic`

Usage lives in the [Memory guide](../../memory/memory.md).
