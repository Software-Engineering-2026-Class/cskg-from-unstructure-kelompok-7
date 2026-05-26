# Use Case Runtime Outputs

Verification date: 2026-05-26  
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
  - total triples: 676
  - reports: 61
  - threat actors: 32
  - vulnerabilities: 19
  - malware: 17
  - indicators: 10
  - attack patterns: 67

Sample output:

```json
{
  "variables": ["metric", "value"],
  "results": [
    {
      "metric": "total_triples",
      "value": "676"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#AttackPattern",
      "value": "67"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#Indicator",
      "value": "10"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#Malware",
      "value": "17"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#Report",
      "value": "61"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#ThreatActor",
      "value": "32"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#Vulnerability",
      "value": "19"
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
- Rows returned: 9
- Key findings:
  - SEPSES-linked CVE result rows: 9
  - Unique SEPSES-linked CVE URIs: 8
  - `CVE-2026-9082` appears in two separate source reports.

SEPSES-linked CVE URI(s):
- `https://w3id.org/sepses/resource/cve/CVE-2025-34291`
- `https://w3id.org/sepses/resource/cve/CVE-2025-52691`
- `https://w3id.org/sepses/resource/cve/CVE-2026-20223`
- `https://w3id.org/sepses/resource/cve/CVE-2026-26980`
- `https://w3id.org/sepses/resource/cve/CVE-2026-41091`
- `https://w3id.org/sepses/resource/cve/CVE-2026-46333`
- `https://w3id.org/sepses/resource/cve/CVE-2026-48172`
- `https://w3id.org/sepses/resource/cve/CVE-2026-9082`

Sample output:

```json
{
  "variables": ["cve", "label", "report"],
  "results": [
    {
      "cve": "https://w3id.org/sepses/resource/cve/CVE-2025-34291",
      "label": "CVE-2025-34291",
      "report": "https://thehackernews.com/2026/05/cisa-adds-exploited-langflow-and-trend.html"
    },
    {
      "cve": "https://w3id.org/sepses/resource/cve/CVE-2025-52691",
      "label": "CVE-2025-52691",
      "report": "https://fortiguard.fortinet.com/outbreak-alert/smartertools-smartermail-rce"
    },
    {
      "cve": "https://w3id.org/sepses/resource/cve/CVE-2026-20223",
      "label": "CVE-2026-20223",
      "report": "https://thehackernews.com/2026/05/cisco-patches-cvss-100-secure-workload.html"
    },
    {
      "cve": "https://w3id.org/sepses/resource/cve/CVE-2026-26980",
      "label": "CVE-2026-26980",
      "report": "https://www.bleepingcomputer.com/news/security/ghost-cms-sql-injection-flaw-exploited-in-large-scale-clickfix-campaign/"
    },
    {
      "cve": "https://w3id.org/sepses/resource/cve/CVE-2026-41091",
      "label": "CVE-2026-41091",
      "report": "https://thehackernews.com/2026/05/microsoft-warns-of-two-actively.html"
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
- Rows returned: 161
- Key findings:
  - attack pattern entities found: 67
  - malware entities found: 17
  - rows with relationship context: 78
  - examples include `Scams`, `Supply chain attack`, and related entities such as `cryptocurrencykiosks` and `packagist`.

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
      "entity": "http://group2.org/cskg/scams",
      "entity_type": "http://docs.oasis-open.org/cti/ns/stix#AttackPattern",
      "label": "Scams",
      "relationship": "http://docs.oasis-open.org/cti/ns/stix#uses",
      "related_entity": "http://group2.org/cskg/cryptocurrencykiosks",
      "related_label": null,
      "report": "https://www.bleepingcomputer.com/news/security/fbi-americans-lost-over-388-million-to-scams-using-crypto-atms-in-2025/"
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
