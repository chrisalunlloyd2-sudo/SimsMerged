# TIMESTAMP: 2026-10-03
# PROJECT_ID: SimsMerged-v1.4.3
# AGENT_ID: copilot-delegation
# DESCRIPTION: File-based bounty queue. Post -> claim (atomic) -> submit -> critic approve/payout.
# Local-only: no external APIs. Nodes are addressed by Tailscale MagicDNS names from nodes.json.

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
BOUNTIES = os.path.join(ROOT, 'bounties')
PROJECT_ID = 'SimsMerged-v1.4.3'
STATES = ('open', 'claimed', 'done')


def _log(agent, msg):
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[{ts}] [{PROJECT_ID}] [{agent}] {msg}")


def _path(state, bounty_id):
    return os.path.join(BOUNTIES, state, f"{bounty_id}.json")


def _read(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def _write(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def load_nodes():
    return _read(os.path.join(ROOT, 'nodes.json'))


def post(bounty_id, description, reward, role='developer'):
    data = {'id': bounty_id, 'description': description, 'reward': reward,
            'role': role, 'status': 'open', 'created': time.time()}
    p = _path('open', bounty_id)
    if os.path.exists(p):
        raise FileExistsError(bounty_id)
    _write(p, data)
    _log('dispatcher', f"posted {bounty_id} reward={reward} role={role}")


def claim(bounty_id, agent):
    """Atomic claim: os.rename fails if another agent already moved the file."""
    src, dst = _path('open', bounty_id), _path('claimed', bounty_id)
    os.rename(src, dst)
    data = _read(dst)
    data.update(status='claimed', agent=agent, claimed_at=time.time())
    _write(dst, data)
    _log(agent, f"claimed {bounty_id}")
    return data


def next_open(role):
    for name in sorted(os.listdir(os.path.join(BOUNTIES, 'open'))):
        if name.endswith('.json'):
            data = _read(os.path.join(BOUNTIES, 'open', name))
            if data.get('role') == role:
                return data['id']
    return None


def _usage_path():
    return os.path.join(BOUNTIES, 'usage.json')


def record_tokens(agent, tokens):
    """Add to today's usage; raises if the agent's daily cap would be exceeded."""
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    path = _usage_path()
    usage = _read(path) if os.path.exists(path) else {}
    if usage.get('date') != today:
        usage = {'date': today}
    cap = load_nodes().get('daily_token_cap', {}).get(agent)
    used = usage.get(agent, 0)
    if cap is not None and used + tokens > cap:
        raise RuntimeError(f"{agent} daily token cap {cap} exceeded (used {used}, +{tokens})")
    usage[agent] = used + tokens
    _write(path, usage)
    return usage[agent]


def approve(bounty_id, critic, approved, notes='', ledger=None):
    """Critic review gate; payout only when approved, otherwise re-open.

    ledger: optional object with fund_wallet(agent_id, amount) (e.g. DePINLedger).
    """
    src = _path('claimed', bounty_id)
    data = _read(src)
    if data.get('agent') == critic:
        raise PermissionError('critic cannot approve own work')
    if approved:
        data.update(status='done', approved_by=critic, notes=notes, paid=data['reward'])
        if ledger is not None:
            data['tx_hash'] = ledger.fund_wallet(data['agent'], data['reward'])
        _write(_path('done', bounty_id), data)
        os.remove(src)
        _log(critic, f"approved {bounty_id}; payout {data['reward']} to {data['agent']}")
    else:
        data.update(status='open', notes=notes)
        data.pop('agent', None)
        _write(_path('open', bounty_id), data)
        os.remove(src)
        _log(critic, f"rejected {bounty_id}; re-opened")
    return data


def tailscale_peers():
    """Return online tailnet peer DNS names, or [] if tailscale is unavailable."""
    if not shutil.which('tailscale'):
        return []
    try:
        out = subprocess.run(['tailscale', 'status', '--json'], capture_output=True,
                             text=True, timeout=10, check=True).stdout
        peers = json.loads(out).get('Peer', {}).values()
        return [p['DNSName'].rstrip('.') for p in peers if p.get('Online')]
    except (subprocess.SubprocessError, ValueError, KeyError):
        return []


def ollama_url(node):
    n = load_nodes()['nodes'][node]
    return f"http://{n['host']}:{n['ollama_port']}"


def digest():
    counts = {s: len([f for f in os.listdir(os.path.join(BOUNTIES, s)) if f.endswith('.json')])
              for s in STATES}
    paid = sum(_read(_path('done', f[:-5])).get('paid', 0)
               for f in os.listdir(os.path.join(BOUNTIES, 'done')) if f.endswith('.json'))
    return {'counts': counts, 'total_paid': paid, 'online_peers': tailscale_peers()}


def write_digest():
    """Write the morning digest to bounties/DIGEST.md and return its path."""
    d = digest()
    path = os.path.join(BOUNTIES, 'DIGEST.md')
    lines = [f"# Morning Digest {datetime.now(timezone.utc).isoformat()}", '',
             f"- open: {d['counts']['open']}", f"- claimed: {d['counts']['claimed']}",
             f"- done: {d['counts']['done']}", f"- total paid: {d['total_paid']}",
             f"- online peers: {', '.join(d['online_peers']) or 'none'}"]
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    return path


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'digest'
    if cmd == 'post':
        post(sys.argv[2], sys.argv[3], int(sys.argv[4]), *(sys.argv[5:6]))
    elif cmd == 'claim':
        claim(sys.argv[2], sys.argv[3])
    elif cmd == 'approve':
        approve(sys.argv[2], sys.argv[3], sys.argv[4] == 'yes', *(sys.argv[5:6]))
    elif cmd == 'tokens':
        print(record_tokens(sys.argv[2], int(sys.argv[3])))
    elif cmd == 'digest-file':
        print(write_digest())
    else:
        print(json.dumps(digest(), indent=2))
