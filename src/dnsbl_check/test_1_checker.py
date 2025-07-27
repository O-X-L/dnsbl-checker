import pytest

import cffi
import aiodns
from pycares import ares_query_a_result

ffi = cffi.FFI()

from provider_config import BASE_PROVIDERS_IP
from config import RAW_PROVIDERS_IP, RAW_PROVIDERS_DOMAIN

PROVIDER_COUNT_IP = len(RAW_PROVIDERS_IP)
PROVIDER_COUNT_DOMAIN = len(RAW_PROVIDERS_DOMAIN)
PROVIDER_COUNT_IP4 = len([p for p in BASE_PROVIDERS_IP if p.IP4])
PROVIDER_COUNT_IP6 = len([p for p in BASE_PROVIDERS_IP if p.IP6])


class AresResponse:
    def __init__(self):
        # just some value as we need it to initialize ares_query_a_result
        self.ipaddr = ffi.new("char[]", '0.0.0.0'.encode('utf-8') + b'\0')
        self.ttl = 5
        self.host = ''


class MockedDNSResolver:
    def __init__(self, timeout = 5, mock_responses: dict = None):
        del timeout
        self._mock_responses = mock_responses

    async def query(self, query: str, rtype: str = 'A') -> ares_query_a_result:
        del rtype
        if self._mock_responses is not None:
            for test_provider, test_response in self._mock_responses.items():
                if query.endswith(test_provider):
                    r = ares_query_a_result(AresResponse())
                    r.host = test_response
                    return r

        e = aiodns.error.DNSError()
        e.args = (4,)
        raise e

    async def close(self):
        pass


def test_check_ip(mocker):
    test_responses = {
        'b.barracudacentral.org': '127.0.0.2',
        'drone.abuse.ch': '127.0.0.2',
    }
    mock_resolver = mocker.patch('aiodns.DNSResolver', autospec=True)
    mock_resolver.return_value = MockedDNSResolver(mock_responses=test_responses)

    from checker import CheckIP

    with CheckIP() as c:
        ip = '1.1.1.1'
        r = c.check(ip)
        assert r.request == ip
        assert len(r.providers) == PROVIDER_COUNT_IP4
        assert r.detected
        assert str(r) == f'<DNSBLResult: {ip} [DETECTED] (2/{PROVIDER_COUNT_IP4})>'
        assert [p.host for p in r.detected_by] == list(test_responses.keys())
        assert len(r.failed_providers) == 0
        assert len(r.general_errors) == 0
        assert r.categories == {'unknown'}


def test_check_domain(mocker):
    test_responses = {
        'multi.surbl.org': '127.0.0.2',
    }
    mock_resolver = mocker.patch('aiodns.DNSResolver', autospec=True)
    mock_resolver.return_value = MockedDNSResolver(mock_responses=test_responses)

    from checker import CheckDomain

    with CheckDomain() as c:
        d = 'this-is-malware.org'
        r = c.check(d)
        assert r.request == d
        assert len(r.providers) == PROVIDER_COUNT_DOMAIN
        assert r.detected
        assert str(r) == f'<DNSBLResult: {d} [DETECTED] (1/{PROVIDER_COUNT_DOMAIN})>'
        assert [p.host for p in r.detected_by] == list(test_responses.keys())
        assert len(r.failed_providers) == 0
        assert len(r.general_errors) == 0
        assert r.categories == {'unknown'}


@pytest.mark.parametrize(
    "ip",
    [
        '1.1.1.x',
        'xxx',
        '::',
        '127.0.0.1',
    ],
)
def test_check_ip_invalid(mocker, ip):
    mocker.patch('aiodns.DNSResolver', MockedDNSResolver)

    from ipaddress import ip_address, AddressValueError

    from checker import CheckIP

    public_ip = True
    try:
        public_ip = ip_address(ip).is_global

    except (ValueError, AddressValueError):
        pass

    with CheckIP() as c:
        r = c.check(ip)
        assert r.request == ip
        assert len(r.general_errors) == 1

        if public_ip:
            assert list(r.general_errors)[0] == f"'{ip}' does not appear to be an IPv4 or IPv6 address"

        else:
            assert list(r.general_errors)[0] == 'Only public IPs can be checked'

        assert len(r.providers) == 0
        assert not r.detected
        assert len(r.failed_providers) == 0


@pytest.mark.parametrize(
    "domain,error",
    [
        ['!nvalid.org', "Codepoint U+0021 at position 1 of '!nvalid' not allowed"]
    ],
)
def test_check_domain_invalid(mocker, domain, error):
    mocker.patch('aiodns.DNSResolver', MockedDNSResolver)

    from checker import CheckDomain

    with CheckDomain() as c:
        r = c.check(domain)
        assert r.request == domain
        assert len(r.general_errors) == 1
        assert list(r.general_errors)[0] == error
        assert len(r.providers) == 0
        assert not r.detected
        assert len(r.failed_providers) == 0


@pytest.mark.parametrize(
    "domain",
    [
        'Google.com',
        'дом.рф',
        'www.digital.govt.nz',
    ],
)
def test_check_domain_variations(mocker, domain):
    mocker.patch('aiodns.DNSResolver', MockedDNSResolver)

    from checker import CheckDomain

    with CheckDomain() as c:
        r = c.check(domain)
        assert r.request == domain
        assert len(r.general_errors) == 0
        assert len(r.providers) == PROVIDER_COUNT_DOMAIN
        assert not r.detected
        assert len(r.failed_providers) == 0



def test_check_ip6(mocker):
    test_responses = {
        'b.barracudacentral.org': '127.0.0.2',
        'drone.abuse.ch': '127.0.0.2',
    }
    mock_resolver = mocker.patch('aiodns.DNSResolver', autospec=True)
    mock_resolver.return_value = MockedDNSResolver(mock_responses=test_responses)

    from checker import CheckIP

    with CheckIP() as c:
        ip = '2a01:4f8:c010:97b4::1'
        r = c.check(ip)
        assert r.request == ip
        assert len(r.providers) == PROVIDER_COUNT_IP6
        assert r.detected
        assert str(r) == f'<DNSBLResult: {ip} [DETECTED] (2/{PROVIDER_COUNT_IP6})>'
        assert [p.host for p in r.detected_by] == list(test_responses.keys())
        assert len(r.failed_providers) == 0
        assert len(r.general_errors) == 0
        assert r.categories == {'unknown'}


def test_ipv6_converting():
    # https://datatracker.ietf.org/doc/html/rfc5782#section-2.4

    from checker import AsyncCheckIP

    checker = AsyncCheckIP()
    assert checker.prepare_query('2600:2600::f03c:91ff:fe50:d2') == "2.d.0.0.0.5.e.f.f.f.1.9.c.3.0.f.0.0.0.0.0.0.0.0.0.0.6.2.0.0.6.2"
