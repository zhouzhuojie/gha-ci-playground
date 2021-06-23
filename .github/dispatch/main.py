from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field


@dataclass
class PR:
    labels: list[str] = field(default_factory=list)


@dataclass
class PlanContext:
    pr: PR = field(default_factory=PR)


@dataclass
class Plan:
    ctx: PlanContext = field(default_factory=PlanContext)
    topics: list[str] = field(default_factory=list)

    @classmethod
    def from_env(cls) -> Plan:
        envPR = json.loads(os.getenv('PR', '{}'))
        plan = Plan()
        plan.ctx.pr.labels = envPR.get('labels', [])
        return plan

    def output(self) -> str:
        print(f"::set-output name=ctx::{json.dumps(asdict(self.ctx))}")
        print(f"::set-output name=topics::{json.dumps(self.topics)}")

    def dispatch(self) -> None:
        # simple passthrough to generate the labels
        self.topics = self.ctx.pr.labels
        self.output()


if __name__ == '__main__':
    Plan.from_env().dispatch()
