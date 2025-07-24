from json import dumps as json_dumps

from config import DEBUG
from provider import Provider, DNSBL_CATEGORY_ERROR


class DNSBLResult:
    """
    DNSBL Result class to keep all info about ip request results.

    Attributes:
        * request - checked ip/domain
        * providers - dnsbl that was asked for response while checking
        * failed_provider - dnsbl that was unable to provide result due
            to connection issues (connection timeout etc...)
        * detected_by - list of providers that have the ip listed
        * provider_categories - dnsbl that have ip listed and categories detected by
            this dnsbls. dict: {'dnsbl_list_name': list(categories_from_this_dnsbl)}
        * categories - set of dnsbl categories from all providers (subset of DNSBL_CATEGORIES)
    """
    def __init__(self, request: str, results: any):
        self.request = request
        self._results = results
        self.detected = False
        self.providers: list[Provider] = []
        self.failed_providers: list[Provider] = []
        self.detected_by: list[Provider] = []
        self.provider_categories: dict[str: list[str]] = {}
        self.categories = set()
        self.general_errors = set()

        self.process_results()

    def process_results(self):
        for result in self._results:
            if not hasattr(result, 'provider'):
                if DEBUG and isinstance(result, Exception):
                    raise result

                self.general_errors.add(str(result))
                continue

            provider = result.provider
            self.providers.append(provider)
            if result.error:
                self.failed_providers.append(provider)
                continue

            if not result.response:
                continue

            # set detected to True if ip is detected with at least one dnsbl
            provider_categories = provider.process_response(result.response)
            # If the response is an error, do not consider it as detected
            # (refer to https://www.spamhaus.org/faqs/domain-blocklist/#291:~:text=The%20following%20special%20codes%20indicate%20an%20error)
            if provider_categories != {DNSBL_CATEGORY_ERROR}:
                self.detected = True
                self.categories = self.categories.union(provider_categories)
                self.detected_by.append(provider)
                self.provider_categories[provider.host] = list(provider_categories)

    def __repr__(self):
        detected = ' [DETECTED]' if self.detected else ''
        return f"<DNSBLResult: {self.request}{detected} ({len(self.detected_by)}/{len(self.providers)})>"

    def to_dict(self) -> dict:
        return {
            'request': self.request,
            'detected': self.detected,
            'detected_by': [p.host for p in self.detected_by],
            'categories': list(self.categories),
            'general_errors': list(self.general_errors),
            'count': {
                'detected': len(self.detected_by),
                'checked': len(self.providers),
                'failed': len(self.failed_providers),
            },
            'detected_provider_categories': self.provider_categories,
            'checked_providers': [p.host for p in self.providers],
            'failed_providers': [p.host for p in self.failed_providers],
        }

    def to_json(self, indent: int = 2) -> str:
        return json_dumps(self.to_dict(), indent=indent)
