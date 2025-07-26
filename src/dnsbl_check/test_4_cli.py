from time import time
from pathlib import Path
from os import system as shell
from json import loads as json_loads

from oxl_utils.ps import process

PATH_REPO = Path(__file__).parent.parent.parent
PATH_VENV = Path('/tmp') / f'dnsbl_test_venv_{int(time())}'
PATH_VENV_BIN = PATH_VENV / 'bin' / 'activate'


def test_cli_prep():
    rc_venv = shell(f'python3 -m virtualenv {PATH_VENV}')
    assert rc_venv == 0
    rc_pip_install = shell(f'/bin/bash -c "source {PATH_VENV_BIN} && python3 -m pip install -e {PATH_REPO}"')
    assert rc_pip_install == 0


def _cli_cmd(cmd: str) -> dict:
    return process(
        f'/bin/bash -c "source {PATH_VENV_BIN} && dnsbl-check {cmd}"',
        shell=True,
    )


def test_cli_base():
    r = _cli_cmd('--help')
    assert r['stderr'] is None
    assert r['rc'] == 0
    assert 'usage: DNS-BL Lookup-Client' in r['stdout']


def test_cli_check_ip():
    r = _cli_cmd('--ip=1.1.1.1 --json')
    assert r['stderr'] is None
    assert r['rc'] == 0
    r = json_loads(r['stdout'])
    assert 'detected' in r
    assert 'detected_by' in r
    assert 'categories' in r
    assert 'general_errors' in r
    assert len(r['general_errors']) == 0
    assert 'count' in r
    assert 'detected' in r['count']
    assert 'checked' in r['count']
    assert 'failed' in r['count']


def test_cli_check_domain():
    r = _cli_cmd('--domain=risk.oxl.app --json')
    assert r['stderr'] is None
    assert r['rc'] == 0
    r = json_loads(r['stdout'])
    assert 'detected' in r
    assert 'detected_by' in r
    assert 'categories' in r
    assert 'general_errors' in r
    assert len(r['general_errors']) == 0
    assert 'count' in r
    assert 'detected' in r['count']
    assert 'checked' in r['count']
    assert 'failed' in r['count']


def test_cli_details():
    r = _cli_cmd('--ip=1.1.1.1 --json --details')
    assert r['stderr'] is None
    assert r['rc'] == 0
    r = json_loads(r['stdout'])
    assert 'detected' in r
    assert 'detected_by' in r
    assert 'categories' in r
    assert 'general_errors' in r
    assert len(r['general_errors']) == 0
    assert 'count' in r
    assert 'detected' in r['count']
    assert 'checked' in r['count']
    assert 'failed' in r['count']
    assert 'detected_provider_categories' in r
    assert 'checked_providers' in r
    assert 'failed_providers' in r
