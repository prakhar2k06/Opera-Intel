from collections import deque

from ...domain.assets.asset import Asset
from ...domain.events.domain_event import DomainEvent
from ...domain.rules.rule_evaluator import RuleEvaluator


class DomainEventProcessor:
    def __init__(self) -> None:
        self.rule_evaluator = RuleEvaluator()

    def process_events(self, asset: Asset) -> None:
        domain_events: list[DomainEvent] = asset.pull_domain_events()

        if not domain_events:
            return

        queue: deque[DomainEvent] = deque(domain_events)

        while queue:
            event: DomainEvent = queue.popleft()
            self.rule_evaluator.evaluate(event)

            domain_events: list[DomainEvent] = asset.pull_domain_events()

            if domain_events:
                queue.extend(domain_events)
