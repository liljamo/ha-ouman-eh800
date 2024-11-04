"""TODO"""

import logging
import requests

_LOGGER = logging.getLogger(__name__)


class EH800:
    """TODO"""

    def __init__(self, host: str, port: int, username: str, password: str) -> None:
        """TODO"""
        self._uri = f"http://{host}:{port}"
        self._login = f"uid={username};pwd={password};"

        self._outside_temp = 0.0
        self._l1_room_temp = 0.0
        self._l1_supply_temp = 0.0

    def _refresh_login(self) -> bool:
        """TODO"""
        r = requests.get(f"{self._uri}/login?{self._login}")

        if r.text[:-1] == "login?result=ok;":
            _LOGGER.debug("Login ok")
            return True

        _LOGGER.debug("Login error")
        return False

    def _request_value(self, register) -> str:
        """TODO"""
        if not self._refresh_login():
            return ""

        r = requests.get(f"{self._uri}/request?{register}")
        eq_index = r.text.find("=")
        sc_index = r.text.find(";")
        return r.text[eq_index + 1 : sc_index]

    def get_outside_temp(self) -> float:
        """TODO"""
        return self._outside_temp

    def update_outside_temp(self):
        """TODO"""
        self._outside_temp = self._request_value("S_227_85")

    def get_l1_room_temp(self) -> float:
        """TODO"""
        return self._l1_room_temp

    def update_l1_room_temp(self):
        """TODO"""
        self._l1_room_temp = self._request_value("S_261_85")

    def get_l1_supply_temp(self) -> float:
        """TODO"""
        return self._l1_supply_temp

    def update_l1_supply_temp(self):
        """TODO"""
        self._l1_supply_temp = self._request_value("S_259_85")
