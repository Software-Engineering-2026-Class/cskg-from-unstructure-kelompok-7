# Runtime Verification Evidence

Verification date: 2026-05-20

## Pipeline Status

The CSKG pipeline has successfully processed the current batch end-to-end:

- RSS producer collected 8 articles.
- Extractor processed the 8 articles.
- Graph builder inserted 83 triples into the named graph `<http://group2.org/cskg>`.
- `extractions_queue` is empty after graph builder execution.
- Virtuoso is reachable through the API and SPARQL endpoint.
- Summary fallback logic is reachable, but report generation is blocked by Gemini quota.

## GET / Response

Runtime response from `GET http://localhost:8000/` after hotfix:

```json
{
  "status": "online",
  "graph_db_backend": "Virtuoso",
  "sparql_endpoint": "http://virtuoso:8890/sparql",
  "named_graph": "http://group2.org/cskg",
  "global_triples": 5830,
  "cskg_named_graph_triples": 83
}
```

## GET /stats Response

Runtime response from `GET http://localhost:8000/stats` after hotfix:

```json
{
  "named_graph": "http://group2.org/cskg",
  "total_triples": 83,
  "count_by_type": {
    "http://docs.oasis-open.org/cti/ns/stix#AttackPattern": 9,
    "http://docs.oasis-open.org/cti/ns/stix#Report": 8,
    "http://docs.oasis-open.org/cti/ns/stix#Vulnerability": 5,
    "http://docs.oasis-open.org/cti/ns/stix#Indicator": 2,
    "http://docs.oasis-open.org/cti/ns/stix#Malware": 1
  },
  "count_by_predicate": {
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": 25,
    "http://docs.oasis-open.org/cti/ns/stix#mentions": 17,
    "http://www.w3.org/2000/01/rdf-schema#label": 17,
    "http://purl.org/dc/terms/created": 8,
    "http://docs.oasis-open.org/cti/ns/stix#patched": 5,
    "http://docs.oasis-open.org/cti/ns/stix#targets": 4,
    "http://docs.oasis-open.org/cti/ns/stix#exploits": 2,
    "http://docs.oasis-open.org/cti/ns/stix#uses": 2,
    "http://docs.oasis-open.org/cti/ns/stix#reports": 2,
    "http://docs.oasis-open.org/cti/ns/stix#variant_of": 1
  },
  "total_reports": 8,
  "total_vulnerabilities": 5,
  "total_malware": 1,
  "total_indicators": 2,
  "total_attack_patterns": 9,
  "total_threat_actors": 0,
  "total_sepses_cve_uri": 1
}
```

## Named Graph Triple Count

SPARQL query:

```sparql
SELECT (COUNT(*) AS ?triples)
WHERE {
  GRAPH <http://group2.org/cskg> {
    ?s ?p ?o .
  }
}
```

Observed result:

```json
{
  "variables": ["triples"],
  "results": [
    {
      "triples": "83"
    }
  ]
}
```

## Entity Type Distribution

SPARQL query:

```sparql
SELECT ?type (COUNT(DISTINCT ?s) AS ?count)
WHERE {
  GRAPH <http://group2.org/cskg> {
    ?s a ?type .
  }
}
GROUP BY ?type
ORDER BY DESC(?count)
```

Observed result:

| Entity type | Count |
|---|---:|
| `http://docs.oasis-open.org/cti/ns/stix#AttackPattern` | 9 |
| `http://docs.oasis-open.org/cti/ns/stix#Report` | 8 |
| `http://docs.oasis-open.org/cti/ns/stix#Vulnerability` | 5 |
| `http://docs.oasis-open.org/cti/ns/stix#Indicator` | 2 |
| `http://docs.oasis-open.org/cti/ns/stix#Malware` | 1 |
| `http://docs.oasis-open.org/cti/ns/stix#ThreatActor` | 0 |

## Predicate Distribution

SPARQL query:

```sparql
SELECT ?p (COUNT(*) AS ?count)
WHERE {
  GRAPH <http://group2.org/cskg> {
    ?s ?p ?o .
  }
}
GROUP BY ?p
ORDER BY DESC(?count)
```

Observed result:

| Predicate | Count |
|---|---:|
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` | 25 |
| `http://docs.oasis-open.org/cti/ns/stix#mentions` | 17 |
| `http://www.w3.org/2000/01/rdf-schema#label` | 17 |
| `http://purl.org/dc/terms/created` | 8 |
| `http://docs.oasis-open.org/cti/ns/stix#patched` | 5 |
| `http://docs.oasis-open.org/cti/ns/stix#targets` | 4 |
| `http://docs.oasis-open.org/cti/ns/stix#exploits` | 2 |
| `http://docs.oasis-open.org/cti/ns/stix#uses` | 2 |
| `http://docs.oasis-open.org/cti/ns/stix#reports` | 2 |
| `http://docs.oasis-open.org/cti/ns/stix#variant_of` | 1 |

## TTL Dump Status

`cskg_full_dump.ttl` has been regenerated from the live named graph `<http://group2.org/cskg>` using `server/cskg_dump.py`.

Evidence:

- Output file: `cskg_full_dump.ttl`
- Size observed: `4.6K`
- Modified time observed: `2026-05-20 00:40 +0700`
- Content begins with current CSKG entities from the 2026 RSS run, such as `trapdoor`, `ad fraud`, `DirtyDecrypt`, and current article URLs.
- The dump does not contain Virtuoso internal graph triples as its primary content.

## Gemini Quota Limitation

Summary fallback was triggered successfully, but report generation failed because Gemini returned quota exhaustion.

Observed summary worker evidence:

```text
[SUMMARY] System Healthy. CSKG Named Graph Triples: 83
[SUMMARY] No threat actor relationships found. Using fallback graph summary.
[SUMMARY] Generating report for 2026-05-19...
```

Observed Gemini error:

```text
429 RESOURCE_EXHAUSTED
Quota exceeded for model: gemini-2.0-flash-lite
```

Impact:

- The graph, API, stats endpoint, and TTL dump are usable.
- Automated natural-language report generation is blocked until Gemini quota/API key/model availability is resolved.
