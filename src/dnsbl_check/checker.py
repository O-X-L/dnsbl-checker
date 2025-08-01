import sys
import abc
import asyncio
import ipaddress
from time import time
from json import dumps as json_dumps

import aiodns

from utils import valid_domain
from config import DEFAULT_TIMEOUT, DEBUG
from result import DNSBLResult, DNSBLResponse
from provider import BaseProvider, query_provider_nameservers
from provider_config import BASE_PROVIDERS_IP, BASE_PROVIDERS_DOMAIN

if sys.platform == 'win32' and sys.version_info >= (3, 8):
    # fixes https://github.com/dmippolitov/pydnsbl/issues/12
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class BaseAsyncDNSBLChecker(abc.ABC):
    """
    Basic DNS-query handling
    """
    def __init__(
            self, timeout = DEFAULT_TIMEOUT, direct_nameservers: bool = False, nameservers: list[str] = None,
            providers: list[BaseProvider] = BASE_PROVIDERS_IP, skip_providers: list[str] = None,
    ):
        self.providers: list[BaseProvider] = []
        self.nameservers: list[str]|None = nameservers
        self.direct_nameservers: bool = direct_nameservers
        self.skip_providers: list[str] = []
        if skip_providers is not None:
            self.skip_providers = skip_providers

        self._timeout = timeout
        for p in providers:
            if not isinstance(p, BaseProvider):
                raise ValueError(f'providers should contain only Provider instances: {p} {type(p)}')

            self.providers.append(p)

        self._resolver = None
        self._debug_time = int(time())

    async def __aenter__(self):
        self._resolver = aiodns.DNSResolver(timeout=self._timeout, nameservers=self.nameservers)
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

    async def query_provider(self, request: str, provider: BaseProvider) -> DNSBLResponse:
        response, error, debug_error = None, None, None
        dnsbl_query = f"{self.prepare_query(request)}.{provider.host}"

        try:
            if provider.ns_ips is not None:
                self._resolver.nameservers = provider.ns_ips

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
        if self.direct_nameservers:
            await query_provider_nameservers(providers=self.providers, resolver=self._resolver)

        tasks = []
        for provider in self.providers:
            if provider.host in self.skip_providers:
                continue

            if isinstance(self, AsyncCheckIP):
                if not provider.IP4 and not provider.IP6:
                    if DEBUG:
                        print(f"DEBUG: Skipping provider {provider.host} because it does not support IP-lookups")

                    continue

                if not provider.IP6 and request.find(':') != -1:
                    if DEBUG:
                        print(f"DEBUG: Skipping provider {provider.host} because it does not support IPv6-lookups")

                    continue

                if not provider.IP4 and request.find(':') == -1:
                    if DEBUG:
                        print(f"DEBUG: Skipping provider {provider.host} because it does not support IPv4-lookups")

                    continue

            elif isinstance(self, AsyncCheckDomain) and not provider.DOMAIN:
                if DEBUG:
                    print(f"DEBUG: Skipping provider {provider.host} because it does not support Domain-lookups")

                continue

            tasks.append(self.query_provider(request, provider))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        return DNSBLResult(request=request, results=results)


class AsyncCheckIP(BaseAsyncDNSBLChecker):
    """
    Async equivalent to 'CheckIP'
    """
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
    """
    Async equivalent to 'CheckDomain'
    """
    def prepare_query(self, request):
        domain, valid = valid_domain(request)
        if not valid:
            raise ValueError('Invalid domain provided')

        return domain


class BaseDNSBLChecker:
    """
    Synchronous usage to async calls
    """
    def __init__(
            self, async_checker: BaseAsyncDNSBLChecker, direct_nameservers: bool = False, nameservers: list[str] = None,
            providers: list[BaseProvider] = BASE_PROVIDERS_IP, timeout = DEFAULT_TIMEOUT, skip_providers: list[str] = None,
    ):
        self._async_checker = async_checker(
            providers=providers,
            timeout=timeout,
            skip_providers=skip_providers,
            nameservers=nameservers,
            direct_nameservers=direct_nameservers,
        )

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
    """
    Check if an IP is listed on a blacklist
    Some providers might be skipped, if we know they do not support IPv4 or IPv6 addresses

    Arguments:
        timeout: DNS-query timeout in seconds
        nameservers: Nameservers to query from
        direct_nameservers: If we should try to query the DNS-BL nameservers directly (if they have a valid NS-record)
        providers: List of Providers to query from
        skip_providers: List of Providers that are listed in 'providers' but should be skipped
    """
    def __init__(
            self, timeout = DEFAULT_TIMEOUT, direct_nameservers: bool = False, nameservers: list[str] = None,
            providers: list[BaseProvider] = BASE_PROVIDERS_IP, skip_providers: list[str] = None,
    ):
        BaseDNSBLChecker.__init__(
            self,
            async_checker=AsyncCheckIP,
            providers=providers,
            skip_providers=skip_providers,
            timeout=timeout,
            nameservers=nameservers,
            direct_nameservers=direct_nameservers,
        )


class CheckDomain(BaseDNSBLChecker):
    """
    Check if a domain is listed on a blacklist

    Arguments:
        timeout: DNS-query timeout in seconds
        nameservers: Nameservers to query from
        direct_nameservers: If we should try to query the DNS-BL nameservers directly (if they have a valid NS-record)
        providers: List of Providers to query from
        skip_providers: List of Providers that are listed in 'providers' but should be skipped
    """
    def __init__(
            self, timeout = DEFAULT_TIMEOUT, direct_nameservers: bool = False, nameservers: list[str] = None,
            providers: list[BaseProvider] = BASE_PROVIDERS_DOMAIN, skip_providers: list[str] = None,
    ):
        BaseDNSBLChecker.__init__(
            self,
            async_checker=AsyncCheckDomain,
            providers=providers,
            skip_providers=skip_providers,
            timeout=timeout,
            nameservers=nameservers,
            direct_nameservers=direct_nameservers,
        )
