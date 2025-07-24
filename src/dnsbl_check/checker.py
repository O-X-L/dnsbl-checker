import re
import sys
import abc
import asyncio
import ipaddress
from time import time
from json import dumps as json_dumps

import idna
import aiodns

from result import DNSBLResult
from config import DEFAULT_TIMEOUT, DEBUG
from provider import Provider, BASE_PROVIDERS_IP, BASE_PROVIDERS_DOMAIN

if sys.platform == 'win32' and sys.version_info >= (3, 8):
    # fixes https://github.com/dmippolitov/pydnsbl/issues/12
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class DNSBLResponse:
    def __init__(self, request: str, provider: Provider, response: any, error: any):
        self.request = request
        self.provider = provider
        self.response = response
        self.error = error


class BaseAsyncDNSBLChecker(abc.ABC):
    def __init__(
            self, timeout = DEFAULT_TIMEOUT,
            providers: list[Provider] = BASE_PROVIDERS_IP, skip_providers: list[str] = None,
    ):
        self.providers: list[Provider] = []
        self.skip_providers: list[str] = []
        if skip_providers is not None:
            self.skip_providers = skip_providers

        self._timeout = timeout
        for p in providers:
            if not hasattr(p, 'host'):
                raise ValueError(f'providers should contain only Provider instances: {p} {type(p)}')

            self.providers.append(p)

        self._resolver = None
        self._debug_time = int(time())

    async def __aenter__(self):
        self._resolver = aiodns.DNSResolver(timeout=self._timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._resolver:
            await self._resolver.close()

    def _debug_dump(self, provider: str, dns: str, response: any, error: any):
        with open(f'/tmp/dnsbl_{self._debug_time}_{provider}.json', 'w', encoding='utf-8') as f:
            f.write(json_dumps({
                'dns': str(dns),
                'response': str(response),
                'error': str(error),
            }))

    async def query_provider(self, request: str, provider: Provider) -> DNSBLResponse:
        response, error, debug_error = None, None, None
        dnsbl_query = f"{self.prepare_query(request)}.{provider.host}"

        try:
            response = await self._resolver.query(dnsbl_query, 'A')

        except aiodns.error.DNSError as e:
            debug_error = e
            if e.args[0] != 4: # 4: domain name not found:
                error = e

        if DEBUG:
            self._debug_dump(provider=provider.host, dns=dnsbl_query, response=response, error=debug_error)

        return DNSBLResponse(request=request, provider=provider, response=response, error=error)

    @abc.abstractmethod
    def prepare_query(self, request: str):
        return NotImplemented

    async def check(self, request: str) -> DNSBLResult:
        tasks = []
        for provider in self.providers:
            if provider.host in self.skip_providers:
                continue

            tasks.append(self.query_provider(request, provider))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        return DNSBLResult(request=request, results=results)


class AsyncCheckIP(BaseAsyncDNSBLChecker):
    def prepare_query(self, request):
        ip = ipaddress.ip_address(request)
        if not ip.is_global:
            raise ValueError('Only public IPs can be checked')

        if ip.version == 4:
            return '.'.join(reversed(request.split('.')))

        if ip.version == 6:
            # according to RFC: https://tools.ietf.org/html/rfc5782#section-2.4
            request_stripped = ip.exploded.replace(':', '')
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
    def __init__(
            self, async_checker: BaseAsyncDNSBLChecker,
            providers: list[Provider] = BASE_PROVIDERS_IP, timeout = DEFAULT_TIMEOUT, skip_providers: list[str] = None,
    ):
        self._async_checker = async_checker(providers=providers, timeout=timeout, skip_providers=skip_providers)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del exc_tb, exc_val, exc_type

    async def _check_async(self, request: str) -> DNSBLResult:
        async with self._async_checker as checker:
            return await checker.check(request)

    def check(self, request: str) -> DNSBLResult:
        return asyncio.run(self._check_async(request))


class CheckIP(BaseDNSBLChecker):
    def __init__(
            self, timeout = DEFAULT_TIMEOUT,
            providers: list[Provider] = BASE_PROVIDERS_IP, skip_providers: list[str] = None,
    ):
        BaseDNSBLChecker.__init__(
            self,
            async_checker=AsyncCheckIP,
            providers=providers,
            skip_providers=skip_providers,
            timeout=timeout,
        )


class CheckDomain(BaseDNSBLChecker):
    def __init__(
            self, timeout = DEFAULT_TIMEOUT,
            providers: list[Provider] = BASE_PROVIDERS_DOMAIN, skip_providers: list[str] = None,
    ):
        BaseDNSBLChecker.__init__(
            self,
            async_checker=AsyncCheckDomain,
            providers=providers,
            skip_providers=skip_providers,
            timeout=timeout,
        )
