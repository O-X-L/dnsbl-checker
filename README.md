# DNSBL Checker

[![Lint](https://github.com/O-X-L/dnsbl-checker/actions/workflows/lint.yml/badge.svg?branch=latest)](https://github.com/O-X-L/dnsbl-checker/actions/workflows/lint.yml)
[![Test](https://github.com/O-X-L/dnsbl-checker/actions/workflows/test.yml/badge.svg?branch=latest)](https://github.com/O-X-L/dnsbl-checker/actions/workflows/test.yml)

This script/library can check if an IP or Domain is listed on DNS-BL's. 

Please be aware that the providers of such public DNSBL mirrors discourage high-volume lookups. Do not abuse their services! You will run into rate-limits.

**Features**:
* Asynchronous DNS requests
* Multi-provider support
* Ability to add custom providers
* Check for 50+ lists usually takes ~1 second
* Can also check domains

----

❤️ This started as a fork of [github.com/dmippolitov/pydnsbl](https://github.com/dmippolitov/pydnsbl) - so thanks to the contributors

❤️ Also thanks go to the maintainers of [multirbl.valli.org](https://multirbl.valli.org/list/) for collecting and sharing information about existing providers

If you are interested in [report-based reputation-systems => check out our Risk-DB project](https://github.com/O-X-L/risk-db).

Tip: If you want to run your own DNS-BL server - check out our [DNS-BL microservice](https://github.com/O-X-L/dnsbl-server).

----

## Scope

* This script/library should act as a **simple tool** to query DNS-BL's for the user

* **Response Validation**

  Interpreting if the provider's response is 'valid' is **out-of-scope** for this tool. (*like checking for false-positives*)

  This heavily depends on the user's context.

  Thus, the user should make sure to only use DNS-BL providers that are useful/safe for them to use.

  We have added some info about providers here: [Providers.md](https://github.com/O-X-L/dnsbl-checker/blob/latest/Providers.md)

* Users that want to use DNS-BL lookups in commercial settings have to make sure to **read the usage policies of those providers**.

  Some providers do not allow commercial usage in their free-tier.

If you want us to add additional providers or have found that existing ones have quit - [open an Issue](https://github.com/O-X-L/dnsbl-checker/issues) or [contact us per e-mail](mailto://contact+dnsblcheck@oxl.at)

----

## Installation

`pip install dnsbl-check`

See: [pypi.org](https://pypi.org/project/dnsbl-check/)

----

## Usage

**WARNING**:

> This script/library cannot impact if the result of a DNS-BL is a false-positive.
> 
> You will have to verify which providers provide 'valid' information for your use-cases and change the list of providers accordingly!

### Via CLI

```bash
dnsbl-check  --help
usage: DNS-BL Lookup-Client [-h] (-i IP | -d DOMAIN) [-j] [-s SKIP_PROVIDERS]
                            [-a ADD_PROVIDERS] [-o ONLY_PROVIDERS] [--details]

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        IP to check
  -d DOMAIN, --domain DOMAIN
                        Domain to check
  -j JSON, --json JSON  Only output JSON
  -s SKIP_PROVIDERS, --skip-providers SKIP_PROVIDERS
                        Comma-separated list of base-providers to skip
  -a ADD_PROVIDERS, --add-providers ADD_PROVIDERS
                        Comma-separated list of additional DNS-BL provider-domains to query
  -o ONLY_PROVIDERS, --only-providers ONLY_PROVIDERS
                        Comma-separated list of DNS-BL provider-domains to query
                        (ignoring the built-in default providers)
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
>     "dnsbl-3.uceprotect.net",
>     "dnsbl.spfbl.net",
>     "rbl.blockedservers.com",
>     "bl.fmb.la",
>     "ip.dnsbl.risk.oxl.app",
>     "abuse.spfbl.net"
>   ],
>   "categories": [
>     "unknown",
>     "abused"
>   ],
>   "general_errors": [],
>   "count": {
>     "detected": 7,
>     "checked": 84,
>     "failed": 0
>   }
> }

# add or skip DNS-BL providers:
dnsbl-check --ip=134.209.173.54 --add-providers ip.dnsbl.risk.oxl.app,dnsbl.host-svc.com --skip-providers abuse.spfbl.net

# or just check one provider:
dnsbl-check --ip=134.209.173.54 --only-providers ip.dnsbl.risk.oxl.app,dnsbl.host-svc.com
```

----

### Programmatically

```python3
# IPs
from dnsbl_check import CheckIP
with CheckIP() as checker:
    result = checker.check('134.209.173.54')

print(result)
# <DNSBLResult: 134.209.173.54 [DETECTED] (7/84)>
print(result.to_dict())
# {'request': '134.209.173.54', 'detected': True, 'detected_by': ['all.s5h.net', 'dnsbl-3.uceprotect.net', 'dnsbl.spfbl.net', 'rbl.blockedservers.com', 'bl.fmb.la', 'ip.dnsbl.risk.oxl.app', 'abuse.spfbl.net'], 'categories': ['abused', 'unknown'], 'general_errors': [], 'count': {'detected': 7, 'checked': 84, 'failed': 0}, 'detected_provider_categories': {'all.s5h.net': ['unknown'], 'dnsbl-3.uceprotect.net': ['unknown'], 'dnsbl.spfbl.net': ['unknown'], 'rbl.blockedservers.com': ['unknown'], 'bl.fmb.la': ['unknown'], 'ip.dnsbl.risk.oxl.app': ['abused'], 'abuse.spfbl.net': ['unknown']}, 'checked_providers': ['all.s5h.net', 'b.barracudacentral.org', 'bl.nordspam.com', 'blacklist.woody.ch', 'xbl.spamhaus.org', 'combined.abuse.ch', 'drone.abuse.ch', 'korea.services.net', 'matrix.spfbl.net', 'proxy.bl.gweep.ca', 'proxy.block.transip.nl', 'psbl.surriel.com', 'rbl.interserver.net', 'relays.bl.gweep.ca', 'relays.bl.kundenserver.de', 'relays.nether.net', 'residential.block.transip.nl', 'singular.ttk.pte.hu', 'ubl.lashback.com', 'virus.rbl.jp', 'z.mailspike.net', 'bl.blocklist.de', 'rbl.your-server.de', 'dnsbl.abusix.net', 'dnsbl.calivent.com.pe', 'dnsbl.dronebl.org', 'hostkarma.junkemailfilter.com', 'black.junkemailfilter.com', 'orvedb.aupads.org', 'dnsbl-1.uceprotect.net', 'dnsbl-2.uceprotect.net', 'dnsbl-3.uceprotect.net', 'duinv.aupads.org', 'ubl.unsubscore.com', 'rbl2.triumf.ca', 'dnsrbl.swinog.ch', 'dnsbl.spfbl.net', 'krn.korumail.com', 'work.drbl.gremlin.ru', 'dnsblchile.org', 'block.ascams.com', 'dnsbl.ascams.com', 'mix.ascams.com', 'superblock.ascams.com', 'rbl.blockedservers.com', 'netscan.rbl.blockedservers.com', 'rbl.abuse.ro', 'pbl.abuse.ro', 'bl.fmb.la', 'rbl.fasthosts.co.uk', 'rbl.efnetrbl.org', 'sbl.nszones.com', 'bl.nszones.com', 'bl.suomispam.net', 'bad.virusfree.cz', 'bip.virusfree.cz', 'dnsbl.zapbl.net', 'ip.dnsbl.risk.oxl.app', 'zen.spamhaus.org', 'ips.backscatterer.org', 'abuse.spfbl.net', 'spambot.bls.digibase.ca', 'openproxy.bls.digibase.ca', 'proxyabuse.bls.digibase.ca', 'spamrbl.swinog.ch', 'spamsources.fabel.dk', 'spam.spamrats.com', 'dyna.spamrats.com', 'noptr.spamrats.com', 'auth.spamrats.com', 'bl.spamcop.net', 'bl.0spam.org', 'rbl.0spam.org', 'nbl.0spam.org', 'spam.dnsbl.anonmails.de', 'tor.dan.me.uk', 'spam.abuse.ch', 'backscatter.spameatingmonkey.net', 'bl.spameatingmonkey.net', 'netbl.spameatingmonkey.net', 'dnsbl.justspam.org', 'spam.rbl.blockedservers.com', 'rbl.polspam.pl', 'ip4.bl.zenrbl.pl'], 'failed_providers': []}
print(result.to_json())
# ... (to_dict but in pretty-json)

with CheckIP() as checker:
    result = checker.check('2a01:4f8:c010:97b4::1')

print(result)
# IPv6 support
# <DNSBLResult: 2a01:4f8:c010:97b4::1 [DETECTED] (2/65)>

# Domains
from dnsbl_check import CheckDomain
with CheckDomain() as checker:
    result = checker.check('malware.com')

print(result)
# <DNSBLResult: malware.com (0/24)>

# add or skip DNS-BL providers
from dnsbl_check.provider import Provider, BASE_PROVIDERS_IP
providers = BASE_PROVIDERS_IP + [Provider('dnsbl.risk.oxl.app')]
with CheckIP(providers=providers, skip_providers=['abuse.spfbl.net']) as checker:
    result = checker.check('134.209.173.54')

# add or skip DNS-BL providers
from dnsbl_check.provider import Provider, BASE_PROVIDERS_IP
providers = BASE_PROVIDERS_IP + [Provider('dnsbl.risk.oxl.app')]
with CheckIP(providers=providers, skip_providers=['abuse.spfbl.net']) as checker:
    result = checker.check('134.209.173.54')

print(result)
# <DNSBLResult: 134.209.173.54 [DETECTED] (3/44)>
```

----

## Contributing

Contributions are welcome (:

See: [Contribute](https://github.com/O-X-L/dnsbl-checker/blob/latest/Contribute.md)
