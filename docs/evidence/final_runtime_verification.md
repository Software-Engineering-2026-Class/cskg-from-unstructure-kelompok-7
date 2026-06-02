# Final Runtime Verification

Verification date: 2026-06-02

## API Status

Endpoint:
`GET http://localhost:8000/`

Observed result:
- status: online
- graph_db_backend: Virtuoso
- named_graph: `http://group2.org/cskg`
- global_triples: 6756
- cskg_named_graph_triples: 1009

## KG Statistics

Endpoint:
`GET http://localhost:8000/stats`

Observed result:
- total triples: 1009
- reports: 94
- vulnerabilities: 30
- malware: 25
- indicators: 11
- attack patterns: 85
- threat actors: 60
- SEPSES CVE URIs: 11

## Use-Case Query Results

The three saved use-case queries were executed through `POST http://localhost:8000/query` against the CSKG named graph.

Observed row counts:
- Use Case 1, KG statistics and coverage: 7 rows
- Use Case 2, vulnerability linking to SEPSES CVE: 13 rows
- Use Case 3, attack pattern and malware context: 241 rows

## Evaluation Summary

The final graph is significantly larger than the earlier runtime verification. The CSKG named graph now contains 1009 triples, 94 reports, 60 threat actors, and 11 SEPSES-linked CVE URIs.

## Known Limitations

- The graph is still limited to the collected RSS/API batch.
- SEPSES linking is strongest for CVE URI mapping, with 11 SEPSES CVE URIs in the latest graph.
- CWE and MITRE ATT&CK URI alignment are not fully implemented yet.
- Automatic natural-language report generation may still be affected by Gemini quota limits.
- Extraction quality depends on the source article summaries and Gemini output consistency.
