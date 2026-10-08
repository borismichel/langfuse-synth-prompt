"""Process-order regression gate for the pinned older authoring core."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys


def test_seed_repeatable_across_process_hash_seeds():
    script = '''from langfuse_synth_core.authoring.egress import install_guard
install_guard()
import socket
socket.socket.connect = lambda *a, **k: (_ for _ in ()).throw(RuntimeError('No seed network'))
from golden_seed import seed
import hashlib
print(hashlib.sha256(seed(24, {})).hexdigest())
'''
    digests = []
    for hash_seed in ('0','1','2'):
        env = {k:v for k,v in os.environ.items() if not any(s in k for s in ('KEY','TOKEN','SECRET','PASSWORD'))}
        env.update(PYTHONHASHSEED=hash_seed,PYTHONPATH=os.pathsep.join([str(Path('src').resolve()),str(Path('tests').resolve())]))
        process=subprocess.run([sys.executable,'-c',script],env=env,capture_output=True,text=True,check=True)
        digests.append(process.stdout.strip())
    assert len(set(digests)) == 1, 'Seed output changes across Python hash seeds'
    expected=hashlib.sha256(Path('tests/golden/prompt_spool.ndjson').read_bytes()).hexdigest()
    assert digests==[expected]*3


def test_declared_seed_and_date_parameters_are_applied():
    from golden_seed import seed
    baseline=seed(1,{})
    assert seed(1,{'seed':7})!=baseline
    assert seed(1,{'as_of_date':'2026-03-30'})!=baseline
    import pytest
    with pytest.raises(ValueError): seed(1,{'unknown':1})
    with pytest.raises(ValueError): seed(1,{'seed':1,'generation.seed':1})
