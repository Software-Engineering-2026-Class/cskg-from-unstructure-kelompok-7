# CSKG Use Cases

This document describes three practical SPARQL use-cases for the current Cybersecurity Knowledge Graph stored in the named graph `<http://group2.org/cskg>`.

## Use Case 1: KG Statistics and Coverage

Query file: `queries/usecases/usecase_1_kg_statistics.rq`

### Purpose

Measure the size and type coverage of the constructed knowledge graph.

This use-case answers:

- How many triples are currently in the CSKG named graph?
- What entity types are present?
- Which entity categories are missing or underrepresented?

### Why the KG Helps

The knowledge graph stores entities and relationships from multiple unstructured cybersecurity sources in one queryable RDF graph. This makes it possible to measure graph coverage with one named-graph query instead of manually checking each source article or pipeline log.

### Query

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?metric ?value
WHERE {
  {
    SELECT ("total_triples" AS ?metric) (COUNT(*) AS ?value)
    WHERE {
      GRAPH <http://group2.org/cskg> {
        ?s ?p ?o .
      }
    }
  }
  UNION
  {
    SELECT (CONCAT("type_count:", STR(?type)) AS ?metric) (COUNT(DISTINCT ?s) AS ?value)
    WHERE {
      GRAPH <http://group2.org/cskg> {
        ?s rdf:type ?type .
      }
    }
    GROUP BY ?type
  }
}
ORDER BY ?metric
```

### Expected Output and Current Runtime Result

Expected output is a table of metrics such as:

| metric | value |
|---|---:|
| `total_triples` | 676 |
| `type_count:http://docs.oasis-open.org/cti/ns/stix#AttackPattern` | 67 |
| `type_count:http://docs.oasis-open.org/cti/ns/stix#Report` | 61 |
| `type_count:http://docs.oasis-open.org/cti/ns/stix#ThreatActor` | 32 |
| `type_count:http://docs.oasis-open.org/cti/ns/stix#Vulnerability` | 19 |
| `type_count:http://docs.oasis-open.org/cti/ns/stix#Malware` | 17 |
| `type_count:http://docs.oasis-open.org/cti/ns/stix#Indicator` | 10 |

Runtime validation on 2026-05-26 returned 7 rows from the named graph. Full evidence is stored in `docs/evidence/usecase_runtime_outputs.md`.

### Current Limitation

This use-case reports graph coverage only. It does not by itself prove extraction accuracy, entity normalization quality, or completeness of the source collection.

### Real-World Benefit

This helps analysts and project evaluators quickly understand graph completeness, extraction coverage, and data quality. It is useful for deciding whether the next improvement should target more sources, better extraction prompts, or ontology mapping fixes.

## Use Case 2: Vulnerability Linking to SEPSES CVE

Query file: `queries/usecases/usecase_2_vulnerability_sepses_linking.rq`

### Purpose

Validate that CVE vulnerabilities extracted from unstructured text are represented using SEPSES CVE URIs.

This use-case answers:

- Which vulnerabilities are linked to external SEPSES CVE resources?
- Which reports mention those CVEs?

### Why the KG Helps

The graph maps CVE-like vulnerability mentions to stable SEPSES CVE URIs. Analysts can use those URIs to connect extracted report evidence with external vulnerability knowledge, instead of treating CVE strings as isolated text mentions.

### Query

```sparql
PREFIX stix: <http://docs.oasis-open.org/cti/ns/stix#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?cve ?label ?report
WHERE {
  GRAPH <http://group2.org/cskg> {
    ?cve a stix:Vulnerability .
    FILTER(STRSTARTS(STR(?cve), "https://w3id.org/sepses/resource/cve/"))

    OPTIONAL { ?cve rdfs:label ?label . }
    OPTIONAL {
      ?report a stix:Report ;
              stix:mentions ?cve .
    }
  }
}
ORDER BY ?cve ?report
```

### Expected Output and Current Runtime Result

Expected output is a list of SEPSES-linked CVE entities, labels, and source reports.

Example expected row shape:

| cve | label | report |
|---|---|---|
| `https://w3id.org/sepses/resource/cve/CVE-2025-52691` | `CVE-2025-52691` | FortiGuard SmarterMail RCE report URI |

Runtime validation on 2026-05-26 returned 9 rows and 8 unique SEPSES-linked CVE URIs from the named graph. The current result includes CVEs such as `CVE-2025-34291`, `CVE-2025-52691`, `CVE-2026-20223`, and `CVE-2026-9082`. Full evidence is stored in `docs/evidence/usecase_runtime_outputs.md`.

### Current Limitation

This use-case validates URI mapping for extracted CVEs. It does not yet enrich the CVEs with external SEPSES attributes such as severity, affected products, or remediation metadata.

### Real-World Benefit

This supports vulnerability impact analysis. A security team can connect extracted CVE mentions from reports to external vulnerability knowledge graphs and enrich them with severity, affected products, or remediation information.

## Use Case 3: Attack Pattern and Malware Context

Query file: `queries/usecases/usecase_3_attack_pattern_malware_context.rq`

### Purpose

Retrieve malware and attack pattern entities with their labels, relationships, related entities, and source reports.

This use-case answers:

- What malware or attack patterns were extracted?
- Which reports mention them?
- What relationships were extracted around those entities?

### Why the KG Helps

The graph links malware and attack-pattern entities to reports and extracted relationships. Analysts can pivot from a technique or malware label to source reports and related concepts without reading every article manually.

### Query

```sparql
PREFIX stix: <http://docs.oasis-open.org/cti/ns/stix#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?entity ?entity_type ?label ?relationship ?related_entity ?related_label ?report
WHERE {
  GRAPH <http://group2.org/cskg> {
    VALUES ?entity_type {
      stix:AttackPattern
      stix:Malware
    }

    ?entity a ?entity_type .
    OPTIONAL { ?entity rdfs:label ?label . }

    OPTIONAL {
      ?entity ?relationship ?related_entity .
      FILTER(?relationship != rdfs:label)
      FILTER(?relationship != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
      OPTIONAL { ?related_entity rdfs:label ?related_label . }
    }

    OPTIONAL {
      ?report a stix:Report ;
              stix:mentions ?entity .
    }
  }
}
ORDER BY ?entity_type ?label ?relationship
```

### Expected Output and Current Runtime Result

Expected output includes attack pattern or malware entities, their RDF type, labels, relationships, related entities, and associated report URLs where available.

Example expected row shape:

| entity | entity_type | label | relationship | related_entity | report |
|---|---|---|---|---|---|
| `cskg:supplychainattack` | `stix:AttackPattern` | `Supply chain attack` | `stix:targets` | `cskg:packagist` | Packagist supply-chain report URI |

Runtime validation on 2026-05-26 returned 161 rows from the named graph, covering 67 attack pattern entities, 17 malware entities, and 78 rows with relationship context. Full evidence is stored in `docs/evidence/usecase_runtime_outputs.md`.

### Current Limitation

Some related entities are currently untyped or do not have `rdfs:label`, so Use Case 3 may show related URI values without readable labels. Repeated entities are expected when the same attack pattern or malware appears in multiple source reports.

### Real-World Benefit

This supports incident triage and threat hunting. Analysts can start from a malware or attack pattern and see what reports mention it, what it targets, and what related indicators or concepts were extracted.
