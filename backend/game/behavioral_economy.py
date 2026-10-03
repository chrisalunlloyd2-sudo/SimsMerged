# [TIMESTAMP: 2026-10-03] [PROJECT_ID: SimsMerged-v1.4.3] [AGENT_ID: copilot-game-logic]
# Phase 13: Treasury Point behavioral economy + host telemetry -> HUD snapshot.
# Pure logic, stdlib only, no I/O, so it is trivially testable and local-only.
#
# TODO markers: TODO(role:id) -> role is architect | developer | critic.
# Agents: turn each TODO into a bounty (see docs/AUTONOMY_WORKFLOW.md).

from dataclasses import dataclass, field
from typing import Dict, List, Optional

NOCTURNAL_START_HOUR = 20  # 8 PM
NOCTURNAL_END_HOUR = 8     # 8 AM
RAM_CAP_MB = 50.0          # DePIN cap per agent


def is_nocturnal(hour: int) -> bool:
    """Agents work 8 PM - 8 AM and sleep otherwise."""
    return hour >= NOCTURNAL_START_HOUR or hour < NOCTURNAL_END_HOUR


@dataclass
class HostTelemetry:
    cpu_percent: float  # 0-100
    io_percent: float   # 0-100
    ram_mb: float

    def load(self) -> float:
        """Blended host load in [0, 1]."""
        raw = (self.cpu_percent * 0.6 + self.io_percent * 0.4) / 100.0
        return max(0.0, min(1.0, raw))

    # TODO(developer:T13-01): replace manual construction with a real reader
    #   (registry/psutil on the Windows laptop). Must stay optional and fail soft.


@dataclass
class Behavior:
    agent_id: str
    task_completed: bool = False
    approved_by_critic: bool = False
    ram_mb: float = 0.0
    cpu_share: float = 0.0
    hour: int = 0
    rejections: int = 0


@dataclass
class TreasuryPoints:
    balances: Dict[str, float] = field(default_factory=dict)
    history: List[dict] = field(default_factory=list)

    def apply(self, agent_id: str, delta: float, reason: str) -> float:
        self.balances[agent_id] = max(0.0, self.balances.get(agent_id, 0.0) + delta)
        self.history.append({"agent": agent_id, "delta": delta, "reason": reason})
        return self.balances[agent_id]


def score_behavior(b: Behavior, telemetry: Optional[HostTelemetry] = None) -> float:
    """Return the Treasury Point delta for one agent tick."""
    score = 0.0
    if b.task_completed and b.approved_by_critic:
        score += 10.0
    elif b.task_completed:
        score += 2.0  # unreviewed work earns little
    score -= 3.0 * b.rejections
    if b.ram_mb > RAM_CAP_MB:
        score -= 5.0 * (b.ram_mb - RAM_CAP_MB) / RAM_CAP_MB  # DePIN cap breach
    if not is_nocturnal(b.hour) and (b.task_completed or b.cpu_share > 0):
        score -= 4.0  # working in daylight violates the Nocturnal Protocol
    if telemetry is not None and telemetry.load() > 0.5:
        score *= 1.0 - (telemetry.load() - 0.5)  # throttle rewards when host is hot (50% CPU rule)
    return round(score, 4)

    # TODO(architect:T13-02): decide the true reward curve (diminishing returns? streak bonus?)
    # TODO(critic:T13-03): review whether penalising daylight work double-counts with sleep logic


def negotiate_resources(requests: Dict[str, float], telemetry: HostTelemetry,
                        budget: float = 0.5) -> Dict[str, float]:
    """DePIN tick: split the spare CPU budget (default 50% cap) among agents.

    requests: agent_id -> desired CPU share (0-1). Returns granted shares, scaled
    proportionally so the total never exceeds the headroom left by the host.
    """
    headroom = max(0.0, budget - telemetry.load() * budget)
    total = sum(max(0.0, r) for r in requests.values())
    if total <= 0 or headroom <= 0:
        return {a: 0.0 for a in requests}
    scale = min(1.0, headroom / total)
    return {a: round(max(0.0, r) * scale, 4) for a, r in requests.items()}

    # TODO(developer:T13-04): weight grants by Treasury balance (rich agents get priority?)
    # TODO(architect:T13-05): add storage + RAM negotiation, not only CPU


def hud_snapshot(treasury: TreasuryPoints, telemetry: HostTelemetry, hour: int) -> dict:
    """Plain-dict payload for the JavaFX HUD. Add keys only, never rename (GUI safeguard)."""
    top = sorted(treasury.balances.items(), key=lambda kv: kv[1], reverse=True)[:5]
    return {
        "cpu_percent": telemetry.cpu_percent,
        "io_percent": telemetry.io_percent,
        "host_load": round(telemetry.load(), 4),
        "nocturnal": is_nocturnal(hour),
        "leaderboard": [{"agent": a, "points": p} for a, p in top],
    }

    # TODO(developer:T13-06): serve this over the existing gui_hooks.json channel
    # TODO(critic:T13-07): confirm no existing JavaFX field is removed or renamed
