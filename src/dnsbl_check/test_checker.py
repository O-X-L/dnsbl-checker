import pytest


def test_1():
    from providers import Provider
    from checker import CheckIP, CheckDomain, AsyncCheckDomain
    pass

# todo: mock responses of dns-resolver to get stable output
# todo: CheckIP
# todo: CheckDomain
# todo: invalid IPs and Domains
# todo: Domain variants (capitalized / 3th+ levels, idna)
# todo: IPv4 + IPv6


# def test_ipv6_converting():
#     # https://datatracker.ietf.org/doc/html/rfc5782#section-2.4
#     checker = AsyncCheckDomain()
#     assert checker.prepare_query('2001:db8:1:2:3:4:567:89ab') == "b.a.9.8.7.6.5.0.4.0.0.0.3.0.0.0.2.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2"
#     assert checker.prepare_query('2600:2600::f03c:91ff:fe50:d2') == "2.d.0.0.0.5.e.f.f.f.1.9.c.3.0.f.0.0.0.0.0.0.0.0.0.0.6.2.0.0.6.2"
