### Current Pull Sources:

**Intel Source 1 — Feodo Tracker IP Blocklist (abuse.ch)**\
Goal / Purpose\
Pulls a curated, real-time JSON blocklist of IP addresses actively associated with Command & Control (C2) infrastructure used by banking trojans and botnet malware families tracked by abuse.ch's Feodo Tracker project.

Summary\
Feodo Tracker is a threat intelligence initiative by abuse.ch that monitors and exposes infrastructure used by malware families such as QakBot, Emotet, Dridex, TrickBot, and BazarLoader. The recommended IP blocklist endpoint delivers structured, machine-readable records of confirmed C2 servers — each enriched with metadata including the associated port, hosting ASN, country of origin, malware family, and activity timestamps (first_seen, last_online). Only IPs meeting abuse.ch's confidence threshold for active or recently active C2 activity are included in this recommended list, making it a high-fidelity, low-noise source.


**Intel Source 2 — Botvrij.eu IP Destination IOC List**\
Goal / Purpose\
Pulls a plain-text list of IP addresses identified as malicious network destination (ip-dst), compiled from open source threat reports, APT writeups, and exploit campaign documentation.

Summary\
Botvrij.eu is a community-driven OSINT project that uses MISP as its backend for storing and managing threat information. Data is ingested via ioc-parser from open source intelligence sources such as blog posts and PDF threat reports, then extracted using PyMISP and formatted through custom Python scripts. The ioclist.ip-dst feed specifically surfaces IP addresses that have been observed as destination points in malicious network traffic — covering C2 callbacks, malware delivery endpoints, and attack infrastructure. To maintain data quality, all entries older than approximately 6 months are automatically removed, keeping the feed relevant and reducing stale indicator noise. 


**Intel Source 3 — IPsum Daily Threat Feed**\
Goal / Purpose\
Pulls a daily-refreshed plain-text feed of malicious IP addresses, each scored by the number of independent blacklists they appear on — providing a built-in confidence signal directly within the feed data.

Summary\
IPsum is a threat intelligence feed that aggregates data from 30+ different publicly available lists of suspicious and/or malicious IP addresses. All lists are automatically retrieved and parsed on a daily basis and the final result is pushed to the repository. What makes this source distinct from the others is its occurrence scoring system; each IP is accompanied by a count of how many source lists flagged it. The higher the number, the lower the chance of a false positive detection. The list is also sorted from the most to least frequently occurring IP addresses. This makes IPsum effectively a meta-feed — an aggregation of aggregations — giving broader threat coverage than any single source alone.


**Intel Source 4 — REScure Malicious IP Blacklist**\
Goal / Purpose\
Pulls a plain-text blacklist of malicious IP addresses from REScure, an independent community-driven CTI project that correlates threat events in real-time to surface only confirmed offending infrastructure.

Summary\
REScure is an independent cyber threat intelligence initiative that maintains blacklists of malicious IPs and domains derived from real-time event correlation across a large internal dataset. Each node in the REScure dataset is an event with its own separate attributes, totalling around 2 million, which are correlated in real-time to ensure only offending, malicious entries are listed. Unlike feeds tied to specific malware families or APT campaigns, REScure's scope is broad, covering general malicious activity across multiple threat categories, which adds width to the pipeline's overall detection coverage.


### Normalization Template:

```python
def format_template(initial_data):
    intel = {}
    intel["type"] = ""
    intel["category"] = "threat_intelligence"
    intel["value"] = initial_data["value"]
    intel["description"] = initial_data["details"]
    intel["confidence"] = ""
    intel["first_seen"] = ""
    intel["last_seen"] = ""
    intel["active"] = ""
    intel["meta"] = initial_data
    return intel
```
