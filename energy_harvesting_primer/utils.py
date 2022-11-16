"""Contains helper methods for energy harvesting primer text and visuals."""

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
