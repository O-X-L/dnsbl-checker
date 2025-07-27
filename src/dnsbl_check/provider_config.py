# pylint: disable=W0401,W0614
from config import *
from provider import ProviderDomain, ProviderIP, ProviderIP4, ProviderIP6

# NOTE: query-support of many providers is listed here: https://multirbl.valli.org/list/

# HOW-TO:
#   Add a class for the provider that should have a custom config => naming 'Provider<Name><BL-Type>'
#   MUST: set the HOST to the provider-dns
#   If required => add RESPONSE_CATEGORIES; the values can be either a single category or a set {CAT1, CAT2} of categories
#   MUST: add the provider to the CUSTOM_PROVIDERS-mapping at the bottom!

class ProviderZenSpamhaus(ProviderIP):
    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_SPAM,
        '127.0.0.3': DNSBL_CATEGORY_SPAM,
        '127.0.0.9': DNSBL_CATEGORY_SPAM,
        '127.0.0.4': DNSBL_CATEGORY_EXPLOITS,
        '127.0.0.5': DNSBL_CATEGORY_EXPLOITS,
        '127.0.0.6': DNSBL_CATEGORY_EXPLOITS,
        '127.0.0.7': DNSBL_CATEGORY_EXPLOITS,
        '127.255.255.252': DNSBL_CATEGORY_ERROR,
        '127.255.255.254': DNSBL_CATEGORY_ERROR,
        '127.255.255.255': DNSBL_CATEGORY_ERROR,
    }
    HOST = 'zen.spamhaus.org'


class ProviderDblSpamhaus(ProviderDomain):
    RESPONSE_CATEGORIES = {
        '127.0.1.2': DNSBL_CATEGORY_SPAM,
        '127.0.1.4': DNSBL_CATEGORY_PHISH,
        '127.0.1.5': DNSBL_CATEGORY_MALWARE,
        '127.0.1.6': DNSBL_CATEGORY_CNC,
        '127.0.1.102': {DNSBL_CATEGORY_ABUSED, DNSBL_CATEGORY_LEGIT, DNSBL_CATEGORY_SPAM},
        '127.0.1.103': {DNSBL_CATEGORY_ABUSED, DNSBL_CATEGORY_SPAM},
        '127.0.1.104': {DNSBL_CATEGORY_ABUSED, DNSBL_CATEGORY_LEGIT, DNSBL_CATEGORY_PHISH},
        '127.0.1.105': {DNSBL_CATEGORY_ABUSED, DNSBL_CATEGORY_LEGIT, DNSBL_CATEGORY_MALWARE},
        '127.0.1.106': {DNSBL_CATEGORY_ABUSED,  DNSBL_CATEGORY_LEGIT, DNSBL_CATEGORY_CNC},
        '127.255.255.252': DNSBL_CATEGORY_ERROR,
        '127.255.255.254': DNSBL_CATEGORY_ERROR,
        '127.255.255.255': DNSBL_CATEGORY_ERROR,
    }
    HOST = 'dbl.spamhaus.org'


class ProviderOXLRisk(ProviderIP):
    # https://github.com/O-X-L/risk-db

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_ABUSED,
        '127.0.0.3': DNSBL_CATEGORY_SCANNER,
        '127.0.0.4': DNSBL_CATEGORY_BOT,
        '127.0.0.5': DNSBL_CATEGORY_ATTACK,
        '127.0.0.6': DNSBL_CATEGORY_SPAM,
    }
    HOST = 'ip.dnsbl.risk.oxl.app'


class ProviderZenrblIP4(ProviderIP4):
    HOST = 'ip4.bl.zenrbl.pl'


class ProviderBlockedserversScan(ProviderIP):
    HOST = 'netscan.rbl.blockedservers.com'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_SCANNER,
    }


class ProviderBlockedserversSpam(ProviderIP):
    HOST = 'spam.rbl.blockedservers.com'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_SPAM,
    }


class ProviderSpameatingmonkeyIP4(ProviderIP4):
    HOST = 'bl.spameatingmonkey.net'


class ProviderSpameatingmonkeyIP6(ProviderIP6):
    HOST = 'bl.ipv6.spameatingmonkey.net'


class ProviderSpameatingmonkeyBackscatter(ProviderIP4):
    HOST = 'backscatter.spameatingmonkey.net'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_BACKSCATTER,
    }


class ProviderSpameatingmonkeyNet4(ProviderIP4):
    HOST = 'netbl.spameatingmonkey.net'


class ProviderAbuseCHSpam(ProviderIP4):
    HOST = 'spam.abuse.ch'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_SPAM,
    }


class ProviderTorDanMe(ProviderIP):
    HOST = 'tor.dan.me.uk'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_PROXY,
    }


class ProviderFmbLaFresh(ProviderDomain):
    HOST = 'fresh.fmb.la'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_FRESH,
    }


class ProviderFmbLaShort(ProviderDomain):
    HOST = 'short.fmb.la'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_FRESH,
    }


class ProviderSpameatingmokeyFresh(ProviderDomain):
    HOST = 'fresh.spameatingmonkey.net'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_FRESH,
    }


class ProviderSpameatingmokeyFreshZero(ProviderDomain):
    HOST = 'freshzero.spameatingmonkey.net'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_FRESH,
    }


class ProviderSpameatingmokeyFresh10(ProviderDomain):
    HOST = 'fresh10.spameatingmonkey.net'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_FRESH,
    }


class ProviderSpameatingmokeyFresh15(ProviderDomain):
    HOST = 'fresh15.spameatingmonkey.net'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_FRESH,
    }


class ProviderSpameatingmokeyFresh30(ProviderDomain):
    HOST = 'fresh30.spameatingmonkey.net'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_FRESH,
    }


class ProviderBackscatterer(ProviderIP4):
    HOST = 'ips.backscatterer.org'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_BACKSCATTER,
    }


class ProviderSpfblAbuse(ProviderIP):
    HOST = 'abuse.spfbl.net'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_ABUSED,
    }


class ProviderDigibaseOpenproxy(ProviderIP4):
    HOST = 'openproxy.bls.digibase.ca'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_PROXY,
    }


class ProviderDigibaseProxyabuse(ProviderIP4):
    HOST = 'proxyabuse.bls.digibase.ca'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': {DNSBL_CATEGORY_PROXY, DNSBL_CATEGORY_ABUSED},
    }


class ProviderDigibaseSpambot(ProviderIP4):
    HOST = 'spambot.bls.digibase.ca'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_SPAM,
    }


class ProviderSwingogSpamrbl(ProviderIP):
    HOST = 'spamrbl.swinog.ch'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_SPAM,
    }


class ProviderFabelSpamsources(ProviderIP):
    HOST = 'spamsources.fabel.dk'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_SPAM,
    }


class ProviderSpamratsSpam(ProviderIP4):
    HOST = 'spam.spamrats.com'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_SPAM,
    }


class ProviderSpamratsDyna(ProviderIP4):
    HOST = 'dyna.spamrats.com'


class ProviderSpamratsNoptr(ProviderIP4):
    HOST = 'noptr.spamrats.com'


class ProviderSpamratsAuth(ProviderIP4):
    HOST = 'auth.spamrats.com'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_ABUSED,
    }


class ProviderSpamcop(ProviderIP4):
    HOST = 'bl.spamcop.net'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_SPAM,
    }


class ProviderSpam0Bl(ProviderIP4):
    HOST = 'bl.0spam.org'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_SPAM,
    }


class ProviderSpam0Rbl(ProviderIP4):
    HOST = 'rbl.0spam.org'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_SPAM,
    }


class ProviderSpam0Net4(ProviderIP4):
    HOST = 'nbl.0spam.org'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_SPAM,
    }


class ProviderAnonmailsSpam(ProviderIP4):
    HOST = 'spam.dnsbl.anonmails.de'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_SPAM,
    }


class ProviderJustspam(ProviderIP4):
    HOST = 'dnsbl.justspam.org'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_SPAM,
    }


class ProviderPolspamRbl(ProviderIP4):
    HOST = 'rbl.polspam.pl'

    RESPONSE_CATEGORIES = {
        '127.0.0.2': DNSBL_CATEGORY_SPAM,
    }


CUSTOM_PROVIDERS = {
    ProviderZenSpamhaus.HOST: ProviderZenSpamhaus,
    ProviderDblSpamhaus.HOST: ProviderDblSpamhaus,
    ProviderOXLRisk.HOST: ProviderOXLRisk,
    ProviderZenrblIP4.HOST: ProviderZenrblIP4,
    ProviderBlockedserversSpam.HOST: ProviderBlockedserversSpam,
    ProviderSpameatingmonkeyIP4.HOST: ProviderSpameatingmonkeyIP4,
    ProviderSpameatingmonkeyIP6.HOST: ProviderSpameatingmonkeyIP6,
    ProviderSpameatingmonkeyBackscatter.HOST: ProviderSpameatingmonkeyBackscatter,
    ProviderSpameatingmonkeyNet4.HOST: ProviderSpameatingmonkeyNet4,
    ProviderAbuseCHSpam.HOST: ProviderAbuseCHSpam,
    ProviderTorDanMe.HOST: ProviderTorDanMe,
    ProviderFmbLaFresh.HOST: ProviderFmbLaFresh,
    ProviderFmbLaShort.HOST: ProviderFmbLaShort,
    ProviderSpameatingmokeyFresh.HOST: ProviderSpameatingmokeyFresh,
    ProviderSpameatingmokeyFreshZero.HOST: ProviderSpameatingmokeyFreshZero,
    ProviderSpameatingmokeyFresh10.HOST: ProviderSpameatingmokeyFresh10,
    ProviderSpameatingmokeyFresh15.HOST: ProviderSpameatingmokeyFresh15,
    ProviderSpameatingmokeyFresh30.HOST: ProviderSpameatingmokeyFresh30,
    ProviderBackscatterer.HOST: ProviderBackscatterer,
    ProviderSpfblAbuse.HOST: ProviderSpfblAbuse,
    ProviderDigibaseOpenproxy.HOST: ProviderDigibaseOpenproxy,
    ProviderDigibaseProxyabuse.HOST: ProviderDigibaseProxyabuse,
    ProviderDigibaseSpambot.HOST: ProviderDigibaseSpambot,
    ProviderSwingogSpamrbl.HOST: ProviderSwingogSpamrbl,
    ProviderFabelSpamsources.HOST: ProviderFabelSpamsources,
    ProviderSpamratsSpam.HOST: ProviderSpamratsSpam,
    ProviderSpamratsDyna.HOST: ProviderSpamratsDyna,
    ProviderSpamratsNoptr.HOST: ProviderSpamratsNoptr,
    ProviderSpamratsAuth.HOST: ProviderSpamratsAuth,
    ProviderSpamcop.HOST: ProviderSpamcop,
    ProviderSpam0Bl.HOST: ProviderSpam0Bl,
    ProviderSpam0Rbl.HOST: ProviderSpam0Rbl,
    ProviderSpam0Net4.HOST: ProviderSpam0Net4,
    ProviderAnonmailsSpam.HOST: ProviderAnonmailsSpam,
    ProviderJustspam.HOST: ProviderJustspam,
    ProviderPolspamRbl.HOST: ProviderPolspamRbl,
}

BASE_PROVIDERS_IP = [
     ProviderIP(host) for host in RAW_PROVIDERS_IP if host not in CUSTOM_PROVIDERS
]
BASE_PROVIDERS_IP.extend([
     CUSTOM_PROVIDERS[host]() for host in RAW_PROVIDERS_IP if host in CUSTOM_PROVIDERS
])
BASE_PROVIDERS_DOMAIN = [
     ProviderDomain(host) for host in RAW_PROVIDERS_DOMAIN if host not in CUSTOM_PROVIDERS
]
BASE_PROVIDERS_DOMAIN.extend([
     CUSTOM_PROVIDERS[host]() for host in RAW_PROVIDERS_DOMAIN if host in CUSTOM_PROVIDERS
])
