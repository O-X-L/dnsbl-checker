from os import path as os_path
from sys import path as sys_path
from argparse import ArgumentParser
from json import dumps as json_dumps

sys_path.append(os_path.dirname(os_path.abspath(__file__)))

from checker import DNSBLDomainChecker, DNSBLIpChecker


def main():
    parser = ArgumentParser(
        prog='DNS-BL Lookup-Client'
    )
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument('-i', '--ip', type=str, default=None, help='IP to check')
    g.add_argument('-d', '--domain', type=str, default=None, help='Domain to check')
    parser.add_argument(
        '-p', '--providers', type=bool, default=False,
        help='If the provider details should be added to the output',
    )
    args = parser.parse_args()

    if args.ip is not None:
        print(f'Checking IP {args.ip}..')
        checker = DNSBLIpChecker()
        result = checker.check(args.ip)

    else:
        print(f'Checking Domain {args.domain}..')
        checker = DNSBLDomainChecker()
        result = checker.check(args.domain)

    response = {
        'detected': result.detected,
        'detected_by': result.detected_by,
        'categories': list(result.categories),
    }
    if args.providers:
        response['providers'] = [p.host for p in result.providers]
        response['failed_providers'] = [p.host for p in result.failed_providers]

    print(json_dumps(response, indent=2))


if __name__ == '__main__':
    main()
