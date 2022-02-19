import asyncio
import json
from collections import OrderedDict
from typing import Dict, Optional, List

import aiohttp


class Controller:
    """Python Interface for the Switcher"""

    def __init__(self, host: str) -> None:
        self._host: str = host
        self._id = None
        self._name = None
        self._current_input = None
        self._input_to_command: Optional[Dict[str, str]] = None

    @property
    def id(self) -> Optional[str]:
        return self._id

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def current_input(self) -> Optional[str]:
        return self._current_input

    @property
    def input_sources(self) -> Optional[List[str]]:
        if not self._input_to_command:
            return None
        return list(self._input_to_command.keys())

    async def refresh(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"http://{self._host}/cgi-bin/MUH44TP_getsetparams.cgi",
                                    data="{tag:ptn}") as response:
                response_text = await response.text()
                response_json = json.loads(response_text.strip()[1:-1].replace("'", "\""))

                self._id = response_json['MacAddr'].replace(" ", "")
                self._name = response_json['Output8Table']

                self._input_to_command = OrderedDict()
                self._input_to_command[response_json["Output1Table"]] = "HDMI1"
                self._input_to_command[response_json["Output2Table"]] = "HDMI2"
                self._input_to_command[response_json["Output3Table"]] = "HDMI3"
                self._input_to_command[response_json["Output4Table"]] = "HDMI4"

                self._current_input = list(self._input_to_command.keys())[int(response_json['Outputbuttom']) - 1]

    async def set_input(self, input_name: str) -> None:
        if not self._input_to_command:
            await self.refresh()

        await self.__send_command(self._input_to_command[input_name])

    async def turn_on_display(self) -> None:
        await self.__send_command("TVON")

    async def turn_off_display(self) -> None:
        await self.__send_command("TVOFF")

    async def increase_volume(self) -> None:
        await self.__send_command("TVVOL")

    async def decrease_volume(self) -> None:
        await self.__send_command("TVVOL-")

    async def mute_volume(self) -> None:
        await self.__send_command("TVMUTE")

    async def __send_command(self, command: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"http://{self._host}/cgi-bin/MMX32_Keyvalue.cgi",
                                    data=f"{{CMD={command}.") as response:
                return response


if __name__ == '__main__':
    async def main():
        controller = Controller("192.168.0.220")
        await controller.refresh()
        controller_id, controller_name, controller_input = controller.id, controller.name, controller.current_input
        print(controller_id, controller_name, controller_input)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
