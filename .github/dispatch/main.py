from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict


@dataclass
class PR:
    labels: list[str]


@dataclass
class PlanContext:
    pr: PR


@dataclass
class Plan:
    ctx: PlanContext
    topics: list[str]

    @classmethod
    def from_env(cls) -> Plan:
        pr = json.load(os.getenv('PR', '{}'))
        plan = Plan()
        plan.ctx = PlanContext
        plan.ctx.pr = pr
        return plan

    def output(self) -> str:
        print(f"::set-output name=ctx::{json.dumps(asdict(self.ctx))}")
        print(f"::set-output name=topics::{json.dumps(asdict(self.topics))}")

    def dispatch(self) -> None:
        # simple passthrough to generate the labels
        self.topics = self.ctx.pr['labels']
        self.output()


if __name__ == '__main__':
    Plan.from_env().dispatch()
