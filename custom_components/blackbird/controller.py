import json
from collections import OrderedDict
from typing import Dict, Optional

import requests


class Controller:
    """Python Interface for the Switcher"""

    def __init__(self, host: str) -> None:
        self._host: str = host
        self._id = None
        self._name = None
        self._current_input = None
        self._input_to_command: Optional[Dict[str, str]] = None

    @property
    def id(self):
        if not self._id:
            self.refresh()

        return self._id

    @property
    def name(self):
        if not self._name:
            self.refresh()

        return self._name

    @property
    def current_input(self):
        return self._current_input

    def refresh(self) -> None:
        response = requests.post(f"http://{self._host}/cgi-bin/MUH44TP_getsetparams.cgi", data="{tag:ptn}")
        response_json = json.loads(response.text[1:-1].replace("'", "\""))

        self._id = response_json['MacAddr'].replace(" ", "")
        self._name = response_json['Output8Table']

        self._input_to_command = OrderedDict()
        self._input_to_command[response_json["Output1Table"]] = "HDMI1"
        self._input_to_command[response_json["Output2Table"]] = "HDMI2"
        self._input_to_command[response_json["Output3Table"]] = "HDMI3"
        self._input_to_command[response_json["Output4Table"]] = "HDMI4"

        self._current_input = self._input_to_command.values()[response_json['Outputbuttom']]

    def set_input(self, input_name: str) -> None:
        if not self._input_to_command:
            self.refresh()

        self.__send_command(self._input_to_command[input_name])

    def turn_on_display(self) -> None:
        self.__send_command("TVON")

    def turn_off_display(self) -> None:
        self.__send_command("TVOFF")

    def increase_volume(self) -> None:
        self.__send_command("TVVOL")

    def decrease_volume(self) -> None:
        self.__send_command("TVVOL-")

    def mute_volume(self) -> None:
        self.__send_command("TVMUTE")

    def __send_command(self, command: str):
        return requests.post(f"http://{self._host}/cgi-bin/MMX32_Keyvalue.cgi", data=f"{{CMD={command}.")
