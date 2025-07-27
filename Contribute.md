# Contribute

Contributions are welcome (:

Feel free to:
* update and extend [the Provider-List](https://github.com/O-X-L/dnsbl-checker/blob/latest/src/dnsbl_check/config.py), [the Provider-Config](https://github.com/O-X-L/dnsbl-checker/blob/latest/src/dnsbl_check/provider_config.py) and [Docs](https://github.com/O-X-L/dnsbl-checker/blob/latest/Providers.md)
* [report Issues](https://github.com/O-X-L/dnsbl-checker/issues)
* [request Features](https://github.com/O-X-L/dnsbl-checker/issues) (*like additional base-lists*)
* [Discuss the implementation](https://github.com/O-X-L/dnsbl-checker/discussions)
* [create Pull-Requests](https://github.com/O-X-L/dnsbl-checker/pulls) for
  * improving and/or extending the Unit-Tests
  * improving Performance
  * fixing bugs
* or contact us directly: [contact+dnsblcheck@oxl.at](mailto://contact+dnsblcheck@oxl.at)

----

## Guidelines

* Please do not post any generic AI-slop.. thanks.
* Be friendly and respectful

----

## Development

* First install the DEV-Dependencies - a VENV is recommended:

  ```bash
  pip install -r requirements.txt
  pip install -r requirements_lint.txt
  pip install -r requirements_test.txt
  pip install -r requirements_build.txt
  ```

* To try out your local changes you can easily execute the CLI: `python3 src/dnsbl_check --help`

* Changes need to be covered by unit-tests. (`src/dnsbl_check/test_*.py` files)

  To run them: `make test` or `bash scripts/test.sh`

  Tests should not depend on DNS responses as we cannot impact their result!

* Also make sure to run the linter:

  To run them: `make lint` or `bash scripts/lint.sh`

* If you add DNS-BL providers - also add them to the [Providers.md](https://github.com/O-X-L/dnsbl-checker/blob/latest/Providers.md) with useful comments and links.

----

## Debug

To enable the debug-mode - set the env-var 'DEV=1'.

Example: `DEV=1 python3 src/dnsbl_check -i 134.209.173.54`

It will:
* Throw exceptions on `general_errors`
* Dump aidns responses to `/tmp/dnsbl_*`
