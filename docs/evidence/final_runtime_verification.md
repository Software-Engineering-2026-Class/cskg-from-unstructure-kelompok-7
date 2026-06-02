# Final Runtime Verification

Verification date: 2026-06-01

## API Status

Endpoint:
`GET http://localhost:8000/`

Observed result:
- status: online
- graph_db_backend: Virtuoso
- named_graph: `http://group2.org/cskg`
- global_triples: 6423
- cskg_named_graph_triples: 963

## KG Statistics

Endpoint:
`GET http://localhost:8000/stats`

Observed result:
- total triples: 963
- reports: 89
- vulnerabilities: 27
- malware: 24
- indicators: 11
- attack patterns: 81
- threat actors: 58
- SEPSES CVE URIs: 11

## Evaluation Summary

The final graph is significantly larger than the earlier runtime verification. The CSKG named graph now contains 963 triples, 89 reports, 58 threat actors, and 11 SEPSES-linked CVE URIs.

## Known Limitations

- The graph is still limited to the collected RSS/API batch.
- SEPSES linking is strongest for CVE URI mapping, with 11 SEPSES CVE URIs in the latest graph.
- CWE and MITRE ATT&CK URI alignment are not fully implemented yet.
- Automatic natural-language report generation may still be affected by Gemini quota limits.
- Extraction quality depends on the source article summaries and Gemini output consistency.
