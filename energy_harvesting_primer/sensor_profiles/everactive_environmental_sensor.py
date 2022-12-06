import abc
import os
from typing import Dict

SECONDS_IN_MIN = 60


class BaseSensorProfile(abc.ABC):
    """Base class representing a sensor."""

    @property
    @abc.abstractclassmethod
    def manufacturer(self) -> str:
        """Return string name of manufacturer."""
        pass

    @property
    @abc.abstractclassmethod
    def display_name(self) -> str:
        """Return string name of sensor."""
        pass

    @property
    @abc.abstractclassmethod
    def full_display_name(self) -> str:
        """Return full string name of sensor."""
        pass

    @property
    @abc.abstractclassmethod
    def article(self) -> str:
        """Return string article to use for sensor."""
        pass

    @property
    @abc.abstractclassmethod
    def operation_active_time(self) -> int:
        """Return required time (in seconds) to perform active sensor operation."""
        pass

    @property
    @abc.abstractclassmethod
    def idle_power(self) -> float:
        """Return power (in watts) consumed when sensor is in idle mode."""
        pass

    @property
    @abc.abstractclassmethod
    def active_power(self) -> float:
        """Return power (in watts) consumed when sensor is in active mode."""
        pass

    @property
    @abc.abstractclassmethod
    def max_stored_energy(self) -> float:
        """Return max stored energy of sensor, in Joules (J)."""
        pass

    @abc.abstractclassmethod
    def get_average_load_power(self, duty_cycle_period: int) -> float:
        """Return average load power for sensor, in microwatts (uW), based on duty cycle.

        Args:
            duty_cycle_period: Duty-cycle rate period, in seconds

        Return:
            Average power load, in microwatts
        """
        pass

    @abc.abstractclassmethod
    def get_required_lux(self, duty_cycle_period: int) -> int:
        """Return light (in lux) required for infinite runtime at the requested duty-cycle.

        Args:
            duty_cycle_period: Duty-cycle rate period, in seconds

        Return:
            Required light, in lux
        """
        pass


class EveractiveEnvironmentalPlusEversensor(BaseSensorProfile):
    """Class representing an Everactive Environmental+ Eversensor."""

    def __init__(self):
        self._params = {}
        self._load_sensor_characteristics()

    def _load_sensor_characteristics(self):
        """Load sensor characteristics from environment variables."""

        sensor_characteristics = {
            "max_voltage_on_vcap": "EHP_MAX_VOLTAGE_ON_VCAP",
            "min_voltage_on_vcap": "EHP_MIN_VOLTAGE_ON_VCAP",
            "total_cap_on_vcap": "EHP_TOTAL_CAP_ON_VCAP",
            "total_cap_on_scap": "EHP_TOTAL_CAP_ON_SCAP",
            "avg_power_during_idle": "EHP_AVG_POWER_DURING_IDLE",
            "avg_power_during_1min_sampling": "EHP_AVG_POWER_DURING_1MIN_SAMPLING",
            "operation_active_time": "EHP_OPERATION_ACTIVE_TIME",
            "efficiency_pin_vin": "EHP_EFFICIENCY_PINVIN",
        }

        for characteristic, characteristic_environ in sensor_characteristics.items():
            try:
                self._params[characteristic] = float(os.environ[characteristic_environ])
            except:
                raise Exception(
                    f"Cannot source environment variable {characteristic_environ}"
                )

        voltage_on_vcap = (
            self._params["max_voltage_on_vcap"] ** 2
            - self._params["min_voltage_on_vcap"] ** 2
        )

        # Max stored energy on sensor in Joules (J).
        self._params["max_stored_energy"] = (
            0.5 * self._params["total_cap_on_vcap"] * voltage_on_vcap
        ) + (0.5 * self._params["total_cap_on_scap"] * voltage_on_vcap)

    @property
    def manufacturer(self) -> str:
        return "Everactive"

    @property
    def display_name(self) -> str:
        return "ENV+ Eversensor"

    @property
    def full_display_name(self) -> str:
        return "Environmental+ (ENV+) Eversensor"

    @property
    def article(self) -> str:
        return "an"

    @property
    def operation_active_time(self) -> int:
        """Return time (s) required for the sensor to take a measurement."""
        return self._params["operation_active_time"]

    @property
    def idle_power(self) -> float:
        return self._params["avg_power_during_idle"]

    @property
    def active_power(self) -> float:
        return self._params["avg_power_during_active"]

    @property
    def max_stored_energy(self) -> float:
        return self._params["max_stored_energy"]

    def get_average_load_power(self, duty_cycle_period: int) -> float:
        """Return average load power for sensor, in microwatts (uW), based on duty cycle.

        Args:
            duty_cycle_period: Duty-cycle rate period, in seconds

        Return:
            Average power load, in microwatts
        """

        # Idle & active power are in W, convert to uW.
        average_load_power = (
            (
                (self._params["avg_power_during_1min_sampling"] * SECONDS_IN_MIN)
                + (duty_cycle_period - SECONDS_IN_MIN)
                * self._params["avg_power_during_idle"]
            )
            / duty_cycle_period
        ) * 1_000_000

        return average_load_power

    @property
    def _duty_cycle_period_to_required_lux(self) -> Dict:
        return {
            "continuous": 865,
            15: 295,
            30: 200,
            60: 150,
            120: 125,
            180: 115,
            240: 110,
            300: 110,
            360: 110,
            420: 105,
            480: 105,
            540: 105,
            600: 105,
            660: 105,
            720: 105,
            780: 105,
            840: 105,
            900: 100,
            960: 100,
            1020: 100,
            1080: 100,
            1140: 100,
            1200: 100,
        }

    def get_required_lux(self, duty_cycle_period: int) -> int:
        """Return light (in lux) required for infinite runtime at the requested duty-cycle.

        Args:
            duty_cycle_period: Duty-cycle rate period, in seconds, or "continuous"

        Return:
            Required light, in lux
        """

        try:
            required_lux = self._duty_cycle_period_to_required_lux[duty_cycle_period]
        except KeyError:
            raise KeyError(
                f"No required lux data for duty cycle period {duty_cycle_period}"
            )

        return required_lux
