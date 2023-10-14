import enum


class BotCommands(enum.Enum):
    START = 'start'
    VIEW_LAST_STATISTIC = 'view_last_statistic'
    VIEW_SPECIFIED_STATISTIC = 'view_specified_statistic'
    INTERACT_WITH_DEPOSIT = 'interact_with_deposit'
    ADD_DEPOSIT = 'add_deposit'
    WITHDRAW_MONEY = 'withdraw_money'
    TO_START = 'to_start'
    SELECT_USER = 'select_user'
    VIEW_USER_DEPOSITS = 'view_user_deposits'
