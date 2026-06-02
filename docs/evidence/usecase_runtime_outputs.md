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
  - total triples: 1009
  - reports: 94
  - threat actors: 60
  - vulnerabilities: 30
  - malware: 25
  - indicators: 11
  - attack patterns: 85

Sample output:

```json
{
  "variables": ["metric", "value"],
  "results": [
    {
      "metric": "total_triples",
      "value": "1009"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#AttackPattern",
      "value": "85"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#Indicator",
      "value": "11"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#Malware",
      "value": "25"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#Report",
      "value": "94"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#ThreatActor",
      "value": "60"
    },
    {
      "metric": "type_count:http://docs.oasis-open.org/cti/ns/stix#Vulnerability",
      "value": "30"
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
- Rows returned: 13
- Key findings:
  - SEPSES-linked CVE result rows: 13
  - Unique SEPSES-linked CVE URIs: 11
  - `CVE-2026-0257` and `CVE-2026-9082` appear in multiple source reports.

SEPSES-linked CVE URI(s):
- `https://w3id.org/sepses/resource/cve/CVE-2025-34291`
- `https://w3id.org/sepses/resource/cve/CVE-2025-52691`
- `https://w3id.org/sepses/resource/cve/CVE-2026-0257`
- `https://w3id.org/sepses/resource/cve/CVE-2026-20223`
- `https://w3id.org/sepses/resource/cve/CVE-2026-26980`
- `https://w3id.org/sepses/resource/cve/CVE-2026-30844`
- `https://w3id.org/sepses/resource/cve/CVE-2026-31260`
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
      "cve": "https://w3id.org/sepses/resource/cve/CVE-2026-0257",
      "label": "CVE-2026-0257",
      "report": "https://thehackernews.com/2026/05/pan-os-globalprotect-authentication.html"
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
- Rows returned: 241
- Key findings:
  - attack pattern entities found: 85
  - malware entities found: 25
  - examples include `AI-generated lures`, `Supply chain attack`, and related entities such as `cryptocurrencykiosks` and `packagist`.

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
      "entity": "http://group2.org/cskg/aigeneratedlures",
      "entity_type": "http://docs.oasis-open.org/cti/ns/stix#AttackPattern",
      "label": "AI-generated lures",
      "relationship": null,
      "related_entity": null,
      "related_label": null,
      "report": "https://www.bleepingcomputer.com/news/security/greyvibe-hackers-use-chatgpt-gemini-to-power-cyberattacks/"
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
