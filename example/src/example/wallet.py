from uuid import UUID

from oop_es import AggregateRoot, Event


class WalletOpened(Event):
    def __init__(self, uuid: UUID, name: str):
        self.uuid = uuid
        self.name = name


class MoneyDeposited(Event):
    def __init__(self, uuid: UUID, amount: int):
        self.uuid = uuid
        self.amount = amount


class MoneyWithdrawn(Event):
    def __init__(self, uuid: UUID, amount: int):
        self.uuid = uuid
        self.amount = amount


class NotEnoughMoney(Exception):
    ...


class Wallet(AggregateRoot):
    def __init__(self, uuid: UUID | None = None):
        super().__init__(uuid)
        self.name = "Default"
        self.amount = 0

    @classmethod
    def create(cls, name: str):
        wallet = Wallet()
        wallet.open(name)

        return wallet

    def open(self, name: str):
        self.apply(WalletOpened(self.uuid, name))

    def deposit(self, amount: int):
        self.apply(MoneyDeposited(self.uuid, amount))

    def withdraw(self, amount: int):
        self.apply(MoneyWithdrawn(self.uuid, amount))

    def apply_wallet_opened(self, event: WalletOpened):
        self.name = event.name

    def apply_money_deposited(self, event: MoneyDeposited):
        self.amount += event.amount

    def apply_money_withdrawn(self, event: MoneyWithdrawn):
        if self.amount < event.amount:
            raise NotEnoughMoney()
        self.amount -= event.amount