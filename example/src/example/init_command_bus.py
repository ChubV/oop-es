from oop_bus import EventBus

from .handlers import DepositMoneyHandler, OpenWalletHandler, WithdrawMoneyHandler
from .wallet_repository import WalletRepository
from oop_es.command import StandardCommandBus
from oop_es.store import InMemoryEventStore


def init_command_bus():
    command_bus = StandardCommandBus()
    wallet_repository = WalletRepository(InMemoryEventStore(), EventBus())
    command_bus.subscribe(OpenWalletHandler(wallet_repository))
    command_bus.subscribe(WithdrawMoneyHandler(wallet_repository))
    command_bus.subscribe(DepositMoneyHandler(wallet_repository))

    return command_bus