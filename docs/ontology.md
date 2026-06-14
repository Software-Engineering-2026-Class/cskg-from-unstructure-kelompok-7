# Ontology Documentation — CSKG from Unstructured Data

**Issue:** #03 Develop or adopt ontology for unstructured sources  
**PIC:** Kesya  
**Status:** Closed  

---

## 1. Overview

The CSKG pipeline extracts cybersecurity entities and relations from unstructured sources (RSS feeds, articles, reports) and maps them into a formal knowledge graph. To ensure interoperability with existing threat intelligence tools and the SEPSES CSKG, this project adopts **STIX 2.1** as the primary ontology, extended with a custom CSKG namespace for project-specific entities and a direct URI link to the SEPSES CVE Knowledge Graph for vulnerability entities.

This document describes:
- The ontology namespaces in use
- Entity classes (types of things in the graph)
- Predicates (types of relationships)
- How each source maps to the ontology

---

## 2. Namespaces

| Prefix | URI | Purpose |
|--------|-----|---------|
| `stix` | `http://docs.oasis-open.org/cti/ns/stix#` | Primary ontology — STIX 2.1 entity types and relation predicates |
| `cskg` | `http://group2.org/cskg/` | Custom project namespace for extracted entity instances |
| `sepses` | `https://w3id.org/sepses/resource/cve/` | External CVE entity URIs from the SEPSES CSKG |
| `rdfs` | `http://www.w3.org/2000/01/rdf-schema#` | Labels and class hierarchy |
| `owl` | `http://www.w3.org/2002/07/owl#` | Entity alignment (`owl:sameAs`) |
| `dcterms` | `http://purl.org/dc/terms/` | Metadata properties (e.g., `dcterms:created`) |

### Why STIX 2.1?

STIX (Structured Threat Information Expression) is the de facto industry standard for representing cybersecurity threat intelligence. By using STIX as the backbone ontology:
- The CSKG is immediately compatible with existing TI tools (MISP, OpenCTI, TAXII servers).
- Entity types are well-defined and widely understood.
- Relations have established semantics that match the language used in cybersecurity reports.

---

## 3. Entity Classes

The following entity types are extracted from unstructured sources and typed according to STIX 2.1 classes.

### 3.1 `stix:Report`

Represents the source article or report from which entities were extracted. The URI of a `Report` is the original article URL.

```turtle
<https://www.bleepingcomputer.com/news/security/example-article/>
    a stix:Report ;
    stix:mentions cskg:dragonforce ,
                  cskg:cve-2025-1234 .
```

**Extracted from:** all RSS sources (TheHackerNews, BleepingComputer, KrebsOnSecurity, FortiGuardLabs, and any additional sources).

---

### 3.2 `stix:ThreatActor`

Represents an individual, group, or organization believed to be responsible for malicious cyber activity.

```turtle
cskg:dragonforce
    a stix:ThreatActor ;
    rdfs:label "DragonForce" ;
    stix:uses cskg:socialengineering .
```

**Typical mentions in source text:** "APT group", "ransomware gang", "threat actor", "nation-state actor", hacker group names.

---

### 3.3 `stix:Malware`

Represents malicious code, including ransomware, trojans, backdoors, spyware, and botnets.

```turtle
cskg:lockbit
    a stix:Malware ;
    rdfs:label "LockBit" ;
    stix:variant_of cskg:lockbit3 .
```

**Typical mentions:** malware family names, ransomware names, tool names used in attacks.

---

### 3.4 `stix:Vulnerability`

Represents a weakness in software or hardware that can be exploited. When the extracted text contains a CVE ID, the entity URI is linked directly to the SEPSES CVE Knowledge Graph instead of a local CSKG URI (see Section 5).

```turtle
<https://w3id.org/sepses/resource/cve/CVE-2025-12480>
    a stix:Vulnerability .
```

**Typical mentions:** CVE IDs (`CVE-YYYY-NNNNN`), named vulnerability disclosures.

---

### 3.5 `stix:Indicator`

Represents an observable pattern that indicates a potential compromise — IP addresses, domains, file hashes, URLs used as indicators of compromise (IOC).

```turtle
cskg:ioc-192-168-1-1
    a stix:Indicator ;
    rdfs:label "192.168.1.1" .
```

**Typical mentions:** IP addresses, domain names, SHA256 hashes, malicious URLs extracted from incident reports.

---

### 3.6 `stix:AttackPattern`

Represents a technique or method used by threat actors to compromise systems, typically mapped to MITRE ATT&CK techniques.

```turtle
cskg:socialengineering
    a stix:AttackPattern ;
    rdfs:label "social engineering" .
```

**Typical mentions:** "phishing", "spear phishing", "credential dumping", "lateral movement", MITRE ATT&CK technique names.

---

## 4. Predicates (Relationship Types)

The following predicates are used to express relationships between entities. All predicates are drawn from the STIX 2.1 namespace (`stix:`), with the exception of `dcterms:created` and `rdfs:label`.

| Predicate | Domain | Range | Meaning |
|-----------|--------|-------|---------|
| `stix:mentions` | Report | Any | The report mentions this entity |
| `stix:uses` | ThreatActor / Malware | Malware / AttackPattern / Indicator | Subject uses the object as a tool or technique |
| `stix:targets` | ThreatActor / Malware | ThreatActor / Organization / Sector | Subject targets the object |
| `stix:exploits` | ThreatActor / Malware | Vulnerability | Subject exploits the vulnerability |
| `stix:attributed_to` | Any | ThreatActor | Activity is attributed to this actor |
| `stix:variant_of` | Malware | Malware | This malware is a variant of another |
| `stix:located_in` | ThreatActor | Location | Actor is located in a geographic region |
| `stix:impersonates` | ThreatActor | Any | Actor impersonates this entity |
| `stix:reports` | Any | Any | Subject reports on or discloses the object |
| `stix:patched` | Any | Vulnerability | The vulnerability has been patched |
| `stix:resolved` | Any | Vulnerability | The vulnerability has been resolved |
| `stix:disrupted` | Any | Any | Subject disrupted the object's operation |
| `stix:aligned_with` | Any | Any | Subject is aligned with or associated to the object |
| `stix:observes` | Any | Any | Subject has observed the object |
| `stix:has_similarities_with` | Any | Any | Subject has similarities to the object |
| `stix:propagated_via` | Malware / ThreatActor | Any | Propagation mechanism or vector |
| `rdfs:label` | Any | Literal | Human-readable name of the entity |
| `dcterms:created` | Report | xsd:dateTime | Publication timestamp of the source article |
| `owl:sameAs` | cskg entity | cskg canonical URI | Links labeled URI to normalized canonical URI |

---

## 5. Dual-URI Entity Resolution

To handle variations in threat actor naming (e.g., `"APT-29"` vs `"APT 29"` vs `"apt29"`), the pipeline creates two linked nodes for **`stix:ThreatActor`** entities specifically:

- **Canonical URI** (`safe_uri`): normalized, lowercase, alphanumeric only (e.g., `cskg:apt29`). Used for all relationships and the `stix:mentions` link from the Report.
- **Labeled URI** (`unsafe_uri`): preserves the original extracted text as `rdfs:label` (e.g., `cskg:APT_29`). Linked to the canonical URI via `owl:sameAs`.

```turtle
# Canonical URI — used in all relations and stix:mentions
cskg:apt29
    a stix:ThreatActor .

# Labeled URI — preserves original text from article
cskg:APT_29
    a stix:ThreatActor ;
    rdfs:label "APT-29" ;
    owl:sameAs cskg:apt29 .
```

This pattern ensures that SPARQL queries on the canonical URI (`cskg:apt29`) will match all mentions regardless of how the name appeared in the original article.

For all other entity types (`stix:Malware`, `stix:Vulnerability`, `stix:Indicator`, `stix:AttackPattern`), only the canonical `safe_uri` is created, with `rdfs:label` attached directly to it:

```turtle
# Malware — single canonical URI with label
cskg:lockbit
    a stix:Malware ;
    rdfs:label "LockBit" .
```

---

## 6. SEPSES CVE Linking

When the LLM extractor identifies a vulnerability entity that matches a CVE ID pattern (`CVE-YYYY-NNNNN`), the pipeline skips creating a local CSKG node and instead uses the corresponding URI from the **SEPSES CVE Knowledge Graph** directly.

```python
# From pipeline/build_kg.py
cve_match = re.search(r"(CVE-\d{4}-\d{4,})", vuln, re.IGNORECASE)
if cve_match:
    cve_id = cve_match.group(1).upper()
    vuln_uri = URIRef(f"https://w3id.org/sepses/resource/cve/{cve_id}")
```

This linking enables federated queries that combine CSKG data with the rich structured CVE data (CVSS scores, affected products, CWE classifications) stored in SEPSES.

**Example — a ThreatActor exploiting a SEPSES-linked CVE:**

```turtle
cskg:konni
    a stix:ThreatActor ;
    rdfs:label "Konni" ;
    stix:exploits <https://w3id.org/sepses/resource/cve/CVE-2025-12480> .

<https://w3id.org/sepses/resource/cve/CVE-2025-12480>
    a stix:Vulnerability .
```

**Current status:** CVE URI linking is implemented and verified (22 SEPSES CVE URIs confirmed in final runtime statistics). Linking for CWE IDs and MITRE ATT&CK technique URIs is planned for future iterations.

---

## 7. Source-to-Ontology Mapping

Each RSS source contributes different types of entities based on the nature of its content.

| Source | Primary Entity Types | Notes |
|--------|---------------------|-------|
| TheHackerNews | ThreatActor, Malware, Vulnerability | General threat news; broad coverage |
| BleepingComputer | Malware, Vulnerability, Indicator | Detailed incident reports; high IOC density |
| KrebsOnSecurity | ThreatActor, Indicator | Investigative reporting; strong actor attribution |
| FortiGuardLabs | Malware, Vulnerability, AttackPattern | Vendor threat intelligence; outbreak alerts |
| *(CISA Advisories — planned)* | Vulnerability, AttackPattern | Official US-CERT advisories; high CVE density |
| *(NVD — planned)* | Vulnerability | Structured CVE feed; links directly to SEPSES |

---

## 8. Limitations and Known Gaps

| Gap | Description |
|-----|-------------|
| No formal OWL axioms | `stix:ThreatActor`, `stix:Malware`, etc. are used as classes but no `SubClassOf`, `Domain`, or `Range` axioms are declared. This is a known simplification. |
| Predicates not formally declared | STIX predicates (e.g., `stix:uses`, `stix:targets`) are applied as-is from the STIX namespace but are not formally defined as `owl:ObjectProperty` in the graph. |
| ThreatActor coverage | Runtime verification shows `stix:ThreatActor` count = 0 in initial run. This is due to Gemini LLM extraction variability, not an ontology issue. |
| SEPSES linking scope | Currently limited to CVE IDs. CWE and MITRE ATT&CK URI alignment is not yet implemented. |
| No temporal reasoning | `dcterms:created` is captured but no temporal inference or ordering is applied. |

---

## 9. Example: Full Article Graph

The following illustrates how a single BleepingComputer article about DragonForce ransomware is represented in the CSKG using this ontology:

```turtle
@prefix stix: <http://docs.oasis-open.org/cti/ns/stix#> .
@prefix cskg: <http://group2.org/cskg/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

# Source report
<https://www.bleepingcomputer.com/news/security/dragonforce-example/>
    a stix:Report ;
    dcterms:created "2025-12-03T10:05:15Z"^^<http://www.w3.org/2001/XMLSchema#dateTime> ;
    stix:mentions cskg:dragonforce ,
                  cskg:scatteredspider ,
                  cskg:socialengineering ,
                  cskg:initialaccess .

# Canonical entity URIs
cskg:dragonforce     a stix:ThreatActor .
cskg:scatteredspider a stix:ThreatActor .
cskg:socialengineering a stix:AttackPattern .
cskg:initialaccess   a stix:AttackPattern .

# Labeled entity URIs (dual-URI pattern)
cskg:DragonForce
    a stix:ThreatActor ;
    rdfs:label "DragonForce" ;
    owl:sameAs cskg:dragonforce .

cskg:ScatteredSpider
    a stix:ThreatActor ;
    rdfs:label "Scattered Spider" ;
    owl:sameAs cskg:scatteredspider ;
    stix:uses cskg:socialengineering ,
              cskg:initialaccess .
```

---

*Document generated for CSKG Kelompok 7 — Metode RPL, Issue #03.*
