from abc import ABC, abstractmethod

from oop_es.command.command import Command
from oop_es.command.command_handler import CommandHandler


class CommandBus(ABC):
    @abstractmethod
    def subscribe(self, handler: CommandHandler):
        ...

    @abstractmethod
    async def handle(self, command: Command):
        ...


class StandardCommandBus(CommandBus):
    def __init__(self):
        self.handlers = {}
        self.handling = False
        self.queue = []

    def subscribe(self, handler: CommandHandler):
        self.handlers[handler.command_type().__name__] = handler

    async def handle(self, command: Command):
        self.queue.append(command)

        if self.handling:
            return

        self.handling = True

        while self.queue:
            await self._handle_command(self.queue.pop(0))

        self.handling = False

    async def _handle_command(self, command: Command):
        try:
            handler = self.handlers[command.__class__.__name__]
        except KeyError:
            return

        await handler.handle(command)
