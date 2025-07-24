import abc
import asyncio
import ipaddress
import re
import sys
from json import dumps as json_dumps

import idna
import aiodns

from config import DEFAULT_TIMEOUT
from providers import Provider, BASE_PROVIDERS, DNSBL_CATEGORY_ERROR

if sys.platform == 'win32' and sys.version_info >= (3, 8):
    # fixes https://github.com/dmippolitov/pydnsbl/issues/12
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


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
        self.process_results()

    def process_results(self):
        for result in self._results:
            if not hasattr(result, 'provider'):
                self.failed_providers.append(result)
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


class DNSBLResponse:
    def __init__(self, request: str, provider: Provider, response: any, error: any):
        self.request = request
        self.provider = provider
        self.response = response
        self.error = error


class BaseAsyncDNSBLChecker(abc.ABC):
    def __init__(self, providers: list[Provider] = BASE_PROVIDERS, timeout = DEFAULT_TIMEOUT):
        self.providers: list[Provider] = []
        self._timeout = timeout
        for p in providers:
            if not hasattr(p, 'host'):
                raise ValueError(f'providers should contain only Provider instances: {p} {type(p)}')

            self.providers.append(p)

        self._resolver = None

    async def __aenter__(self):
        self._resolver = aiodns.DNSResolver(timeout=self._timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._resolver:
            await self._resolver.close()

    async def query_provider(self, request: str, provider: Provider) -> DNSBLResponse:
        response = None
        error = None
        dnsbl_query = f"{self.prepare_query(request)}.{provider.host}"

        try:
            response = await self._resolver.query(dnsbl_query, 'A')

        except aiodns.error.DNSError as exc:
            if exc.args[0] != 4: # 4: domain name not found:
                error = exc

        return DNSBLResponse(request=request, provider=provider, response=response, error=error)

    @abc.abstractmethod
    def prepare_query(self, request: str):
        return NotImplemented

    async def check(self, request: str) -> DNSBLResult:
        tasks = []
        for provider in self.providers:
            tasks.append(self.query_provider(request, provider))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        return DNSBLResult(request=request, results=results)

    async def bulk_check(self, requests: list[str]) -> list[DNSBLResult]:
        results = []
        for request in requests:
            results.append(await self.check(request))

        return results


class AsyncCheckIP(BaseAsyncDNSBLChecker):
    def prepare_query(self, request):
        address = ipaddress.ip_address(request)
        if address.version == 4:
            return '.'.join(reversed(request.split('.')))

        if address.version == 6:
            # according to RFC: https://tools.ietf.org/html/rfc5782#section-2.4
            request_stripped = address.exploded.replace(':', '')
            return '.'.join(reversed(request_stripped))

        raise ValueError('unknown ip version')


class AsyncCheckDomain(BaseAsyncDNSBLChecker):
    # https://regex101.com/r/vdrgm7/1
    DOMAIN_REGEX = re.compile(r"^(((?!-))(xn--|_{1,1})?[a-z0-9-]{0,61}[a-z0-9]{1,1}\.)*(xn--[a-z0-9][a-z0-9\-]{0,60}|[a-z0-9-]{1,30}\.[a-z]{2,})$")

    def prepare_query(self, request):
        request = request.lower() # Adding support for capitalized letters in domain name.
        domain_idna = idna.encode(request).decode()
        if not self.DOMAIN_REGEX.match(domain_idna):
            raise ValueError(f'should be valid domain, got {domain_idna}')

        return domain_idna


class BaseDNSBLChecker:
    def __init__(self,
             async_checker: BaseAsyncDNSBLChecker,
             providers: list[Provider] = BASE_PROVIDERS, timeout = DEFAULT_TIMEOUT,
     ):
        self._async_checker = async_checker(providers=providers, timeout=timeout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del exc_tb, exc_val, exc_type

    @staticmethod
    def _raise_result_exception(result: DNSBLResult) -> None:
        if isinstance(result, Exception):
            raise result

    async def _check_async(self, request: str) -> DNSBLResult:
        async with self._async_checker as checker:
            return await checker.check(request)

    def check(self, request: str) -> DNSBLResult:
        result = asyncio.run(self._check_async(request))
        self._raise_result_exception(result)
        return result

    async def _bulk_check_async(self, request: list[str]) -> list[DNSBLResult]:
        async with self._async_checker as checker:
            return await checker.bulk_check(request)

    def bulk_check(self, request: list[str]) -> list[DNSBLResult]:
        results = asyncio.run(self._bulk_check_async(request))
        for r in results:
            self._raise_result_exception(r)

        return results


class CheckIP(BaseDNSBLChecker):
    def __init__(self, providers: list[Provider] = BASE_PROVIDERS, timeout = DEFAULT_TIMEOUT):
        BaseDNSBLChecker.__init__(self, async_checker=AsyncCheckIP, providers=providers, timeout=timeout)


class CheckDomain(BaseDNSBLChecker):
    def __init__(self, providers: list[Provider] = BASE_PROVIDERS, timeout = DEFAULT_TIMEOUT):
        BaseDNSBLChecker.__init__(self, async_checker=AsyncCheckDomain, providers=providers, timeout=timeout)
