from typing import List

from oop_es.store import EventStore
from oop_es.view import Projector
from .wallet import Wallet
from oop_es.repository import SimpleAggregateRepository


class WalletRepository(SimpleAggregateRepository[Wallet]):
    def __init__(self, store: EventStore, projectors: List[Projector]):
        super().__init__(store, projectors, Wallet)