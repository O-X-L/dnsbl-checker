# DNSBL Checker

[![Lint](https://github.com/O-X-L/dnsbl-checker/actions/workflows/lint.yml/badge.svg?branch=latest)](https://github.com/O-X-L/dnsbl-checker/actions/workflows/lint.yml)
[![Test](https://github.com/O-X-L/dnsbl-checker/actions/workflows/test.yml/badge.svg?branch=latest)](https://github.com/O-X-L/dnsbl-checker/actions/workflows/test.yml)

This script/library can check if an IP or Domain is listed on DNS-BL's. 

Please be aware that the providers of such public DNSBL mirrors discourage high-volume lookups. Do not abuse their services! You will run into rate-limits.

**Features**:
* Asynchronous DNS requests
* Multi-provider support
* Ability to add custom providers
* Check for 50+ lists usually takes a few seconds
* Can also check domains

This started as a fork of [github.com/dmippolitov/pydnsbl](https://github.com/dmippolitov/pydnsbl) - so thanks to the contributors ❤️

If you are interested in [report-based reputation-systems => check out our Risk-DB project](https://github.com/O-X-L/risk-db).

----

## Installation

`pip install dnsbl-check`

----

## Usage

### Via CLI

```bash
dnsbl-check  --help
usage: DNS-BL Lookup-Client [-h] (-i IP | -d DOMAIN) [-j JSON] [-s SKIP_PROVIDERS] [--details]

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        IP to check
  -d DOMAIN, --domain DOMAIN
                        Domain to check
  -j JSON, --json JSON  Only output JSON
  -s SKIP_PROVIDERS, --skip-providers SKIP_PROVIDERS
                        Comma-separated list of base-providers to skip
  --details             If the result details should be added to the output
```

**Example:**

```bash
dnsbl-check --ip 134.209.173.54
> Checking IP 134.209.173.54 ..
> {
>   "detected": true,
>   "detected_by": [
>     "all.s5h.net",
>     "dnsbl-3.uceprotect.net"
>   ],
>   "categories": [
>     "unknown"
>   ],
>   "general_errors": [],
>   "count": {
>     "detected": 2,
>     "checked": 43,
>     "failed": 2
>   }
> }
```

----

### Programmatically

```python3
# IPs
from dnsbl_check import CheckIP
with CheckIP() as checker:
    result = checker.check('134.209.173.54')

print(result)
# <DNSBLResult: 134.209.173.54 [DETECTED] (2/43)>
print(result.to_dict())
# {'request': '134.209.173.54', 'detected': True, 'detected_by': ['all.s5h.net', 'dnsbl-3.uceprotect.net'], 'categories': ['unknown'], 'general_errors': [], 'count': {'detected': 2, 'checked': 43, 'failed': 2}, 'detected_provider_categories': {'all.s5h.net': ['unknown'], 'dnsbl-3.uceprotect.net': ['unknown']}, 'checked_providers': ['all.s5h.net', 'aspews.ext.sorbs.net', 'b.barracudacentral.org', 'bl.nordspam.com', 'blacklist.woody.ch', 'bogons.cymru.com', 'combined.abuse.ch', 'combined.rbl.msrbl.net', 'db.wpbl.info', 'dnsbl-2.uceprotect.net', 'dnsbl-3.uceprotect.net', 'dnsbl.cyberlogic.net', 'dnsbl.sorbs.net', 'drone.abuse.ch', 'images.rbl.msrbl.net', 'ips.backscatterer.org', 'korea.services.net', 'matrix.spfbl.net', 'phishing.rbl.msrbl.net', 'proxy.bl.gweep.ca', 'proxy.block.transip.nl', 'psbl.surriel.com', 'rbl.interserver.net', 'relays.bl.gweep.ca', 'relays.bl.kundenserver.de', 'relays.nether.net', 'residential.block.transip.nl', 'singular.ttk.pte.hu', 'spam.dnsbl.sorbs.net', 'spam.rbl.msrbl.net', 'spambot.bls.digibase.ca', 'spamlist.or.kr', 'spamrbl.imp.ch', 'spamsources.fabel.dk', 'ubl.lashback.com', 'virbl.bit.nl', 'virus.rbl.msrbl.net', 'virus.rbl.jp', 'wormrbl.imp.ch', 'z.mailspike.net', 'zen.spamhaus.org'], 'failed_providers': ['ix.dnsbl.manitu.net', 'spamlist.or.kr']}
print(result.to_json())
# ... (to_dict but in pretty json)

# Domains
from dnsbl_check import CheckDomain
with CheckDomain() as checker:
    result = checker.check('maleware.com')

print(result)
# <DNSBLResult: maleware.com (0/2)>
```

#### Adding custom providers

```python3
from dnsbl_check import CheckIP
from dnsbl_check.providers import BASE_PROVIDERS, Provider
p = BASE_PROVIDERS + [Provider('dnsbl.oxl.app')]
with CheckIP(providers=p) as checker:
    result = checker.check('134.209.173.54')
 
print(result)
# <DNSBLResult: 134.209.173.54 [DETECTED] (3/44)>
```

----

## Contributing

Contributions are welcome (:

See: [Contribute](https://github.com/O-X-L/dnsbl-checker/blob/latest/Contribute.md)
