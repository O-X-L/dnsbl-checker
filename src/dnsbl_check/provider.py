from pycares import ares_query_a_result

from config import DNSBL_CATEGORY_UNKNOWN


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
