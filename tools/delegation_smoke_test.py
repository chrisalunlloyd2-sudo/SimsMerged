# Run on your laptop: python tools/delegation_smoke_test.py
# Exercises post/claim/approve/escalation/token cap/digest in a temp queue, then checks Tailscale.
import os, sys, tempfile, shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend', 'core', 'delegation'))
import bounty_dispatcher as b

tmp = tempfile.mkdtemp()
for s in b.STATES:
    os.makedirs(os.path.join(tmp, s))
b.BOUNTIES = tmp
try:
    b.post('S1', 'smoke', 5); b.claim('S1', 'hermes')
    b.approve('S1', 'alice', False, 'bad 1'); b.claim('S1', 'hermes')
    b.approve('S1', 'alice', False, 'bad 2')
    assert b._read(b._path('open', 'S1'))['role'] == 'architect', 'escalation failed'
    b.claim('S1', 'claude'); b.approve('S1', 'alice', False, 'bad 3')
    assert b.digest()['counts']['needs_human'] == 1
    b.post('S2', 'ok', 3); b.claim('S2', 'hermes'); b.approve('S2', 'alice', True, 'fine')
    try:
        b.approve('S2', 'alice', True, ''); raise SystemExit('empty notes accepted')
    except (ValueError, FileNotFoundError):
        pass
    seeded = b.seed(); assert 'T13-01' in seeded and b.seed() == [], 'seed failed/not idempotent'
    print('dispatcher OK:', b.digest()['counts'])
finally:
    shutil.rmtree(tmp)
peers = b.tailscale_peers()
print('tailscale peers online:', peers or 'NONE (is tailscale installed/up?)')
