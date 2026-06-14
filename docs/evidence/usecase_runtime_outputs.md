# Use Case Runtime Outputs

Verification date: 2026-06-02  
Named graph: `<http://group2.org/cskg>`

All queries were executed through the local FastAPI endpoint `POST http://localhost:8000/query` and explicitly scoped to the CSKG named graph with `GRAPH <http://group2.org/cskg>`.

## Use Case 1 — KG Statistics

Purpose:
Shows current CSKG statistics such as total triples and entity distribution.

Query file:
`queries/usecases/usecase_1_kg_statistics.rq`

Runtime result:
- Rows returned: 7
- Key findings:
  - total triples: 1227
  - reports: 117
  - threat actors: 70
  - vulnerabilities: 46
  - malware: 30
  - indicators: 14
  - attack patterns: 95

Sample output:

```json
{
  "variables": ["metric", "value"],
  "results": [
    {
      "metric": "total_triples",
      "value": "1227"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#AttackPattern",
      "value": "95"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#Indicator",
      "value": "14"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#Malware",
      "value": "30"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#Report",
      "value": "117"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#ThreatActor",
      "value": "70"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#Vulnerability",
      "value": "46"
    }
  ]
}
```

## Use Case 2 — Vulnerability / SEPSES CVE Linking

Purpose:
Demonstrates how CVE vulnerabilities extracted from unstructured sources are linked to SEPSES CVE URIs.

Query file:
`queries/usecases/usecase_2_vulnerability_sepses_linking.rq`

Runtime result:
- Rows returned: 24
- Key findings:
  - SEPSES-linked CVE result rows: 24
  - Unique SEPSES-linked CVE URIs: 22
  - `CVE-2024-38063` and `CVE-2024-38106` appear in multiple source reports.

SEPSES-linked CVE URI(s):
- `https://w3id.org/sepses/resource/cve/CVE-1999-0082`
- `https://w3id.org/sepses/resource/cve/CVE-1999-0095`
- `https://w3id.org/sepses/resource/cve/CVE-2023-38035`
- `https://w3id.org/sepses/resource/cve/CVE-2023-38036`
- `https://w3id.org/sepses/resource/cve/CVE-2024-38063`
- `https://w3id.org/sepses/resource/cve/CVE-2024-38106`
- `https://w3id.org/sepses/resource/cve/CVE-2024-38107`
- `https://w3id.org/sepses/resource/cve/CVE-2025-8088`
- `https://w3id.org/sepses/resource/cve/CVE-2026-0257`
- `https://w3id.org/sepses/resource/cve/CVE-2026-20230`
- `https://w3id.org/sepses/resource/cve/CVE-2026-20245`
- `https://w3id.org/sepses/resource/cve/CVE-2026-20253`
- `https://w3id.org/sepses/resource/cve/CVE-2026-23111`
- `https://w3id.org/sepses/resource/cve/CVE-2026-25089`
- `https://w3id.org/sepses/resource/cve/CVE-2026-28318`
- `https://w3id.org/sepses/resource/cve/CVE-2026-3055`
- `https://w3id.org/sepses/resource/cve/CVE-2026-3300`
- `https://w3id.org/sepses/resource/cve/CVE-2026-35273`
- `https://w3id.org/sepses/resource/cve/CVE-2026-42271`
- `https://w3id.org/sepses/resource/cve/CVE-2026-44963`
- `https://w3id.org/sepses/resource/cve/CVE-2026-45247`
- `https://w3id.org/sepses/resource/cve/CVE-2026-5027`

Sample output:

```json
{
  "variables": ["cve", "label", "report"],
  "results": [
    {
      "cve": "https://w3id.org/sepses/resource/cve/CVE-1999-0082",
      "label": "CVE-1999-0082",
      "report": "https://nvd.nist.gov/vuln/detail/CVE-1999-0082"
    },
    {
      "cve": "https://w3id.org/sepses/resource/cve/CVE-1999-0095",
      "label": "CVE-1999-0095",
      "report": "https://nvd.nist.gov/vuln/detail/CVE-1999-0095"
    },
    {
      "cve": "https://w3id.org/sepses/resource/cve/CVE-2023-38035",
      "label": "CVE-2023-38035",
      "report": "https://www.bleepingcomputer.com/news/security/new-max-severity-ivanti-sentry-flaw-allows-code-execution-as-root/"
    },
    {
      "cve": "https://w3id.org/sepses/resource/cve/CVE-2023-38036",
      "label": "CVE-2023-38036",
      "report": "https://www.bleepingcomputer.com/news/security/new-max-severity-ivanti-sentry-flaw-allows-code-execution-as-root/"
    },
    {
      "cve": "https://w3id.org/sepses/resource/cve/CVE-2024-38063",
      "label": "CVE-2024-38063",
      "report": "https://www.bleepingcomputer.com/news/microsoft/microsoft-patches-yellowkey-greenplasma-miniplasma-zero-days/"
    }
  ]
}
```

## Use Case 3 — Attack Pattern and Malware Context

Purpose:
Shows how attack patterns or malware entities can be traced back to reports and related graph context.

Query file:
`queries/usecases/usecase_3_attack_pattern_malware_context.rq`

Runtime result:
- Rows returned: 240
- Key findings:
  - attack pattern entities found: 95
  - malware entities found: 30
  - examples include `AI-driven attacks`, `Authentication bypass`, and related report context.

Sample output:

```json
{
  "variables": [
    "entity",
    "entity_type",
    "label",
    "relationship",
    "related_entity",
    "related_label",
    "report"
  ],
  "results": [
    {
      "entity": "http://group2.org/cskg/aidrivenattacks",
      "entity_type": "http://docs.oasis-open.org/cti/ns/stix#AttackPattern",
      "label": "AI-driven attacks",
      "relationship": null,
      "related_entity": null,
      "related_label": null,
      "report": "https://www.bleepingcomputer.com/news/security/why-ai-driven-threats-are-exposing-the-limits-of-msp-security-stacks/"
    },
    {
      "entity": "http://group2.org/cskg/supplychainattack",
      "entity_type": "http://docs.oasis-open.org/cti/ns/stix#AttackPattern",
      "label": "Supply chain attack",
      "relationship": "http://docs.oasis-open.org/cti/ns/stix#targets",
      "related_entity": "http://group2.org/cskg/packagist",
      "related_label": null,
      "report": "https://www.bleepingcomputer.com/news/security/grafana-breach-caused-by-missed-token-rotation-after-tanstack-attack/"
    },
    {
      "entity": "http://group2.org/cskg/supplychainattack",
      "entity_type": "http://docs.oasis-open.org/cti/ns/stix#AttackPattern",
      "label": "Supply chain attack",
      "relationship": "http://docs.oasis-open.org/cti/ns/stix#targets",
      "related_entity": "http://group2.org/cskg/packagist",
      "related_label": null,
      "report": "https://www.bleepingcomputer.com/news/security/laravel-lang-packages-hijacked-to-deploy-credential-stealing-malware/"
    },
    {
      "entity": "http://group2.org/cskg/supplychainattack",
      "entity_type": "http://docs.oasis-open.org/cti/ns/stix#AttackPattern",
      "label": "Supply chain attack",
      "relationship": "http://docs.oasis-open.org/cti/ns/stix#targets",
      "related_entity": "http://group2.org/cskg/packagist",
      "related_label": null,
      "report": "https://thehackernews.com/2026/05/packagist-supply-chain-attack-infects-8.html"
    }
  ]
}
```

## Limitations Found During Runtime Validation

- Some related entities are untyped or do not have `rdfs:label`, for example `http://group2.org/cskg/packagist` and `http://group2.org/cskg/cryptocurrencykiosks` in the sampled Use Case 3 output.
- Use Case 3 returns one row per matching report and relationship combination, so repeated entities such as `Supply chain attack` are expected when the same entity appears in multiple reports.
- Screenshots were not captured in this validation run. The Markdown runtime outputs above provide reproducible API evidence.
