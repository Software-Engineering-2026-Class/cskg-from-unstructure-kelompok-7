# Final Runtime Verification

Verification date: 2026-06-02

## API Status

Endpoint:
`GET http://localhost:8000/`

Observed result:
- status: online
- graph_db_backend: Virtuoso
- named_graph: `http://group2.org/cskg`
- global_triples: 6974
- cskg_named_graph_triples: 1227

## KG Statistics

Endpoint:
`GET http://localhost:8000/stats`

Observed result:
- total triples: 1227
- reports: 117
- vulnerabilities: 46
- malware: 30
- indicators: 14
- attack patterns: 95
- threat actors: 70
- SEPSES CVE URIs: 22

## Use-Case Query Results

The three saved use-case queries were executed through `POST http://localhost:8000/query` against the CSKG named graph.

Observed row counts:
- Use Case 1, KG statistics and coverage: 7 rows
- Use Case 2, vulnerability linking to SEPSES CVE: 24 rows
- Use Case 3, attack pattern and malware context: 240 rows

## Evaluation Summary

The final graph is significantly larger than the earlier runtime verification. The CSKG named graph now contains 1227 triples, 117 reports, 70 threat actors, and 22 SEPSES-linked CVE URIs.

## Turtle Dump Validation

The final Turtle dump `cskg_full_dump.ttl` was regenerated from the Virtuoso named graph `<http://group2.org/cskg>` and validated with `rdflib`.

Observed result:

```text
TTL triples: 1227
```

The Docker Compose pipeline now includes a `ttl_dump` service for automatic periodic dumping.

## Known Limitations

- The graph is still limited to the collected RSS/API batch.
- SEPSES linking is strongest for CVE URI mapping, with 22 SEPSES CVE URIs in the latest graph.
- CWE and MITRE ATT&CK URI alignment are not fully implemented yet.
- Automatic natural-language report generation may still be affected by Gemini quota limits.
- Extraction quality depends on the source article summaries and Gemini output consistency.
