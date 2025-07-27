from idna import encode as idna_encode

from config import DOMAIN_REGEX


def valid_domain(v: str) -> tuple[str, bool]:
    v = idna_encode(v.lower()).decode()
    return v, DOMAIN_REGEX.match(v) is not None
