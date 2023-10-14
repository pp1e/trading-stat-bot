from dataclasses import dataclass
from datetime import date
from typing import BinaryIO


@dataclass
class WeekStat:
    monday_date: date
    week_profit: float
    week_profit_percents: float
    overall_balance: float
    profit: float
    profit_percents: float
    user_overall_profits: dict
    user_week_profits: dict
    user_balances: dict
    screenshot: BinaryIO
    week_number: int
