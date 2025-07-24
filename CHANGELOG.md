# Changelog

## [2.0.1] - 2025-?

## Deprecations
- Removed `bulk_check` as high-volume lookups are discouraged by DNSBL-providers and users could simply use a loop instead

## [2.0.0] - 2025-07-24

## Features
- Type hints
- Usage via Context-Manager
- Simple CLI-interface

## Fixes
- Cleanup of async resources
- [Errors interpreted as matches](https://github.com/dmippolitov/pydnsbl/issues/27) [@felmoltor](https://github.com/felmoltor)
- [Removed uceprotect.net list](https://github.com/dmippolitov/pydnsbl/issues/38) [@felmoltor](https://github.com/felmoltor)

----

## [1.1.7] - 2025-03-25
### Changed
- Updated providers list
- Security Fixes (IDNA vuln)

----

## [1.1.6] - 2023-10-17
- Fixed incorrect ipv6 conversion (#31)

----

## [1.1.5] - 2023-01-02
### Changed
- Updated providers list

----

## [1.1.4] - 2021-10-03
### Changed
- improved domain regex to allow usage for 3rd+ level domains (inspired by #22)
- removed some duplicated sorbs.net blacklists (#21)

----

## [1.1.0] - 2020-09-27
### Added
- ipv6 support for DNSBLIpChecker

### Changed
- Updated providers list

----

## [1.0.0] - 2020-03-08
### Added
- CHANGELOG
- Domain DNSBL Providers (dbl.spamhaus.org, uribl.spameatingmonkey.net, multi.surbl.org, rhsbl.sorbs.net)
- DNSBLIpChecker class to check ips
- DNSBLDomainChecker class to check domains

### Changed
- DNSBLChecker marked as deprecated
