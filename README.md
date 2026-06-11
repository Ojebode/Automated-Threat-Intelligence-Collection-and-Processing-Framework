### Automated Threat Intelligence Collection and Processing Framework
##### Overview
Multi-source IP threat intelligence pipeline that normalizes and ships CTI feeds to Elasticsearch. Currently pulls from 4 sources:
- Feodo Tracker
- Botvrij
- IPsum
- REScure

Normalization Template:

def format_template(initial_data):\
    intel = {}\
    intel["type"] = "ip_address"\
    intel["category"] = "threat_intelligence"\
    intel["value"] = initial_data["value"]\
    intel["description"] = initial_data["details"]\
    intel["confidence"] = ""\
    intel["first_seen"] = ""\
    intel["last_seen"] = ""\
    intel["active"] = ""\
    intel["meta"] = initial_data\
    return intel
