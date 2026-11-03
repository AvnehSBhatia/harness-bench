"""line_net — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from billing_common import round_money, to_decimal, check_currency  # noqa: F401


def line_net(line: dict, currency: str) -> Decimal:
    """Net amount of one invoice line (SPEC 3.1).

    Round with ``billing_common.round_money`` (finance policy FIN-2, see TEAM_NOTES.md).
    """
    raise NotImplementedError
