import asyncio
from pathlib import Path

from oop_di import ContainerDefinition, JsonExtension

from example.wallet import NotEnoughMoney
from example.handlers import DepositMoney, OpenWallet, WithdrawMoney
# from example.init_command_bus import init_command_bus
from oop_es.command import CommandBus

container_definition = ContainerDefinition()
container_definition.add_extension(JsonExtension(Path(__file__).parent / "config.json"))
container = container_definition.compile()


@container.inject()
async def run(*, command_bus: CommandBus):
    open_command = OpenWallet("TEST")
    await command_bus.handle(open_command)
    uuid = open_command.uuid

    await command_bus.handle(DepositMoney(uuid, 1000))
    await command_bus.handle(DepositMoney(uuid, 500))
    await command_bus.handle(WithdrawMoney(uuid, 1000))

    try:
        await command_bus.handle(WithdrawMoney(uuid, 1000))
    except NotEnoughMoney:
        print("Failed to withdraw")


async def main():
    await run()
    # await run(command_bus=init_command_bus()) # init_command_bus inits it without dependency injection.

asyncio.run(main())
