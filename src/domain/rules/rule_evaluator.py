from ...domain.assets.asset import Asset
from ...domain.assets.asset_type import AssetType
from ..events.domain_event import DomainEvent


class RuleEvaluator:
    def evaluate(self, domain_event: DomainEvent) -> None:
        asset: Asset = domain_event.asset
        asset_type: AssetType = asset.asset_type

        for rule in asset_type.rules:
            if not isinstance(domain_event, rule.trigger.trigger_event):
                continue

            if not rule.condition.evaluate(asset):
                continue

            asset.transition(rule.action.transition_to)

            break
