RAW_BASE_PROVIDERS = [
    'all.s5h.net',
    'aspews.ext.sorbs.net',
    'b.barracudacentral.org',
    'bl.nordspam.com',
    'blackholes.five-ten-sg.com',
    'blacklist.woody.ch',
    # The provider zen.spamhaus.org is already being used. abuseat.org redirects to spamhaus.org
    # Additionally, abuseat.org has the same behaviour as zen.spamhaus.org
    # and we manage the new DNSBL_CATEGORY_ERROR in the zen.spamhaus.org Provider class
    # 'cbl.abuseat.org',
    'combined.abuse.ch',
    'combined.rbl.msrbl.net',
    'db.wpbl.info',
    'dnsbl.cyberlogic.net',
    'dnsbl.sorbs.net',
    'drone.abuse.ch',
    'images.rbl.msrbl.net',
    'ips.backscatterer.org',
    'ix.dnsbl.manitu.net',
    'korea.services.net',
    'matrix.spfbl.net',
    'phishing.rbl.msrbl.net',
    'proxy.bl.gweep.ca',
    'proxy.block.transip.nl',
    'psbl.surriel.com',
    'rbl.interserver.net',
    'relays.bl.gweep.ca',
    'relays.bl.kundenserver.de',
    'relays.nether.net',
    'residential.block.transip.nl',
    'singular.ttk.pte.hu',
    'spam.dnsbl.sorbs.net',
    'spam.rbl.msrbl.net',
    'spambot.bls.digibase.ca',
    'spamlist.or.kr',
    'spamrbl.imp.ch',
    'spamsources.fabel.dk',
    'ubl.lashback.com',
    'virbl.bit.nl',
    'virus.rbl.msrbl.net',
    'virus.rbl.jp',
    'wormrbl.imp.ch',
    'z.mailspike.net',
]
RAW_DOMAIN_PROVIDERS = [
    'uribl.spameatingmonkey.net',
    'multi.surbl.org',
    'rhsbl.sorbs.net '
]
DNSBL_CATEGORY_UNKNOWN = 'unknown'
DNSBL_CATEGORY_SPAM = 'spam'
DNSBL_CATEGORY_EXPLOITS = 'exploits'
DNSBL_CATEGORY_PHISH = 'phish'
DNSBL_CATEGORY_MALWARE = 'malware'
DNSBL_CATEGORY_CNC = 'cnc'
DNSBL_CATEGORY_ABUSED = 'abused'
DNSBL_CATEGORY_LEGIT = 'legit'
DNSBL_CATEGORY_ERROR = 'error'
DEFAULT_TIMEOUT = 5
