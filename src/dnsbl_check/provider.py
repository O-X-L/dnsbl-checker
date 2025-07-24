# pylint: disable=W0401,W0614
from config import *


class Provider:
    def __init__(self, host: str):
        self.host = host

    def process_response(self, response):
        """
        Usually DNSBL lists returns ip-codes like this: 127.0.0.2
        Some of the lists provides some specification about
        this codes and their meaning. This function will be helpful to build mapping
        between response codes and DNSBL_CATEGORIES.  It is used in construction
        of DNSBLResult. You should redefine this function
        in your custom providers according to their specification.

        Parmeters:
            result - list of c-ares dns responses

        Returns:
            set of categories (DNSBL_CATEGORIES subset)

        """
        result = set()
        if response:
            result.add(DNSBL_CATEGORY_UNKNOWN)

        return result

    def __repr__(self):
        return f"<Provider: {self.host}>"


class ZenSpamhaus(Provider):
    """ Combined spamhaus list:
        https://www.spamhaus.org/faq/section/DNSBL%20Usage#200
    """

    def __init__(self):
        Provider.__init__(self, host='zen.spamhaus.org')

    def process_response(self, response):
        categories = set()
        for result in response:
            if result.host in ['127.0.0.2', '127.0.0.3', '127.0.0.9']:
                categories.add(DNSBL_CATEGORY_SPAM)

            elif result.host in ['127.0.0.4', '127.0.0.5', '127.0.0.6', '127.0.0.7']:
                categories.add(DNSBL_CATEGORY_EXPLOITS)

            elif result.host in ['127.255.255.252', '127.255.255.254', '127.255.255.255']:
                categories.add(DNSBL_CATEGORY_ERROR)

            else:
                categories.add(DNSBL_CATEGORY_UNKNOWN)

        return categories


class DblSpamhaus(Provider):
    """ Spamhaus domain blacklist
        https://www.spamhaus.org/faq/section/Spamhaus%20DBL#291
    """
    CATEGORY_MAPPING = {
        '127.0.1.2': {DNSBL_CATEGORY_SPAM},
        '127.0.1.4': {DNSBL_CATEGORY_PHISH},
        '127.0.1.5': {DNSBL_CATEGORY_MALWARE},
        '127.0.1.6': {DNSBL_CATEGORY_CNC},
        '127.0.1.102': {DNSBL_CATEGORY_ABUSED, DNSBL_CATEGORY_LEGIT, DNSBL_CATEGORY_SPAM},
        '127.0.1.103': {DNSBL_CATEGORY_ABUSED, DNSBL_CATEGORY_SPAM},
        '127.0.1.104': {DNSBL_CATEGORY_ABUSED, DNSBL_CATEGORY_LEGIT, DNSBL_CATEGORY_PHISH},
        '127.0.1.105': {DNSBL_CATEGORY_ABUSED, DNSBL_CATEGORY_LEGIT, DNSBL_CATEGORY_MALWARE},
        '127.0.1.106': {DNSBL_CATEGORY_ABUSED,  DNSBL_CATEGORY_LEGIT, DNSBL_CATEGORY_CNC},
        '127.255.255.252': {DNSBL_CATEGORY_ERROR},
        '127.255.255.254': {DNSBL_CATEGORY_ERROR},
        '127.255.255.255': {DNSBL_CATEGORY_ERROR},
    }

    def __init__(self):
        Provider.__init__(self, host='dbl.spamhaus.org')

    def process_response(self, response):
        categories = set()
        for result in response:
            result_categories = self.CATEGORY_MAPPING.get(result.host, {DNSBL_CATEGORY_UNKNOWN})
            categories.update(result_categories)

        return categories


CUSTOM_PROVIDERS = {
    'zen.spamhaus.org': ZenSpamhaus,
    'dbl.spamhaus.org': DblSpamhaus,
}

BASE_PROVIDERS_IP = [
     Provider(host) for host in RAW_PROVIDERS_IP if host not in CUSTOM_PROVIDERS
]
BASE_PROVIDERS_IP.extend([
     CUSTOM_PROVIDERS[host]() for host in RAW_PROVIDERS_IP if host in CUSTOM_PROVIDERS
])
BASE_PROVIDERS_DOMAIN = [
     Provider(host) for host in RAW_PROVIDERS_DOMAIN if host not in CUSTOM_PROVIDERS
]
BASE_PROVIDERS_DOMAIN.extend([
     CUSTOM_PROVIDERS[host]() for host in RAW_PROVIDERS_DOMAIN if host in CUSTOM_PROVIDERS
])
