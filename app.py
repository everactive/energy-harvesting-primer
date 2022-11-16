import collections

import pandas as pd
import streamlit as st

import energy_harvesting_primer as eh

IMAGE_DIR = "static/images"

## Page Config ##########################################################
st.set_page_config(
    page_title="Everactive Energy Harvesting Primer",
    page_icon="⚡️",
    initial_sidebar_state="expanded",
)

## Sidebar ##########################################################
st.sidebar.image(f"{IMAGE_DIR}/everactive_logo.png")
st.sidebar.title(f"Energy Harvesting 101")

sidebar_links = [
    {"title": "Fundamentals of Energy Harvesting", "image": "▶︎"},
    {"title": "A Simple Energy Usage Model", "image": "▶︎"},
    {"title": "Energy Harvesting Scenarios", "image": "▶︎"},
    {"title": "Environment Profiles for Harvestable Energy", "image": "▶︎"},
    {"title": "The Eversensor vs. Conventional Batteries", "image": "▶︎"},
]

for link in sidebar_links:
    sidebar_col1, sidebar_col2 = st.sidebar.columns([0.5, 8])
    sidebar_col1.write(link["image"])
    page_link = link["title"].lower().replace(".", "").replace(" ", "-")
    sidebar_col2.markdown(f"[{link['title']}](#{page_link})")

## App Variables ####################################################
sensor_profile = eh.sensor_profiles.EveractiveEnvironmentalSensor()

run_duty_cycle_every = collections.OrderedDict(
    {
        "Continuous": sensor_profile.operation_active_time,
        "Every 30 seconds": 30,
        "Every minute": 60,
        "Every 10 minutes": 60 * 10,
        "Every hour": 60 * 60,
        "Every day": 60 * 60 * 24,
        "Never (always idle)": 10000000,
    }
)

## Fundamentals of Energy Harvesting ################################
st.error("This draft documentation, currently under review.", icon="🚨")

st.header("Fundamentals of Energy Harvesting")

st.markdown(
    f"""{sensor_profile.article.capitalize()} {sensor_profile.display_name} is a
**self-powered** sensor that takes temperature measurements, relative humidity
measurements, and shock/drop readings. The {sensor_profile.display_name} harvests energy
from the surrounding environment, stores the harvested energy locally on a capacitor,
and then consumes the stored harvested energy to take measurements."""
)

energy_harvesting_process_chart = eh.charts.energy_harvesting_process()
st.altair_chart(energy_harvesting_process_chart)

st.markdown(
    """Unlike sensors without energy harvesting, self-powered sensors have an infinite
lifetime because harvested energy can bring the sensor to life at any time. Sensor
runtime, however, depends on the environment in which the sensor operates."""
)

st.markdown(
    """To illustrate the different energy harvesting scenarios, and how they affect
sensor runtime, consider the analogy of a bank account. The energy stored on a sensor
serves as its "bank account."  When the sensor performs an operation, like taking a
measurement, it withdraws energy from that bank account, and the account balance
available for further operations decreases. When the sensor harvests energy, it deposits
energy into its bank account, and the available balance increases."""
)

column_sizes = [1, 12]

col_1_1, col_1_2 = st.columns(column_sizes)
col_2_1, col_2_2 = st.columns(column_sizes)
col_3_1, col_3_2 = st.columns(column_sizes)

col_1_1.subheader(1)
col_1_2.markdown(
    """**Plentiful energy harvesting**. In this scenario, there is ample energy for
the sensor to harvest, and its bank account is overflowing. Energy deposits far exceed
withdrawals, and the sensor is able to "spend" (perform operations) without
budgeting how frequently it processes data or how much data it processes. Sensor runtime
is infinite in an environment with plentiful energy harvesting."""
)

col_2_1.subheader(2)
col_2_2.markdown(
    """**Constrained energy harvesting**. In this scenario, the sensor is able to
harvest energy, but a limited or constrained amount of energy. An energy-constrained
sensor operates with a bank account where it can make both withdrawals and deposits,
albeit modest deposits. If the sensor "lives within its means" and limits how frequently
and how much data it processes, it can save up energy in its bank account over a period
of time. That saved energy can then be used to continue "paying the bills" (taking
measurements) in the absence of regular deposits of energy, so that the bank account
never drops to zero. In this situation, the lifetime of the sensor is infinite. If its
bank account does drop to zero, then the sensor is able to wait until the next deposit,
and can then use that energy to recharge and continue operations."""
)

col_3_1.subheader(3)
col_3_2.markdown(
    """**No energy harvesting**. In this scenario, the sensor isn’t able to harvest
any energy from the surrounding environment, and this renders the sensor equivalent to a
conventional battery-powered sensor with a finite runtime. A battery-powered sensor can
only make withdrawals from its bank account, leaving two options to increase sensor
runtime:

* decrease how frequently the sensor makes withdrawals by decreasing how often it acquires, processes, and transmits data, or
* decrease how much energy the sensor withdraws for each operation by decreasing how much data it processes.

Either way, the end result is the same. Runtime is finite because the sensor will
eventually run out of energy in its bank account."""
)

## A Simple Energy Model ############################################
st.markdown("---")
st.header("A Simple Energy Usage Model")
st.markdown("""""")

st.markdown(
    """The typical sensor use case has two modes of operation: **active** and **idle**.
In idle mode, the sensor waits in a low power mode for the next event (e.g. sampling,
processing, transmitting data) to start. Once the next event begins, the sensor exits
idle mode and enters active mode. During active mode, the sensor performs its work and
consumes a higher average power than in idle mode. When the active operation is
completed, the sensor returns to idle mode. The power profile is depicted below.
"""
)

power_profile_chart = eh.charts.power_profile()
st.altair_chart(power_profile_chart)


st.markdown(
    f"""To generate simplified energy usage model for the {sensor_profile.display_name},
we only need to define a few properties of our system:"""
)

col1, col2 = st.columns(2)
col1.markdown("**Energy Harvest and Storage**")
col1.markdown(
    """* average amount of power harvested
* amount of energy stored on the sensor"""
)
col2.markdown("**Sensor Load**")
col2.markdown(
    """* modes of operation (e.g. idle/standby, sampling, transmission)
* amount of power consumed in each mode of operation
* period of time spent in each mode of operation
"""
)

st.markdown("")
st.markdown(
    """The **duty-cycle rate** is the rate at which the sensor is active. It is
calculated as follows:"""
)

st.latex(r"""R_{cycle} = \dfrac{1}{t_{idle} + t_{active}}""")

st.markdown(
    """where $R_{cycle}$ is the duty-cycle rate, $t_{idle}$ is the time in idle
mode during one duty-cycle, and $t_{active}$ is the time in active mode during one
duty-cycle. The **average load power** is the average of the powers used during each
mode of operation, defined as:"""
)

st.latex(
    r"""P_{load} = R_{cycle}(P_{idle} \cdot t_{idle} + P_{active} \cdot t_{active})"""
)

st.markdown(
    """where $P_{load}$ is the average load power, $P_{idle}$ is the power
consumed in idle mode, and $P_{active}$ is the average power consumed in active mode."""
)

st.markdown(
    """To solve for **runtime**, the stored sensor energy is divided by the
difference between the the load power and harvested power:"""
)

st.latex(r"""t_{runtime} = \dfrac{E_{store}}{P_{load} - P_{harvest}}""")

st.markdown(
    """where $t_{runtime}$ is runtime and $E_{store}$ is the energy stored by
the sensor."""
)


## No Energy Harvesting #############################################
st.markdown("---")
st.header("Energy Harvesting Scenarios")

st.markdown(
    f"""We can apply the simplified energy usage model to two scenarios and explore the
impact of energy harvesting on the {sensor_profile.display_name} runtime for different
duty-cycle rates."""
)

st.subheader("No Energy Harvesting: Equivalent to Battery")

st.markdown(
    f"""When the {sensor_profile.display_name} is not able to harvest any energy from
the environment, it is equivalent to a battery-powered sensor. The design space provides
just one variable without making hardware or firmware changes, duty-cycle rate, and
operation is a trade-off between taking more measurements vs. extending sensor runtime.
Decreasing the duty-cycle rate decreases the average load power and increases sensor
runtime; however, there is a limit. As the sensor approaches its power floor, the
runtime no longer improves."""
)

st.markdown(
    f"""The chart below depicts the expected runtime and measurements$^{1}$ of a {sensor_profile.display_name}
for different duty-cycle rates in the absence of harvestable energy, assuming that the
sensor is fully charged before beginning operation."""
)
st.markdown("")

runtime_no_harvestable_energy_chart = eh.charts.runtime_no_harvestable_energy(
    run_duty_cycle_every, sensor_profile
)
st.altair_chart(runtime_no_harvestable_energy_chart)


## Available Energy Harvesting ######################################
st.subheader("Available Energy Harvesting")

st.markdown(
    f"""The {sensor_profile.display_name} is able to harvest energy from ambient light
using its integrated photovoltaic (PV) cells and store that harvested energy to power
continued measurements. If the sensor can decrease the average load power to less than
the average harvested power, then the runtime of the sensor is **infinite**."""
)

st.markdown(
    f"""Ambient light is measured in lux. As the available ambient light increases, the
{sensor_profile.display_name} is able to operate, with infinite runtime, at increasingly
frequent duty-cycle rates."""
)

df_lux_values = pd.DataFrame(
    [{"display_value": f"{x} lux", "lux": x} for x in range(50, 301, 5)]
)
selected_lux = st.select_slider("Ambient Light", df_lux_values)
harvestable_lux = df_lux_values[df_lux_values["display_value"] == selected_lux].iloc[0][
    "lux"
]

runtime_variable_lux_chart = eh.charts.runtime_variable_lux(
    sensor_profile, harvestable_lux
)
st.altair_chart(runtime_variable_lux_chart)


## Harvesting Energy from the Environment ###########################
st.markdown("---")
st.header("Environment Profiles for Harvestable Energy")

st.markdown(
    f"""Available light enables the {sensor_profile.display_name} to harvest energy from
the environment to perform sensor operations, like taking temperature measurements,
relative humidity measurements, and shock/drop readings. As we saw above, a relatively
low ambient light (200 lux) enables the sensor to reach infinite runtime for duty-cycle
rates as frequent as thirty seconds."""
)

st.markdown(
    f"""A key consideration when using the {sensor_profile.display_name} as part of an
energy harvesting approach is the profile of the environment in which it will be
deployed. The most critical environment profile characteristic is the level of ambient
light available. Without sufficient light, the sensor is not able to harvest enough
energy to achieve infinite runtime. To gauge sensor performance and viable duty-cycle
rates in a given environment, we this need to examine the available ambient light of the
environmental setting."""
)

st.markdown(
    """In outdoor settings, there is substantial ambient light, but this is not
sustained overnight."""
)
st.markdown("")

outdoor_lux_chart = eh.charts.environment_lux_outside()
st.altair_chart(outdoor_lux_chart)

st.markdown(
    f"""In indoor settings, available ambient light is reduced, but with targeted
placement, the {sensor_profile.display_name} can harvest enough energy to power infinite
runtimes for varying duty-cycles."""
)

st.markdown("")

indoor_lux_chart = eh.charts.environment_lux_inside()
st.altair_chart(indoor_lux_chart)


st.markdown(
    """For successful and sustained energy harvesting, it is paramount to consider the
environment and position in which the sensor is placed, and how the ambient light of the
setting varies over time. Except for indoor settings with 24/7 artificial lighting, the
available light will change depending on the time of day, time of year, and the weather.
Continued sensor operation becomes a question of whether the environment profile
supports the sensor harvesting and storing enough energy during well-lit periods such
that it can run in the absence of light until light is restored - for example,
overnight."""
)


## Energy Harvesting vs. Conventional Batteries #####################
st.markdown("---")
st.header("The Eversensor vs. Conventional Batteries")

st.markdown(
    f"""As shown above, the {sensor_profile.display_name} has a short, finite
runtime in the absence of harvestable energy. As a thought experiment, let us explore
the hypothetical runtime of the {sensor_profile.display_name} if it were powered by
a conventional commercial battery."""
)

st.markdown(
    f"""Alkaline batteries, including AAA and AA types have a finite shelf life. Even
though theoretical battery-powered {sensor_profile.display_name} runtime calculations
might predict a runtime of 10+ years, in reality, these batteries have a shelf life of
five to ten years, when kept in ideal conditions (room temperature, low relative
humidity). The calculations used for the chart below thus incorporate a maximum shelf
life of ten years for an alkaline battery."""
)

st.markdown("")

runtime_battery_comparison_chart = eh.charts.runtime_battery_comparison(
    run_duty_cycle_every, sensor_profile
)

st.altair_chart(runtime_battery_comparison_chart)

st.markdown(
    f"""In the absence of harvestable energy, the order of magnitude of runtime is
drastically different between energy harvesting and a commercial battery: years vs.
hours. At first, it might appear that the commercial battery is the more compelling
choice; runtime could theoretically range up to ten years, depending on the duty-cycle
rate. For a single sensor, using a commercial battery is a cheaper choice, with minimal
required maintenance."""
)

st.markdown("""However, there are other key variables to consider.""")

st.subheader("Frequency of Sampling")

st.markdown(
    f"""The {sensor_profile.display_name} takes environmental measurements of interest
at a rate defined by the duty-cycle. Typically, these measurements are taken in service
of a sensing solution that detects events based on available sensor measurements. The
profile of the detected event(s) needs to drive the sensor duty-cycle rate. For example,
an event that occurs over a short period (e.g. a minute, several seconds) is unlikely to
be detected if the sensor takes measurements every day or every hour. To increase the
probability of detecting the event, the sensor would need to take measurements more
frequently, requiring a higher duty-cycle rate."""
)

st.markdown(
    """When using a battery-powered sensor, increasing the sensor duty-cycle rate
decreases the sensor runtime. For sensing solutions that rely on frequent or continuous
duty-cycle rates, battery-powered sensors require increased battery replacement to
compensate for shorter-lived runtimes."""
)

st.subheader("Average Power Load")
st.markdown(
    """The average power load utilized by a sensor increases as new operations are
introduced to the sensor and as it takes on more computationally intensive workloads.
Increasing the average power load will decrease the runtime of a battery-powered sensor.
As such, there is a direct tradeoff between sensor runtime and the number of operations
that can be executed by the sensor over its lifetime. A battery cannot replenish stored
energy in the same manner as an energy harvesting sensor; its number of potential
operations is limited by the power load required by these operations. Average power load
is a central concern for sensor solutions that require intensive edge data processing
capabilities, particularly solutions that leverage machine learning."""
)

st.subheader("Scale of Solution")
st.markdown(
    """Wireless sensing solutions are rarely dependent on one sensor; it often takes a
fleet of sensors to implement a sensing solution for a large operation or facility.
At scale, in challenging environments, sensor maintenance is a substantial concern.
Battery-powered sensors not only require replacements for dead batteries, but also
require an additional level of monitoring such that dead batteries can be detected."""
)

st.markdown(
    """In industrial settings, sensors can be difficult to access due to necessary
placement. Within a facility, a sensor might be located out of reach without a ladder,
under large machinery, or amidst potentially hazardous equipment - the act of replacing
a single battery might take several minutes. As the sensor fleet size increases, the
maintenance burden can quickly scale to require days, weeks, even months of effort
simply to keep battery-powered sensors operational."""
)

df_battery_minutes = pd.DataFrame(
    [{"display_value": f"{x} minutes", "minutes": x} for x in range(3, 10, 1)]
)

selected_time_to_replace_battery = st.select_slider(
    "Average Time to Replace a Battery", value="5 minutes", options=df_battery_minutes
)

time_to_replace_battery = df_battery_minutes[
    df_battery_minutes["display_value"] == selected_time_to_replace_battery
].iloc[0]["minutes"]


battery_maintenance_burden_chart = eh.charts.battery_maintenance_burden(
    time_to_replace_battery
)

st.altair_chart(battery_maintenance_burden_chart)


## Footnotes ########################################################
st.markdown("---")

st.caption("""$^{1}$ Sensor performance was measured at room temperature.""")
