# Data Sources Documentation

This document describes all data sources used in the CSKG pipeline.

These sources are selected to provide a balanced combination of cybersecurity news, threat intelligence research, and structured vulnerability data to support comprehensive entity and relationship extraction.

---

## 1. The Hacker News
- **RSS URL:** `http://feeds.feedburner.com/TheHackersNews`
- **Category:** News
- **Access Method:** RSS via `feedparser`
- **Information Type:** Cybersecurity news articles covering breaches, vulnerabilities, and malware campaigns
- **Reason Selected:** High publication frequency and broad cybersecurity coverage including CVEs, ransomware, and threat actors
- **Entities that can be extracted:** `Vulnerability`, `Malware`, `ThreatActor`, `AttackPattern`

---

## 2. BleepingComputer
- **RSS URL:** `https://www.bleepingcomputer.com/feed/`
- **Category:** News
- **Access Method:** RSS via `feedparser`
- **Information Type:** Technical security news, ransomware reports, and vulnerability disclosures
- **Reason Selected:** Detailed technical reporting with frequent CVE references and indicators of compromise (IOCs)
- **Entities that can be extracted:** `Vulnerability`, `Malware`, `Indicator (IP, Domain, Hash)`, `AttackPattern`

---

## 3. KrebsOnSecurity
- **RSS URL:** `https://krebsonsecurity.com/feed/`
- **Category:** News (Investigative)
- **Access Method:** RSS via `feedparser`
- **Information Type:** Investigative cybercrime reporting and breach analysis
- **Reason Selected:** Narrative-rich articles containing relationships between threat actors, organizations, and attack campaigns
- **Entities that can be extracted:** `ThreatActor`, `Campaign`, `Organization`, `Malware`

---

## 4. Securelist (Kaspersky)
- **RSS URL:** `https://securelist.com/feed/`
- **Category:** Threat Research
- **Access Method:** RSS via `feedparser`
- **Information Type:** APT reports, malware analysis, and threat intelligence research
- **Reason Selected:** Deep technical analysis with rich entities such as malware families, threat actors, and TTPs
- **Entities that can be extracted:** `ThreatActor`, `Malware`, `Campaign`, `AttackPattern`, `Indicator (IP, Domain, Hash)`

---

## 5. Check Point Research
- **RSS URL:** `https://research.checkpoint.com/category/threat-research/feed/`
- **Category:** Threat Research
- **Access Method:** RSS via `feedparser`
- **Information Type:** Malware reverse engineering, exploit analysis, and campaign tracking
- **Reason Selected:** High-quality technical writeups with CVE references, IOCs, and attack techniques
- **Entities that can be extracted:** `Vulnerability`, `Malware`, `Indicator (IP, Domain, Hash)`, `AttackPattern`

---

## 6. SANS Internet Storm Center (ISC)
- **RSS URL:** `https://isc.sans.edu/rssfeed_full.xml`
- **Category:** Threat Monitoring
- **Access Method:** RSS via `feedparser`
- **Information Type:** Daily threat diaries and real-time incident observations
- **Reason Selected:** Provides real-time threat intelligence including malicious IPs, domains, and emerging vulnerabilities
- **Entities that can be extracted:** `Indicator (IP, Domain, Hash)`, `Vulnerability`, `AttackPattern`

---

## 7. FortiGuard Labs
- **RSS URL:** `https://filestore.fortinet.com/fortiguard/rss/outbreakalert.xml`
- **Category:** Vendor Threat Intelligence
- **Access Method:** RSS via `feedparser`
- **Information Type:** Security alerts, outbreak reports, and threat intelligence updates from Fortinet
- **Reason Selected:** Provides vendor-based threat intelligence and complements other research sources
- **Entities that can be extracted:** `Malware`, `Vulnerability`, `ThreatActor`, `AttackPattern`

---

## 8. NVD — National Vulnerability Database (NIST)
- **API URL:** `https://services.nvd.nist.gov/rest/json/cves/2.0`
- **Category:** Structured Vulnerability Database
- **Access Method:** REST API via `requests`
- **Information Type:** Official CVE records with descriptions, CVSS scores, and CWE classifications
- **Reason Selected:** Serves as a ground truth source for enriching extracted entities with standardized vulnerability metadata
- **Entities that can be extracted:** `Vulnerability (CVE)`, `Severity (CVSS)`, `Weakness (CWE)`

---

## Notes

- RSS-based sources provide unstructured textual data for NLP-based entity and relationship extraction.
- NVD serves as a structured ground truth for enrichment and validation of vulnerability-related entities.
