from os import path as os_path
from sys import path as sys_path
from argparse import ArgumentParser
from json import dumps as json_dumps

sys_path.append(os_path.dirname(os_path.abspath(__file__)))

# pylint: disable=C0413
from provider import Provider
from checker import CheckDomain, CheckIP
from provider_config import BASE_PROVIDERS_IP, BASE_PROVIDERS_DOMAIN


def main():
    parser = ArgumentParser(
        prog='DNS-BL Lookup-Client'
    )
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument('-i', '--ip', type=str, default=None, help='IP to check')
    g.add_argument('-d', '--domain', type=str, default=None, help='Domain to check')
    parser.add_argument('-j', '--json', action='store_true', default=False, help='Only output JSON')
    parser.add_argument(
        '-s', '--skip-providers', type=str, default='',
        help='Comma-separated list of base-providers to skip',
    )
    parser.add_argument(
        '-a', '--add-providers', type=str, default='',
        help='Comma-separated list of additional DNS-BL provider-domains to query',
    )
    parser.add_argument(
        '-o', '--only-providers', type=str, default='',
        help='Comma-separated list of DNS-BL provider-domains to query (ignoring the built-in default providers)',
    )
    parser.add_argument(
        '--details', action='store_true', default=False,
        help='If the result details should be added to the output',
    )
    args = parser.parse_args()

    add_providers = [Provider(p) for p in args.add_providers.split(',')]
    only_providers = [Provider(p) for p in args.only_providers.split(',')]
    skip_providers = args.skip_providers.split(',')

    if args.ip is not None:
        if len(only_providers) > 0:
            providers = only_providers

        else:
            providers = BASE_PROVIDERS_IP + add_providers

        if not args.json:
            print(f'Checking IP {args.ip} ..')

        with CheckIP(providers=providers, skip_providers=skip_providers, ) as checker:
            result = checker.check(args.ip)

    else:
        if len(only_providers) > 0:
            providers = only_providers

        else:
            providers = BASE_PROVIDERS_DOMAIN + add_providers

        if not args.json:
            print(f'Checking Domain {args.domain} ..')

        with CheckDomain(providers=providers, skip_providers=skip_providers) as checker:
            result = checker.check(args.domain)

    response = {
        'detected': result.detected,
        'detected_by': [p.host for p in result.detected_by],
        'categories': list(result.categories),
        'general_errors': list(result.general_errors),
        'count': {
            'detected': len(result.detected_by),
            'checked': len(result.providers),
            'failed': len(result.failed_providers),
        }
    }
    if args.details:
        response['detected_provider_categories'] = result.provider_categories
        response['checked_providers'] = [p.host for p in result.providers]
        response['failed_providers'] = [p.host for p in result.failed_providers]

    print(json_dumps(response, indent=2))


if __name__ == '__main__':
    main()
