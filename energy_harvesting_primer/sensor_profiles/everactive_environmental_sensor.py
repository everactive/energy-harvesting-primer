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
