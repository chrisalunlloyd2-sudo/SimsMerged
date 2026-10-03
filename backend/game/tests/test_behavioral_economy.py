from backend.game.behavioral_economy import *


def test_nocturnal_window():
    assert is_nocturnal(23) and is_nocturnal(3) and not is_nocturnal(12)


def test_reward_and_penalties():
    assert score_behavior(Behavior("a", True, True, hour=22)) == 10.0
    assert score_behavior(Behavior("a", True, False, hour=22)) == 2.0
    assert score_behavior(Behavior("a", True, True, hour=12)) == 6.0
    assert score_behavior(Behavior("a", ram_mb=100, hour=22)) == -5.0


def test_hot_host_throttles_reward():
    hot = HostTelemetry(100, 100, 0)
    assert score_behavior(Behavior("a", True, True, hour=22), hot) == 5.0


def test_negotiation_respects_budget():
    t = HostTelemetry(20, 10, 0)
    g = negotiate_resources({"a": 0.6, "b": 0.6}, t)
    assert sum(g.values()) <= 0.5 + 1e-6
    assert negotiate_resources({"a": 1}, HostTelemetry(100, 100, 0)) == {"a": 0.0}


def test_treasury_floor_and_hud():
    tp = TreasuryPoints()
    tp.apply("a", 5, "x"); tp.apply("a", -50, "y")
    assert tp.balances["a"] == 0.0
    snap = hud_snapshot(tp, HostTelemetry(10, 10, 0), 22)
    assert snap["nocturnal"] and snap["leaderboard"][0]["agent"] == "a"
