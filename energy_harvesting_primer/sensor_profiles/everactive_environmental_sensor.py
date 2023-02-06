"""Contains classes representing energy harvesting sensors."""

import abc
from typing import Dict


class BaseSensorProfile(abc.ABC):
    """Abstract base class to represent a Energy Harvesting Sensor showcased and
    explored through the Energy Harvesting Sensors 101 primer.

    Typical usage example:
        class MyNewSensor(BaseSensorProfile):
            ...
    """

    @property
    @abc.abstractclassmethod
    def manufacturer(self) -> str:
        """Return name of manufacturer."""
        pass

    @property
    @abc.abstractclassmethod
    def display_name(self) -> str:
        """Return (short) display name of sensor."""
        pass

    @property
    @abc.abstractclassmethod
    def full_display_name(self) -> str:
        """Return full display name of sensor."""
        pass

    @abc.abstractclassmethod
    def get_required_lux(self, sampling_rate: int) -> int:
        """Return light (in lux) required to achieve infinite sensor runtime at the
        requested sampling rate.

        Args:
            sampling_rate: Sampling rate period, in seconds, or "continuous"

        Return:
            Required light, in lux
        """
        pass


class EveractiveEnvironmentalPlusEversensor(BaseSensorProfile):
    """Class representing an Everactive Environmental+ (ENV+) Eversensor.

    Provides attributes such as manufacturer, display name that are repeatedly
    referenced in primer content.

    Typical usage example:
        sensor_profile = EveractiveEnvironmentalPlusEversensor()
        print(f"This is the {sensor_profile.display_name()} sensor.")
        lux = sensor_profile.get_required_lux(30)
    """

    @property
    def manufacturer(self) -> str:
        """Return name of manufacturer."""
        return "Everactive"

    @property
    def display_name(self) -> str:
        """Return (short) display name of sensor."""
        return "ENV+ Eversensor"

    @property
    def full_display_name(self) -> str:
        """Return full display name of sensor."""
        return "Environmental+ (ENV+) Eversensor"

    @property
    def _sampling_rate_to_required_lux(self) -> Dict:
        return {
            # sampling rate (in seconds) : light intensity (in lux)
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

    def get_required_lux(self, sampling_rate: int) -> int:
        """Return light (in lux) required to achieve infinite sensor runtime at the
        requested sampling rate.

        Args:
            sampling_rate: Sampling rate period, in seconds, or "continuous"

        Return:
            Required light, in lux
        """
        try:
            required_lux = self._sampling_rate_to_required_lux[sampling_rate]
        except KeyError:
            raise KeyError(f"No required lux data for sampling rate {sampling_rate}")

        return required_lux
