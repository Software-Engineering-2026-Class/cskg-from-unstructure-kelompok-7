# Contribution Summary

This document summarizes member contributions for the final CSKG project audit and Issue #10.

## Members

| Member | Main Contribution | Evidence |
|---|---|---|
| Axelle Chandra | README, final documentation coordination, issue evidence, use-case/evaluation evidence refresh | `README.md`, `docs/evidence/final_runtime_verification.md`, `docs/evidence/usecase_runtime_outputs.md`, GitHub issue comments |
| Danar Fathurahman | LLM extraction pipeline, worker flow, graph building/export, Virtuoso runtime verification | `pipeline/extractor.py`, `pipeline/extractor_worker.py`, `pipeline/build_kg.py`, `pipeline/builder_worker.py`, `server/cskg_dump.py`, issue #4/#6/#7 evidence |
| Kesya Izumi | Ontology design and documentation using STIX-style classes, predicates, SEPSES CVE URI mapping, known ontology gaps | `docs/ontology.md`, issue #3 evidence |
| Keyne Elvaretta | Additional source selection and source documentation, including Securelist, Check Point Research, SANS ISC, and NVD API | `pipeline/scraper.py`, `docs/data_sources.md`, issue #2 evidence |

## Completed Documentation Scope

- Project setup and runtime instructions are documented in `README.md`.
- Source rationale and access methods are documented in `docs/data_sources.md`.
- Ontology classes, predicates, SEPSES CVE mapping, and known gaps are documented in `docs/ontology.md`.
- Three SPARQL use-cases are documented in `docs/usecases.md`.
- Final runtime statistics are documented in `docs/evidence/final_runtime_verification.md`.
- Use-case runtime outputs are documented in `docs/evidence/usecase_runtime_outputs.md`.
- Evaluation, limitations, and improvement plan are documented in `docs/evaluation.md`.

## Final Runtime Evidence

The frozen final runtime evidence reports:

| Metric | Value |
|---|---:|
| CSKG named graph triples | 1009 |
| Reports | 94 |
| Vulnerabilities | 30 |
| Malware | 25 |
| Indicators | 11 |
| Attack patterns | 85 |
| Threat actors | 60 |
| SEPSES CVE URIs | 11 |

The final use-case row counts are:

| Use case | Rows |
|---|---:|
| KG statistics and coverage | 7 |
| Vulnerability linking to SEPSES CVE | 13 |
| Attack pattern and malware context | 241 |

## Remaining Future Work

- SEPSES alignment is complete for CVE URI mapping, but CWE and MITRE ATT&CK URI alignment remain future work.
- Automatic natural-language report generation can still be affected by Gemini quota limits.
- Extraction precision and recall are evaluated qualitatively because no gold-standard labeled dataset was created.
