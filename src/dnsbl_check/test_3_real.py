import pytest


# NOTE: DO NOT assert on detection as we cannot impact the result

from config import RAW_PROVIDERS_DOMAIN, RAW_PROVIDERS_IP

PROVIDER_COUNT_IP = len(RAW_PROVIDERS_IP)
PROVIDER_COUNT_DOMAIN = len(RAW_PROVIDERS_DOMAIN)


@pytest.mark.parametrize(
    "ip",
    [
        '134.209.173.54',
        '2a01:4f8:c010:97b4::1',
    ],
)
def test_check_real_ip(ip):
    from checker import CheckIP

    with CheckIP() as c:
        r = c.check(ip)
        assert r.request == ip
        assert len(r.providers) == PROVIDER_COUNT_IP
        assert len(r.general_errors) == 0
        if r.detected:
            assert len(r.detected_by) > 0
            assert len(r.categories) > 0


@pytest.mark.parametrize(
    "domain",
    [
        'google.com',
    ],
)
def test_check_real_domain(domain):
    from checker import CheckDomain

    with CheckDomain() as c:
        r = c.check(domain)
        assert r.request == domain
        assert len(r.providers) == PROVIDER_COUNT_DOMAIN
        assert len(r.general_errors) == 0
        if r.detected:
            assert len(r.detected_by) > 0
            assert len(r.categories) > 0
