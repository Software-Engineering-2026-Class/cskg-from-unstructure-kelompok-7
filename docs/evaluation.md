# CSKG Evaluation

This document evaluates the final runtime state of the Cybersecurity Knowledge Graph pipeline and generated graph.

## What Works

The current pipeline is functional end-to-end for the final verified run.

Successful components:

- The producer collected articles from the configured RSS/API sources.
- The extractor processed queued articles and produced cybersecurity entity/relation extractions.
- The graph builder inserted 1227 triples into the named graph `<http://group2.org/cskg>`.
- Redis queues are draining correctly for the processed batch; `extractions_queue` is empty after graph insertion.
- Virtuoso is reachable at the configured SPARQL endpoint.
- FastAPI can query Virtuoso through `POST /query`.
- `GET /` now distinguishes global Virtuoso triples from CSKG named graph triples.
- `GET /stats` now reports named graph statistics.
- SEPSES CVE URI linking is present for 22 CVE resources.
- Threat actor extraction improved from 0 entities in the earlier runtime snapshot to 70 entities in the final verified graph.

Final graph summary:

| Metric | Value |
|---|---:|
| Total CSKG named graph triples | 1227 |
| Reports | 117 |
| Vulnerabilities | 46 |
| Malware | 30 |
| Indicators | 14 |
| Attack patterns | 95 |
| Threat actors | 70 |
| SEPSES CVE URIs | 22 |

## What Is Still Missing

The final run covers the main runtime requirements, but it does not yet cover all desired knowledge graph quality goals.

Missing or weak areas:

- Some extracted relationships point to untyped object nodes, for example target or related concept URIs that do not yet have explicit RDF types.
- The graph is still limited to the collected RSS/API batch.
- SEPSES linking is currently strongest for CVE URI mapping, with 22 SEPSES CVE URIs in the latest graph; CWE and MITRE ATT&CK URI alignment remain future work.
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
ThreatActor = 70
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
| Multiple unstructured sources | Partially satisfied | RSS/API source pipeline produced 117 reports | Continue expanding source coverage |
| RDF knowledge graph | Satisfied for final run | 1227 triples in `<http://group2.org/cskg>` | Improve typing and external alignment |
| Named graph correctness | Satisfied | `GET /` and `/stats` report CSKG named graph metrics | Continue using named graph queries only |
| SPARQL endpoint | Satisfied | `POST /query` returns named graph counts and use-case results | Keep saved runtime evidence updated |
| SEPSES CVE linking | Partially satisfied | `/stats` reports `total_sepses_cve_uri = 22` | Extend linking beyond CVE where appropriate |
| Summary/statistics | Satisfied for KG statistics | `/stats` works and final evidence is documented | Natural-language reports still depend on Gemini quota |
| Threat actor analysis | Partially satisfied | `total_threat_actors = 70` | Validate actor relation quality and coverage |
| TTL dump | Satisfied and automated | `ttl_dump` service runs `server/cskg_dump.py` and validates the dump | Monitor dump worker logs |

## Final Requirement Evaluation

| Requirement | Final Status | Evidence |
|---|---|---|
| Triple count | Completed | 1227 named graph triples |
| Entity counts per class | Completed | `/stats` endpoint |
| SEPSES linking rate | Partially completed | 22 SEPSES CVE URIs |
| Extraction precision/recall estimate | Qualitative / partial | Manual inspection and limitation notes |
| Known gaps/errors | Completed | Evaluation limitations section |

## Evaluation of Generated Turtle Output

The generated Turtle output `cskg_full_dump.ttl` was regenerated from the Virtuoso named graph `<http://group2.org/cskg>` and validated using `rdflib`.

### Validation Result

The Turtle file was parsed successfully using `rdflib`, which confirms that the generated `.ttl` file is syntactically valid RDF/Turtle.

```bash
python - <<'PY'
from rdflib import Graph

g = Graph()
g.parse("cskg_full_dump.ttl", format="turtle")
print("TTL triples:", len(g))
PY
```

Observed result:

```text
TTL triples: 1227
```

### 1. Completeness

The final Turtle dump contains 1227 RDF triples generated from the final collected RSS/API batch. The output includes reports and extracted cybersecurity entities across the main CSKG categories.

| Metric | Value |
|---|---:|
| Total RDF triples | 1227 |
| Reports | 117 |
| Vulnerabilities | 46 |
| Malware | 30 |
| Indicators | 14 |
| Attack patterns | 95 |
| Threat actors | 70 |
| SEPSES CVE URIs | 22 |

Based on this result, the Turtle output is considered complete for the final collected dataset batch. However, it is not intended to represent the entire cybersecurity domain.

### 2. STIX Mapping Coverage

The generated entities are mapped into STIX-style RDF classes.

| Entity Category | RDF/STIX Class | Status |
|---|---|---|
| Reports | `stix:Report` | Covered |
| Threat actors | `stix:ThreatActor` | Covered |
| Malware | `stix:Malware` | Covered |
| Vulnerabilities | `stix:Vulnerability` | Covered |
| Indicators | `stix:Indicator` | Covered |
| Attack patterns | `stix:AttackPattern` | Covered |

The graph also uses STIX-style relationship predicates, including `stix:mentions`, `stix:uses`, `stix:targets`, `stix:exploits`, `stix:patched`, `stix:reports`, `stix:observes`, `stix:disrupted`, and `stix:propagated_via`.

### 3. Integration and Linking

The generated Turtle output contains meaningful links between reports and extracted cybersecurity entities. Reports are connected to extracted entities using `stix:mentions`, while other entity-to-entity relations are represented using predicates such as `stix:uses`, `stix:targets`, `stix:exploits`, `stix:patched`, and `stix:reports`.

External linking is also present through SEPSES CVE URIs. CVE-formatted vulnerabilities are mapped to the SEPSES CVE namespace instead of only using local CSKG URIs. Entity normalization is represented using `owl:sameAs` for cases where raw labels and canonical local URIs refer to the same concept.

| Linking Type | Evidence |
|---|---|
| Report-to-entity linking | `stix:mentions` |
| Threat actor / malware / vulnerability relations | `stix:uses`, `stix:targets`, `stix:exploits` |
| Patch/reporting relations | `stix:patched`, `stix:reports` |
| Entity normalization | `owl:sameAs` |
| External CVE linking | 22 SEPSES CVE URIs |

### Interactive Visual Evidence

An offline interactive JavaScript network visualization is available at:

`docs/visualization/cskg_full_network_offline_canvas.html`

The visualization uses the generated `cskg_full_dump.ttl` output to inspect graph completeness, STIX-style entity coverage, and integration/linking relationships. It supports node type filters, predicate filters, search, zoom, pan, and node/edge detail inspection.

This visual evidence supports the integration/linking evaluation by showing relationships such as `stix:mentions`, `stix:uses`, `stix:targets`, `stix:exploits`, `stix:patched`, `stix:reports`, and `owl:sameAs`.

### Known Limitations

- The graph is complete for the final collected RSS/API batch, but it is not intended to represent the entire cybersecurity domain.
- External SEPSES linking is currently implemented primarily for CVE-based vulnerability entities.
- The graph uses STIX-style classes and predicates, but direct URI alignment to CWE and MITRE ATT&CK knowledge bases remains future work.
- Some extracted entities are represented as local CSKG URIs when no external standardized URI mapping is available.

### Conclusion

The generated `cskg_full_dump.ttl` output satisfies the final project scope for generated output evaluation. It is valid Turtle, contains 1227 RDF triples, covers the main STIX-style cybersecurity entity classes, and includes integration/linking between reports, extracted entities, normalized entities, and SEPSES-linked CVE resources.

## Improvement Plan

Recommended next steps:

1. Resolve or monitor Gemini quota for automatic natural-language report generation.
2. Add or prioritize sources likely to mention richer threat actor, malware, vulnerability, and campaign context.
3. Improve extraction validation so relationship subjects and objects that appear as actor-like or malware-like entities are also typed when appropriate.
4. Extend external URI alignment beyond SEPSES CVE mapping, especially CWE and MITRE ATT&CK where applicable.
5. Re-run the pipeline on larger batches and regenerate `cskg_full_dump.ttl` after every major graph build.
