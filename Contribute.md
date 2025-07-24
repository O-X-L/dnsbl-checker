# Contribute

Contributions are welcome (:

If you have ideas on how to improve the project feel free to:
* [report Issues](https://github.com/O-X-L/dnsbl-checker/issues)
* [request Features](https://github.com/O-X-L/dnsbl-checker/issues) (*like additional base-lists*)
* [Discuss about the implementation](https://github.com/O-X-L/dnsbl-checker/discussions)
* [create Pull-Requests](https://github.com/O-X-L/dnsbl-checker/pulls) for
  * improving and/or extending the Unit-Tests
  * improving Performance
  * fixing bugs
* or contact us directly: [contact+dnsblcheck@oxl.at](mailto://contact+dnsblcheck@oxl.at)

## Guidelines

* Please do not post any generic AI-slop.. thanks.
* Be friendly and respectful

## Debug

To enable the debug-mode - set the env-var 'DEV=1'.

Example: `DEV=1 python3 src/dnsbl_check -i 134.209.173.54`

It will:
* Throw exceptions on `general_errors`
* Dump aidns responses to `/tmp/dnsbl_*`
