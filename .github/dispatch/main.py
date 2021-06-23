#!/usr/bin/env python3
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
        plan = Plan().set_labels(envPR)
        return plan

    def set_labels(self, envPR: dict) -> Plan:
        self.ctx.pr.labels = [label['name'] for label in envPR['labels']]
        return self

    def output(self) -> str:
        ctx = json.dumps(asdict(self.ctx))
        topics = json.dumps(self.topics)
        print(f"::set-output name=ctx::{ctx}")
        print(f"::set-output name=topics::{topics}")

    def dispatch(self) -> None:
        # simple dispatch strategy: passthrough labels
        self.topics = self.ctx.pr.labels

        self.output()


if __name__ == '__main__':
    Plan.from_env().dispatch()
