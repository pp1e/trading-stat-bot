import enum


class BotCommands(enum.Enum):
    START = 'start'
    VIEW_STATISTIC = 'view_statistic'
    VIEW_ACTUAL_STATISTIC = 'view_actual_statistic'
    VIEW_SPECIFIED_STATISTIC = 'view_specified_statistic'
    INTERACT_WITH_DEPOSIT = 'interact_with_deposit'
    ADD_DEPOSIT = 'add_deposit'
    WITHDRAW_MONEY = 'withdraw_money'
    TO_START = 'to_start'
    SELECT_USER = 'select_user'
    VIEW_AVERAGE_PURCHASE_DOLLAR_PRICE = 'view_average_purchase_dollar_price'
