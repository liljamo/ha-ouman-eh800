import dataclasses
import logging

from httpx import AsyncClient

_LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Value:
    key: str
    register: str


VALUES: tuple[Value, ...] = (
    # Asetusarvot > Menoveden minimiraja
    Value(key="l1_supply_temperature_minimum", register="S_54_85"),
    # Asetusarvot > Menoveden maksimiraja
    Value(key="l1_supply_temperature_maximum", register="S_55_85"),
    # Asetusarvot > L1 Säätökäyrä
    # n = negative, p = positive
    Value(key="l1_heating_curve_n_20", register="S_67_85"),
    Value(key="l1_heating_curve_n_10", register="S_69_85"),
    Value(key="l1_heating_curve_zero", register="S_71_85"),
    Value(key="l1_heating_curve_p_10", register="S_73_85"),
    Value(key="l1_heating_curve_p_20", register="S_75_85"),
    # Asetusarvot > Huonelämpötila
    Value(key="l1_target_room_temperature", register="S_81_85"),
    # Asetusarvot > Lämmönpudotus (huonelämpö)
    Value(key="l1_temperature_drop", register="S_87_85"),
    # Asetusarvot > Suuri lämmönpudotus (huonelämpö)
    Value(key="l1_temperature_drop_big", register="S_88_85"),
    # Ohjaustavat
    # 0 = Automaatti
    # 3 = Pakko-ohjaus, norm. lämpötaso
    # 1 = Pakko-ohjaus, lämmönpudotus
    # 2 = Pakko-ohjaus, suuri lämmönpudotus
    # 6 = Käsiajo, sähköinen
    # 5 = Alasajo
    Value(key="l1_operation_mode", register="S_59_85"),
    Value(key="l1_manual_drive_valve_position", register="S_92_85"),
    # Mittaukset > Ulkolämpötila
    Value(key="outside_temperature", register="S_227_85"),
    # Mittaukset > L1 Menoveden lämpötila
    Value(key="l1_supply_temperature", register="S_259_85"),
    # Mittaukset > L1 Huonelämpötila
    Value(key="l1_room_temperature", register="S_284_85"),
    # Mittaukset > Huonelämpökaukoasetus TMR/SP
    Value(key="l1_tmrsp", register="S_274_85"),
    # Mittaukset > L1 Venttiilin asento
    Value(key="l1_valve_position", register="S_272_85"),
    # EH-800 > Huonelämpötila
    Value(key="room_temperature", register="S_261_85"),
    # EH-800 > Huonelämpötilan hienosäätö
    Value(key="room_temperature_fine_adjustment", register="S_102_85"),
    # EH-800 > Lämpötaso:: (UI placement is strange)
    Value(key="l1_operation_mode_str", register="S_1000_0"),
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class OperationMode:
    name: str
    value: int


OPERATION_MODES: tuple[OperationMode, ...] = (
    OperationMode(name="Automatic", value=0),
    OperationMode(name="Forced - Normal", value=3),
    OperationMode(name="Forced - Drop", value=1),
    OperationMode(name="Forced - Big Drop", value=2),
    OperationMode(name="Manual", value=6),
    OperationMode(name="Off", value=5),
)


class EH800:
    def __init__(self, host: str, port: int, username: str, password: str) -> None:
        self._uri = f"http://{host}:{port}"
        self._login = f"uid={username};pwd={password};"

        self._client = AsyncClient()

        self._request_query = "request?"
        for value in VALUES:
            self._request_query += f"{value.register};"

        self.data = {}

    async def _refresh_login(self) -> bool:
        """
        Refresh login.

        Logs an error if the login failed.
        """
        r = await self._client.get(f"{self._uri}/login?{self._login}")

        if r.text[:-1] == "login?result=ok;":
            return True

        _LOGGER.error("Login error")
        return False

    async def _request_values(self) -> bool:
        """
        Request values from the API.
        """
        r = await self._client.get(f"{self._uri}/{self._request_query}")
        if r.status_code != 200:
            _LOGGER.error("unexpected return code %s", r.status_code)
            return False

        # Remove suffix and prefix so we end up with key=val pairs separated by
        # semicolons: key=val;key2=val;key3=val
        text = r.text.removeprefix("request?").removesuffix("\x00").removesuffix(";")
        pairs = text.split(";")
        for pair in pairs:
            kv = pair.split("=")
            # Only process those that returned something
            if len(kv) == 2:
                # Find the data key for the register
                data_key = [value.key for value in VALUES if value.register == kv[0]][0]
                self.data[data_key] = kv[1]
            else:
                _LOGGER.warning("register %s didn't return a value", str(kv[0]))

        return True

    async def _update_value(self, value: Value, new_value) -> None:
        """
        Update a value via the API.

        Checks the API return value and logs an error if the value update failed.
        """
        r = await self._client.get(f"{self._uri}/update?{value.register}={new_value};")
        eq_index = r.text.find("=")
        sc_index = r.text.find(";")
        got_value = r.text[eq_index + 1 : sc_index]
        if str(got_value) != str(new_value):
            _LOGGER.error(
                "Value update failed, got '%s', wanted '%s'", got_value, new_value
            )
        else:
            # Update data to match the new value
            self.data[value.key] = new_value

    async def update(self) -> bool:
        """Update data values from the API."""
        if not await self._refresh_login():
            return False

        if not await self._request_values():
            return False

        return True

    async def update_value(self, key, new_value) -> None:
        """Update a value via the API."""
        value = [value for value in VALUES if value.key == key][0]
        _LOGGER.debug(
            "Updating '%s' (%s) to '%s'", value.key, value.register, new_value
        )
        await self._update_value(value, new_value)
