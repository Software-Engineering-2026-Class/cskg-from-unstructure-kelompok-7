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
- cskg_named_graph_triples: 676

## KG Statistics

Endpoint:
`GET http://localhost:8000/stats`

Observed result:
- total triples: 676
- reports: 61
- vulnerabilities: 19
- malware: 17
- indicators: 10
- attack patterns: 67
- threat actors: 32
- SEPSES CVE URIs: 8

## Evaluation Summary

The final graph is significantly larger than the earlier runtime verification. The CSKG named graph now contains 676 triples, 61 reports, 32 threat actors, and 8 SEPSES-linked CVE URIs.

## Known Limitations

- The graph is still limited to the collected RSS/API batch.
- SEPSES linking is strongest for CVE URI mapping.
- CWE and MITRE ATT&CK URI alignment are not fully implemented yet.
- Automatic natural-language report generation may still be affected by Gemini quota limits.
- Extraction quality depends on the source article summaries and Gemini output consistency.
