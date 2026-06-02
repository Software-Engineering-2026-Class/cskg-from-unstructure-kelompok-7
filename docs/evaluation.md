# CSKG Evaluation

This document evaluates the final runtime state of the Cybersecurity Knowledge Graph pipeline and generated graph.

## What Works

The current pipeline is functional end-to-end for the final verified run.

Successful components:

- The producer collected articles from the configured RSS/API sources.
- The extractor processed queued articles and produced cybersecurity entity/relation extractions.
- The graph builder inserted 1009 triples into the named graph `<http://group2.org/cskg>`.
- Redis queues are draining correctly for the processed batch; `extractions_queue` is empty after graph insertion.
- Virtuoso is reachable at the configured SPARQL endpoint.
- FastAPI can query Virtuoso through `POST /query`.
- `GET /` now distinguishes global Virtuoso triples from CSKG named graph triples.
- `GET /stats` now reports named graph statistics.
- SEPSES CVE URI linking is present for 11 CVE resources.
- Threat actor extraction improved from 0 entities in the earlier runtime snapshot to 60 entities in the final verified graph.

Final graph summary:

| Metric | Value |
|---|---:|
| Total CSKG named graph triples | 1009 |
| Reports | 94 |
| Vulnerabilities | 30 |
| Malware | 25 |
| Indicators | 11 |
| Attack patterns | 85 |
| Threat actors | 60 |
| SEPSES CVE URIs | 11 |

## What Is Still Missing

The final run covers the main runtime requirements, but it does not yet cover all desired knowledge graph quality goals.

Missing or weak areas:

- Some extracted relationships point to untyped object nodes, for example target or related concept URIs that do not yet have explicit RDF types.
- The graph is still limited to the collected RSS/API batch.
- SEPSES linking is currently strongest for CVE URI mapping, with 11 SEPSES CVE URIs in the latest graph; CWE and MITRE ATT&CK URI alignment remain future work.
- Automatic natural-language report generation may still be affected by Gemini quota limits.
- Extraction quality depends on source article summaries and Gemini output consistency.

## Errors and Limitations

### Gemini Quota Risk

Automatic report generation depends on Gemini availability and quota.

Earlier runtime behavior showed quota exhaustion:

```text
[SUMMARY] System Healthy. CSKG Named Graph Triples: 83
[SUMMARY] No threat actor relationships found. Using fallback graph summary.
[SUMMARY] Generating report for 2026-05-19...
429 RESOURCE_EXHAUSTED
Quota exceeded for model: gemini-2.0-flash-lite
```

Impact:

- Graph statistics, SPARQL queries, and `/stats` output remain available even if Gemini quota is exhausted.
- Natural-language report generation can be blocked until Gemini quota or API configuration is resolved.
- This is an external LLM availability issue, not an RDF/Virtuoso/API issue.

### Historical ThreatActor Gap

An earlier 8-article runtime snapshot produced:

```text
ThreatActor = 0
```

The final verified graph improved this to:

```text
ThreatActor = 60
```

Possible causes that need further checking:

- The specific article summaries may not explicitly mention named threat actors.
- The extractor prompt may be conservative or inconsistent for actor extraction.
- RSS summaries may be too short compared to full article text.
- Extracted actor-like strings may have been emitted as untyped relationship subjects instead of typed `stix:ThreatActor` entities.

Impact:

- Threat actor coverage is now present in the final graph, but extraction quality still depends on source content and model consistency.
- Further validation is needed to measure whether each extracted actor is correctly typed and linked.

### Precision and Recall Estimate

Exact precision/recall is not calculated because no manually labeled gold-standard dataset was created. Instead, this project provides a qualitative evaluation based on runtime outputs, entity distribution, query results, and known extraction gaps.

## Evaluation of Current Requirements

| Requirement | Current Status | Evidence | Remaining Work |
|---|---|---|---|
| Multiple unstructured sources | Partially satisfied | RSS/API source pipeline produced 94 reports | Continue expanding source coverage |
| RDF knowledge graph | Satisfied for final run | 1009 triples in `<http://group2.org/cskg>` | Improve typing and external alignment |
| Named graph correctness | Satisfied | `GET /` and `/stats` report CSKG named graph metrics | Continue using named graph queries only |
| SPARQL endpoint | Satisfied | `POST /query` returns named graph counts and use-case results | Keep saved runtime evidence updated |
| SEPSES CVE linking | Partially satisfied | `/stats` reports `total_sepses_cve_uri = 11` | Extend linking beyond CVE where appropriate |
| Summary/statistics | Satisfied for KG statistics | `/stats` works and final evidence is documented | Natural-language reports still depend on Gemini quota |
| Threat actor analysis | Partially satisfied | `total_threat_actors = 60` | Validate actor relation quality and coverage |
| TTL dump | Satisfied when regenerated | `server/cskg_dump.py` exports the named graph | Re-dump after every major graph build |

## Final Requirement Evaluation

| Requirement | Final Status | Evidence |
|---|---|---|
| Triple count | Completed | 1009 named graph triples |
| Entity counts per class | Completed | `/stats` endpoint |
| SEPSES linking rate | Partially completed | 11 SEPSES CVE URIs |
| Extraction precision/recall estimate | Qualitative / partial | Manual inspection and limitation notes |
| Known gaps/errors | Completed | Evaluation limitations section |

## Improvement Plan

Recommended next steps:

1. Resolve or monitor Gemini quota for automatic natural-language report generation.
2. Add or prioritize sources likely to mention richer threat actor, malware, vulnerability, and campaign context.
3. Improve extraction validation so relationship subjects and objects that appear as actor-like or malware-like entities are also typed when appropriate.
4. Extend external URI alignment beyond SEPSES CVE mapping, especially CWE and MITRE ATT&CK where applicable.
5. Re-run the pipeline on larger batches and regenerate `cskg_full_dump.ttl` after every major graph build.
