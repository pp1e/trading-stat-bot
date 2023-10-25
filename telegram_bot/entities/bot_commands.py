import enum


class BotCommands(enum.Enum):
    START = 'start'
    VIEW_STATISTIC = 'view_statistic'
    VIEW_ACTUAL_STATISTIC = 'view_actual_statistic'
    VIEW_SPECIFIED_STATISTIC = 'view_specified_statistic'
    VIEW_DEPOSIT_STATISTIC = 'view_deposit_statistic'
    INTERACT_WITH_DEPOSIT = 'interact_with_deposit'
    ADD_DEPOSIT = 'add_deposit'
    WITHDRAW_MONEY = 'withdraw_money'
    TO_START = 'to_start'
    SELECT_USER = 'select_user'
