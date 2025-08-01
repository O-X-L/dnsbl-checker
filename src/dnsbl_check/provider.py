import asyncio

import aiodns
from pycares import ares_query_a_result

from utils import valid_domain
from config import DNSBL_CATEGORY_UNKNOWN, DEBUG


class BaseProvider:
    IP4 = False
    IP6 = False
    DOMAIN = False
    HOST = None

    RESPONSE_CATEGORIES = {}

    def __init__(self, host: str = None):
        if self.HOST is None and host is None:
            raise ValueError('The provider hostname needs to be provided')

        if self.HOST is not None:
            self.host = self.HOST

        else:
            self.host = host

        _, valid = valid_domain(self.host)
        if not valid:
            raise ValueError('Invalid provider hostname supplied')

        self.ns_ips: None|list[str] = None
        self.ns_error: bool = False

    def response_categories(self, response: (list[ares_query_a_result], ares_query_a_result)) -> set[str]:
        categories = set()

        if not response:
            return categories

        if len(self.RESPONSE_CATEGORIES) == 0:
            categories.add(DNSBL_CATEGORY_UNKNOWN)

        else:
            if not isinstance(response, list):
                response = [response]

            for res in response:
                cat = self.RESPONSE_CATEGORIES.get(res.host, DNSBL_CATEGORY_UNKNOWN)
                if isinstance(cat, set):
                    categories.update(cat)

                else:
                    categories.add(cat)

        return categories

    def __repr__(self):
        return f"<Provider: {self.host}>"

    async def query_ns_ips(self, resolver):
        if self.ns_ips is not None or self.ns_error:
            # further queries in this session
            return

        try:
            ns_dns = await resolver.query(self.host, 'NS')
            if not isinstance(ns_dns, list):
                ns_dns = [ns_dns]

            ns_dns = [r.host for r in ns_dns]
            if len(ns_dns) == 0:
                raise aiodns.error.DNSError

            if len(ns_dns) > 2:
                ns_dns = ns_dns[0:2]

            self.ns_ips = []
            for dns in ns_dns:
                ns_ips = await resolver.query(dns, 'A')
                if not isinstance(ns_ips, list):
                    ns_ips = [ns_ips]

                ns_ips = [r.host for r in ns_ips]
                self.ns_ips.extend(ns_ips)

            if self.ns_ips is not None and len(self.ns_ips) == 0:
                self.ns_ips = None

        except aiodns.error.DNSError as e:
            self.ns_error = True
            if DEBUG:
                print('NS QUERY ERROR', self.host, e)


async def query_provider_nameservers(providers: list[BaseProvider], resolver):
    """
    Queries the nameservers for all providers (if they have a valid NS-record)
    """
    tasks = []
    for provider in providers:
        tasks.append(provider.query_ns_ips(resolver))

    await asyncio.gather(*tasks, return_exceptions=True)


class Provider(BaseProvider):
    IP4 = True
    IP6 = True
    DOMAIN = True


class ProviderIP(BaseProvider):
    IP4 = True
    IP6 = True
    DOMAIN = False


class ProviderIP4(BaseProvider):
    IP4 = True
    IP6 = False
    DOMAIN = False


class ProviderIP6(BaseProvider):
    IP4 = False
    IP6 = True
    DOMAIN = False


class ProviderDomain(BaseProvider):
    IP4 = False
    IP6 = False
    DOMAIN = True
