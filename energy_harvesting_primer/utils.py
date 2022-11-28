"""Contains helper methods for energy harvesting primer text and visuals."""

import collections

import pandas as pd

import energy_harvesting_primer.sensor_profiles as profiles

IDLE_DUTY_CYCLE = "Never (always idle)"


def get_runtime_seconds(
    max_stored_energy: float, load_power: float, harvested_power: float
) -> float:
    """Calculate runtime based on max stored energy, load power, and available
    harvestable power.

    Args:
        stored_energy: energy stored, in joules
        load_power: load power, in micro watts (uW)
        harvested_power: harvested power, in micro watts (uW)

    Returns:
        Runtime, in seconds.
        Returns 60M seconds (1M minutes) if runtime is infinite given harvesting params.
    """
    # Add small epsilon to avoid div/0 when harvested power = load power.
    runtime_seconds = (max_stored_energy * 1_000_000) / (
        load_power - harvested_power + 0.00001
    )

    if runtime_seconds < 0:
        return 1_000_000 * 60

    return runtime_seconds


# https://en.wikipedia.org/wiki/List_of_battery_sizes
COMMERCIAL_BATTERY_SIZES = [
    {"name": "AAA (alkaline)", "capacity_mAh": 1200, "voltage": 1.5},
    {"name": "AA (alkaline)", "capacity_mAh": 2700, "voltage": 1.5},
]

MAX_YEARS_SHELF_LIFE = 10


def calculate_battery_runtimes(
    duty_cycles: collections.OrderedDict, sensor_profile: profiles.BaseSensorProfile
) -> pd.DataFrame:
    """Calculate theoretical runtimes for desired duty-cycles, if sensor was powered by
    commercial batteries.

    Args:
        duty_cycles: OrderedDict of duty-cycles to use for chart generation - should
            be keyed by duty-cycle name, with values of duty-cycle length in seconds.
        sensor_profile: Sensor profile object to use for energy/chart calculations

    Returns:
        battery-powered runtimes as pandas DataFrame
    """
    batteries = []

    for battery in COMMERCIAL_BATTERY_SIZES:
        for k, v in duty_cycles.items():
            batteries.append(
                {
                    **battery,
                    "duty_cycle_name": k,
                    "duty_cycle": v,
                }
            )

    df_batteries = pd.DataFrame(batteries)

    df_batteries["capacity_Ah"] = df_batteries["capacity_mAh"].apply(
        lambda x: x * 0.001
    )
    df_batteries["stored_energy_joules"] = df_batteries.apply(
        lambda row: row["capacity_Ah"] * row["voltage"] * 3600, axis=1
    )
    df_batteries["runtime_s"] = df_batteries.apply(
        lambda row: get_runtime_seconds(
            row["stored_energy_joules"],
            sensor_profile.get_average_load_power(
                row["duty_cycle"],
            ),
            0,
        ),
        axis=1,
    )

    df_batteries["ops"] = df_batteries.apply(
        lambda row: 0
        if (row["duty_cycle_name"] == IDLE_DUTY_CYCLE)
        else int(row["runtime_s"] / row["duty_cycle"]) + 1,
        axis=1,
    )

    df_batteries["runtime_min"] = df_batteries["runtime_s"].apply(lambda x: x / 60)
    df_batteries["runtime_hour"] = df_batteries["runtime_min"].apply(lambda x: x / 60)
    df_batteries["runtime_year"] = df_batteries["runtime_hour"].apply(
        lambda x: x / 24 / 365
    )

    df_batteries["runtime_year"] = df_batteries["runtime_year"].apply(
        lambda x: round(min(x, MAX_YEARS_SHELF_LIFE), 1)
    )

    return df_batteries
