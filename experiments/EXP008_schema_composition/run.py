"""Run EXP008 and write a compact, append-only scientific event log."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from perspective_dynamics.schema_composition import SchemaCompositionEngine, demo_world

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    world, schemas, goal = demo_world()
    engine = SchemaCompositionEngine(schemas)
    cases = (("compose", None), ("single", ("support",)), ("pool", None))
    events = []
    for mode, perspectives in cases:
        result = engine.solve(world, goal, mode=mode, perspectives=perspectives)
        events.append({
            "date": str(date.today()), "experiment": "EXP008", "mode": mode,
            "perspectives": perspectives, "success": result.success,
            "explored_states": result.explored_states, "reason": result.reason,
            "plan": [{"schema": step.schema, "perspective": step.perspective,
                      "action": step.action, "produced": step.produced,
                      "enabled_by": step.enabled_by} for step in result.steps],
        })
    (RESULTS / "events.jsonl").write_text(
        "".join(json.dumps(event, sort_keys=True) + "\n" for event in events), encoding="utf-8"
    )
    summary = {
        "experiment": "EXP008", "hypothesis": "H8.1-H8.3", "cases": events,
        "structured_composition_success": events[0]["success"],
        "single_and_pool_fail": not events[1]["success"] and not events[2]["success"],
        "claim_boundary": "synthetic Level 1 implementation check; not neural or biological evidence",
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
