from typing import Type
from uuid import UUID, uuid4

from .wallet import Wallet
from .wallet_repository import WalletRepository
from oop_es.command.command import Command
from oop_es.command.command_handler import CommandHandler


class OpenWallet(Command):
    def __init__(self, name: str):
        self.name = name
        self.uuid: UUID = uuid4()

    def set_uuid(self, uuid):
        self.uuid = uuid


class OpenWalletHandler(CommandHandler[OpenWallet]):
    def __init__(self, wallet_repository: WalletRepository):
        self.wallet_repository = wallet_repository

    def command_type(self) -> Type[OpenWallet]:
        return OpenWallet

    async def handle(self, command: OpenWallet) -> None:
        name = command.name
        print(f"Opening wallet {name}")
        wallet = Wallet.create(name)
        await self.wallet_repository.save(wallet)

        command.set_uuid(wallet.uuid)


class MoveMoney(Command):
    def __init__(self, uuid: UUID, amount: int):
        self.uuid = uuid
        self.amount = amount
        self.new_amound = 0

    def set_new_amount(self, new_amount: int):
        self.new_amount = new_amount


class DepositMoney(MoveMoney):
    ...


class WithdrawMoney(MoveMoney):
    ...


class DepositMoneyHandler(CommandHandler[DepositMoney]):
    def __init__(self, wallet_repository: WalletRepository):
        self.wallet_repository = wallet_repository

    def command_type(self) -> Type[DepositMoney]:
        return DepositMoney

    async def handle(self, command: DepositMoney) -> None:
        uuid = command.uuid
        print(f"Loading wallet {str(uuid)}")
        wallet = await self.wallet_repository.load(uuid)
        print(f"Wallet loaded with amount {wallet.amount}")
        wallet.deposit(command.amount)
        print(f"New amount {wallet.amount}")
        await self.wallet_repository.save(wallet)
        command.set_new_amount(command.amount)


class WithdrawMoneyHandler(CommandHandler[WithdrawMoney]):
    def __init__(self, wallet_repository: WalletRepository):
        self.wallet_repository = wallet_repository

    def command_type(self) -> Type[WithdrawMoney]:
        return WithdrawMoney

    async def handle(self, command: WithdrawMoney) -> None:
        uuid = command.uuid
        print(f"Loading wallet {str(uuid)}")
        wallet = await self.wallet_repository.load(uuid)
        print(f"Wallet loaded with amount {wallet.amount}")
        wallet.withdraw(command.amount)
        print(f"New amount {wallet.amount}")
        await self.wallet_repository.save(wallet)
        command.set_new_amount(command.amount)