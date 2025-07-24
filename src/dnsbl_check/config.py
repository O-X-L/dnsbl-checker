from os import environ

DEBUG = 'DEV' in environ
RAW_PROVIDERS_IP = [
    'all.s5h.net',
    'b.barracudacentral.org',
    'bl.nordspam.com',
    'blacklist.woody.ch',
    'zen.spamhaus.org',
    'xbl.spamhaus.org',
    'combined.abuse.ch',
    'combined.rbl.msrbl.net',
    'db.wpbl.info',
    'dnsbl.cyberlogic.net',
    'drone.abuse.ch',
    'images.rbl.msrbl.net',
    'ips.backscatterer.org',
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
    'spam.rbl.msrbl.net',
    'spambot.bls.digibase.ca',
    # 'spamlist.or.kr',
    'spamrbl.imp.ch',
    'spamsources.fabel.dk',
    'ubl.lashback.com',
    'virbl.bit.nl',
    'virus.rbl.msrbl.net',
    'virus.rbl.jp',
    'wormrbl.imp.ch',
    'z.mailspike.net',
    'spam.spamrats.com',
    'dyna.spamrats.com',
    'noptr.spamrats.com',
    'bl.spamcop.net',
    'bl.blocklist.de',
    'rbl.your-server.de',
    'bl.0spam.org',
    'rbl.0spam.org',
    'dnsbl.abusix.net',
    'spam.dnsbl.anonmails.de',
    'dnsbl.calivent.com.pe',
    'tor.dan.me.uk',
    'dnsbl.dronebl.org',
    'hostkarma.junkemailfilter.com',
    'orvedb.aupads.org',
    'dnsbl-1.uceprotect.net',
    'dnsbl-2.uceprotect.net',
    'dnsbl-3.uceprotect.net',
    'duinv.aupads.org',
    'spam.abuse.ch',
    'ubl.unsubscore.com',
    'rbl2.triumf.ca',
    'dnsrbl.swinog.ch',
    'dnsbl.spfbl.net',
    'dbl.spamhaus.org',
]
RAW_PROVIDERS_DOMAIN = [
    'uribl.spameatingmonkey.net',
    'multi.surbl.org',
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
