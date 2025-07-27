from json import dumps as json_dumps

from pycares import ares_query_a_result

from provider import BaseProvider
from config import DEBUG, DNSBL_CATEGORY_ERROR


class DNSBLResponse:
    def __init__(
            self, request: str, provider: BaseProvider,
            response: (list[ares_query_a_result], ares_query_a_result, None),
            error: (None, any),
    ):
        self.request: str = request
        self.provider: BaseProvider = provider
        self.response: (list[ares_query_a_result], ares_query_a_result, None) = response
        self.error: (None, any) = error


class DNSBLResult:
    def __init__(self, request: str, results: list[DNSBLResponse]):
        self.request = request
        self._results: list[DNSBLResponse] = results
        self.detected = False
        self.providers: list[BaseProvider] = []
        self.failed_providers: list[BaseProvider] = []
        self.detected_by: list[BaseProvider] = []
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

            self.providers.append(result.provider)
            if result.error:
                self.failed_providers.append(result.provider)
                continue

            if not result.response:
                continue

            # set detected to True if ip is detected with at least one dnsbl
            provider_categories = result.provider.response_categories(result.response)
            # If the response is an error, do not consider it as detected
            # (refer to https://www.spamhaus.org/faqs/domain-blocklist/#291:~:text=The%20following%20special%20codes%20indicate%20an%20error)
            if provider_categories != {DNSBL_CATEGORY_ERROR}:
                self.detected = True
                self.categories = self.categories.union(provider_categories)
                self.detected_by.append(result.provider)
                self.provider_categories[result.provider.host] = list(provider_categories)

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
