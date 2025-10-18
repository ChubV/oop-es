from oop_bus import EventBus

from oop_es.store import EventStore
from .wallet import Wallet
from oop_es.repository import SimpleAggregateRepository


class WalletRepository(SimpleAggregateRepository[Wallet]):
    def __init__(self, store: EventStore, event_bus: EventBus):
        super().__init__(store, event_bus, Wallet)