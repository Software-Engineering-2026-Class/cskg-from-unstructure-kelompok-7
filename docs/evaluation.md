# CSKG Evaluation

This document evaluates the current state of the Cybersecurity Knowledge Graph pipeline and generated graph.

## What Works

The current pipeline is functional end-to-end for the latest run.

Successful components:

- RSS producer collected 8 articles from configured cybersecurity sources.
- Extractor processed the 8 queued articles.
- Graph builder inserted 83 triples into the named graph `<http://group2.org/cskg>`.
- Redis queues are draining correctly for the processed batch; `extractions_queue` is empty after graph insertion.
- Virtuoso is reachable at the configured SPARQL endpoint.
- FastAPI can query Virtuoso through `POST /query`.
- `GET /` now distinguishes global Virtuoso triples from CSKG named graph triples.
- `GET /stats` now reports named graph statistics.
- `cskg_full_dump.ttl` has been regenerated from the live CSKG named graph.
- SEPSES CVE URI linking is present for at least one CVE resource.

Current graph summary:

| Metric | Value |
|---|---:|
| Total CSKG named graph triples | 83 |
| Reports | 8 |
| Vulnerabilities | 5 |
| Malware | 1 |
| Indicators | 2 |
| Attack patterns | 9 |
| Threat actors | 0 |
| SEPSES CVE URIs | 1 |

## What Is Still Missing

The current run does not yet cover all desired knowledge graph quality goals.

Missing or weak areas:

- No `stix:ThreatActor` entities were extracted in this run.
- No threat actor relationship summary could be generated from actor-tool relations.
- Some extracted relationships point to untyped object nodes, for example target or related concept URIs that do not yet have explicit RDF types.
- The graph is still small, with 83 triples from 8 reports.
- The summary report was not written because Gemini quota blocked LLM generation.

## Errors and Limitations

### Gemini Quota Issue

The summary fallback path was triggered, but report generation failed due to Gemini quota exhaustion.

Observed behavior:

```text
[SUMMARY] System Healthy. CSKG Named Graph Triples: 83
[SUMMARY] No threat actor relationships found. Using fallback graph summary.
[SUMMARY] Generating report for 2026-05-19...
429 RESOURCE_EXHAUSTED
Quota exceeded for model: gemini-2.0-flash-lite
```

Impact:

- The graph statistics and fallback summary input are available.
- The Markdown report cannot be generated until Gemini quota or API configuration is resolved.
- This is an external LLM availability issue, not an RDF/Virtuoso/API issue.

### ThreatActor Missing in This Run

The latest 8-article run produced:

```text
ThreatActor = 0
```

Possible causes that need further checking:

- The specific article summaries may not explicitly mention named threat actors.
- The extractor prompt may be conservative or inconsistent for actor extraction.
- RSS summaries may be too short compared to full article text.
- Extracted actor-like strings may have been emitted as untyped relationship subjects instead of typed `stix:ThreatActor` entities.

Impact:

- Threat actor profiling use-cases cannot be demonstrated from this run.
- Summary had to fallback to vulnerabilities, malware, attack patterns, indicators, and graph stats.

## Evaluation of Current Requirements

| Requirement | Current Status | Evidence | Remaining Work |
|---|---|---|---|
| Multiple unstructured sources | Partially satisfied | RSS source pipeline processed 8 articles | Document all configured sources and add more source coverage if required |
| RDF knowledge graph | Satisfied for current run | 83 triples in `<http://group2.org/cskg>` | Grow graph with more articles and better typing |
| Named graph correctness | Satisfied | `GET /` and `/stats` report CSKG named graph metrics | Re-run after larger graph builds |
| SPARQL endpoint | Satisfied | `POST /query` returns named graph count and distributions | Add saved example query outputs if needed |
| SEPSES CVE linking | Partially satisfied | `/stats` reports `total_sepses_cve_uri = 1` | Add more CVE-containing sources and validate links |
| Summary/statistics | Partially satisfied | `/stats` works; fallback starts | Gemini quota blocks report generation |
| Threat actor analysis | Missing in this run | `total_threat_actors = 0` | Improve data/source/prompt coverage for actor extraction |
| TTL dump | Satisfied | `cskg_full_dump.ttl` regenerated from named graph | Re-dump after every major graph build |

## Improvement Plan

Recommended next steps:

1. Resolve Gemini quota by using a valid project/key with available quota, waiting for quota reset, or switching to an approved model only after confirming assignment constraints.
2. Add or prioritize sources likely to mention threat actors, such as CISA advisories, vendor threat reports, Mandiant, CrowdStrike, or curated threat intel blogs.
3. Improve extraction validation so relationship subjects and objects that appear as actor-like or malware-like entities are also typed when appropriate.
4. Re-run the pipeline on a larger article batch and regenerate `cskg_full_dump.ttl`.
5. Save example SPARQL query outputs for the three real-world use-cases under `docs/evidence/` after the graph grows.
