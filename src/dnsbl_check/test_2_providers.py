from test_1_checker import MockedDNSResolver, AresResponse


def test_provider_custom_init():
    from provider_config import BASE_PROVIDERS_IP, ProviderOXLRisk, BASE_PROVIDERS_DOMAIN, ProviderDblSpamhaus

    for p in BASE_PROVIDERS_IP:
        if p.host == ProviderOXLRisk.HOST:
            assert isinstance(p, ProviderOXLRisk)

    for p in BASE_PROVIDERS_DOMAIN:
        if p.host == ProviderDblSpamhaus.HOST:
            assert isinstance(p, ProviderDblSpamhaus)

    assert ProviderOXLRisk('dnsbl.invalid.org').host == ProviderOXLRisk.HOST


def test_provider_query_support():
    from provider import Provider, ProviderIP, ProviderIP4, ProviderDomain
    from provider_config import BASE_PROVIDERS_IP, BASE_PROVIDERS_DOMAIN

    p = Provider('dnsbl.example.org')
    assert p.IP4 and p.IP6 and p.DOMAIN

    p = ProviderIP('dnsbl.example.org')
    assert p.IP4 and p.IP6 and not p.DOMAIN

    p = ProviderIP4('dnsbl.example.org')
    assert p.IP4 and not p.IP6 and not p.DOMAIN

    p = ProviderDomain('dnsbl.example.org')
    assert not p.IP4 and not p.IP6 and p.DOMAIN

    p = ProviderDomain('dnsbl.example.org')
    assert not p.IP4 and not p.IP6 and p.DOMAIN

    p = BASE_PROVIDERS_IP[0]
    assert isinstance(p, ProviderIP)
    assert p.IP4 and p.IP6 and not p.DOMAIN

    p = BASE_PROVIDERS_DOMAIN[0]
    assert isinstance(p, ProviderDomain)
    assert not p.IP4 and not p.IP6 and p.DOMAIN


def test_provider_query_support_skip(mocker):
    mocker.patch('aiodns.DNSResolver', MockedDNSResolver)

    from checker import CheckDomain
    from provider_config import ProviderOXLRisk

    with CheckDomain(providers=[ProviderOXLRisk()]) as c:
        d = 'this-is-malware.org'
        r = c.check(d)
        assert r.request == d
        assert len(r.providers) == 0
        assert not r.detected
        assert len(r.failed_providers) == 0
        assert len(r.general_errors) == 0


def test_provider_custom_categories_method(mocker):
    from provider import BaseProvider, DNSBL_CATEGORY_UNKNOWN

    p = BaseProvider('dnsbl.example.org')
    p.RESPONSE_CATEGORIES = {'127.0.0.3': 'test'}

    r = AresResponse()
    r.host = '127.0.0.2'
    assert p.response_categories(r) == {DNSBL_CATEGORY_UNKNOWN}

    r.host = '127.0.0.3'
    assert p.response_categories(r) == {'test'}

    r = [AresResponse(), AresResponse()]
    r[0].host = '127.0.0.2'
    r[1].host = '127.0.0.2'
    assert p.response_categories(r) == {DNSBL_CATEGORY_UNKNOWN}

    r = [AresResponse(), AresResponse()]
    r[0].host = '127.0.0.2'
    r[1].host = '127.0.0.3'
    assert p.response_categories(r) == {DNSBL_CATEGORY_UNKNOWN, 'test'}


def test_provider_custom_categories(mocker):
    res_code = '127.0.0.3'
    test_responses = {
        'ip.dnsbl.risk.oxl.app': '127.0.0.3',
    }
    mock_resolver = mocker.patch('aiodns.DNSResolver', autospec=True)
    mock_resolver.return_value = MockedDNSResolver(mock_responses=test_responses)

    from checker import CheckIP
    from provider_config import ProviderOXLRisk

    with CheckIP(providers=[ProviderOXLRisk()]) as c:
        ip = '1.1.1.1'
        r = c.check(ip)
        assert r.request == ip
        assert len(r.providers) == 1
        assert r.detected
        assert [p.host for p in r.detected_by] == list(test_responses.keys())
        assert len(r.failed_providers) == 0
        assert len(r.general_errors) == 0
        assert list(r.categories)[0] == ProviderOXLRisk.RESPONSE_CATEGORIES[res_code]
