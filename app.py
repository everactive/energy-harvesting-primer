import collections
import re

import pandas as pd
import streamlit as st

import energy_harvesting_primer as eh

IMAGE_DIR = "static/images"
ST_LINE_BREAK = "  \n"

## Page Config ##########################################################
st.set_page_config(
    page_title="Everactive: Energy Harvesting Sensors 101",
    page_icon="⚡️",
    initial_sidebar_state="expanded",
)


## App Variables ####################################################
sensor_profile = eh.sensor_profiles.EveractiveEnvironmentalPlusEversensor()


## Sidebar ##########################################################
st.sidebar.image(f"{IMAGE_DIR}/everactive_logo.png")
st.sidebar.title(f"Energy Harvesting Sensors 101")

sidebar_links = [
    {
        "title": "Introduction",
        "level": "I",
        "page_link": "energy-harvesting-sensors-101",
    },
    {"title": "Fundamentals of Energy Harvesting Sensors", "level": "II"},
    {"title": "Environment Profiles for Energy Harvesting", "level": "III"},
    {"title": "Energy Harvesting Sensor Power Management", "level": "IV"},
    {
        "title": f"The Everactive Environmental+ Batteryless IoT Evaluation Kit and Eversensor",
        "level": "V",
    },
    {
        "title": f"Energy Harvesting in Action with the {sensor_profile.manufacturer} {sensor_profile.display_name}",
        "level": "VI",
    },
    {"title": "Continue the Exploration", "level": "VII"},
]

for idx, link in enumerate(sidebar_links):
    sidebar_col1, sidebar_col2, _ = st.sidebar.columns([1.5, 10, 1])
    sidebar_col1.markdown(f"**{link['level']}**")

    if link.get("page_link"):
        page_link = link["page_link"]
    else:
        page_link = re.sub(r"[\.\+\:]", "", link["title"].lower()).replace(" ", "-")

    sidebar_col2.markdown(f"{ST_LINE_BREAK}[{link['title']}](#{page_link})")


## Introduction #####################################################
st.caption(
    "⚡️ This primer is interactive: explore energy harvesting through chart mouseover, clicks, and controls. ⚡️"
)

st.header("Energy Harvesting Sensors 101")

st.markdown(
    """Welcome to Everactive's Energy Harvesting Sensors 101. In this primer, we'll
explore:
* the fundamentals of energy harvesting sensor nodes,
* environmental conditions that affect energy harvesting,
* and power usage within energy harvesting sensor nodes.

You will gain intuition on how energy harvesting sensor nodes operate in the real world,
along with an appreciation of the tradeoffs that come in to play when designing and using
these types of systems."""
)

st.markdown(
    f"""We will also showcase the [{sensor_profile.manufacturer}
{sensor_profile.display_name}](#the-everactive-environmental-batteryless-iot-evaluation-kit)
as an example of a real-world energy harvesting sensor node."""
)

st.info(
    """Note that within this primer, we will refer to energy harvesting sensor nodes as
*energy harvesting sensors* or *sensors* for simplicity. The focus of our exploration
is the system of the node and how it uses harvested energy, rather than simply the
mechanics of the harvesting itself.""",
    icon="ℹ",
)


## Fundamentals of Energy Harvesting ################################
st.markdown("---")
st.header("Fundamentals of Energy Harvesting Sensors")

st.markdown(
    """**Energy** is the capacity to do work. In the context of a sensor, **work** is
performing operations, such as: taking a measurement (reading), making a calculation, or
transmitting data. When a sensor does work, it consumes energy. **Power** is the rate at
which energy is produced or consumed; it is energy per unit of time. Energy harvesting
sensors harvest energy from the surrounding environment, and either directly consume
that energy in order to perform work, or store the energy locally to consume it at a
later time."""
)

energy_harvesting_process_chart = eh.charts.energy_harvesting_process()
st.altair_chart(energy_harvesting_process_chart)

st.markdown(
    """A sensor exists in one of two states: **available**, in which it has sufficient
energy to perform work, or **unavailable**, in which it does not have sufficient energy
to perform work. The **runtime** of a sensor is the remaining time until an available
sensor becomes unavailable, and the **lifetime** of a sensor is the time period over
which a sensor can become available and perform work."""
)
st.markdown("")

col1, col2 = st.columns([1, 1])
col1.markdown("**Energy Source: Harvesting**")
col1.markdown(
    """* variable availability
* infinite lifetime
* lifetime = *n* runtimes"""
)

col2.markdown("**Energy Source: Battery**")
col2.markdown(
    """* continuous availability
* finite lifetime
* lifetime = runtime"""
)

st.markdown("")
st.markdown(
    """Energy harvesting sensors have an infinite lifetime (given the presence of
harvestable energy) because harvested energy can transition a sensor from unavailable to
available at any time. The current runtime of an energy harvesting sensor, and its
availability over its lifetime, depends on the environment in which the sensor
operates."""
)

st.markdown(
    """To illustrate the different energy harvesting zones, and how each affects sensor
availability, runtime, and lifetime, consider the analogy of a bank account. The energy
stored on a sensor serves as its "bank account."  When a sensor performs work, like
taking a measurement or transmitting a data packet, it withdraws energy from that bank
account, and the account balance available for further operations decreases. When a
sensor harvests energy, it deposits energy into its bank account, and the available
balance increases."""
)

column_sizes = [1, 12]

col_1_1, col_1_2 = st.columns(column_sizes)
col_2_1, col_2_2 = st.columns(column_sizes)
col_3_1, col_3_2 = st.columns(column_sizes)

col_1_1.subheader(1)
col_1_2.markdown(
    """**Plentiful energy harvesting**. In this zone, there is ample energy for a sensor
to harvest, and its bank account is overflowing. Energy deposits far exceed withdrawals,
and a sensor is able to "spend" (perform work) without budgeting how frequently it works
or how much energy it consumes while working. In an environment with plentiful energy
harvesting, sensor availability is continuous, sensor runtime is infinite, and sensor
lifetime is infinite."""
)

col_2_1.subheader(2)
col_2_2.markdown(
    """**Limited energy harvesting**. In this zone, a sensor is able to harvest energy,
but a limited amount of energy. It operates with a bank account where it can make both
withdrawals and deposits, albeit modest deposits. If a sensor "lives within its means"
and limits how frequently it works and how much energy it consumes when working, it can
save up energy in its bank account over a period of time. That saved energy can then be
used to continue "paying the bills" (performing work) in the absence of regular deposits
of energy, so that the bank account never drops to zero. A sensor in this zone is
*power-constrained*; it must be conservative with the rate at which it uses its energy.

In this situation, the lifetime of a sensor is infinite, though its availability and
length of runtimes will vary based on the level of harvestable energy. If its bank
account does drop to zero, an energy harvesting sensor is able to wait until the next
deposit, and can then use that energy to transition to available and resume work."""
)

col_3_1.subheader(3)
col_3_2.markdown(
    """**No energy harvesting**. In this zone, a sensor is not able to harvest any
energy from the surrounding environment; it is *energy-constrained*, and can only make
withdrawals from its bank account. Sensor runtime and lifetime are both finite. Once
the sensor depletes its energy bank account, it becomes unavailable and remains in that
state due to lack of further deposits of harvested energy.

When energy-constrained, a sensor has two options to increase its remaining runtime:
* Decrease the frequency of its energy withdrawals by reducing how often it performs work
* Decrease how much energy it withdraws for each that operation it performs

However, runtime is ultimately finite because the sensor will eventually run out of
energy in its bank account."""
)


## Environment Profiles for Energy Harvesting #######################
st.markdown("---")
st.header("Environment Profiles for Energy Harvesting")

st.markdown(
    """A energy harvesting sensor is able to harvest energy from its surrounding
environment by converting the target energy type (for instance, ambient solar or thermal
energy) into electrical energy that is stored locally on the sensor. A key design
consideration when using an energy harvesting sensor is thus the profile of the
environment in which the sensor is deployed."""
)

st.markdown(
    f"""Sensors that harvest light energy from the environment use a solar cell, or
photovoltaic (PV) cell, to convert available light into electricity. The most critical
environment profile characteristic for a PV cell-enabled sensor is the level of
intensity of the available ambient light, which is measured in lux. The environment lux
level contributes to whether a sensor operates in a plentiful, limited, or no energy
harvesting zone and has a direct impact on sensor availability and runtime."""
)

st.markdown(
    """In outdoor settings, environment lux levels are driven by ambient solar light,
and vary widely depending on the time of day and the weather. The chart below depicts
typical lux levels across a range of outdoor conditions.$^{1}$"""
)
st.markdown("")

outdoor_lux_chart = eh.charts.environment_lux_outside()
st.altair_chart(outdoor_lux_chart)

st.markdown(
    """In indoor settings$^{2}$, environmental lux levels are driven primarily by
ambient artificial lighting, but can also be influenced by the presence of ambient solar
light. The chart below depicts characteristic lux ranges across a variety of indoor
spaces.$^{3}$"""
)

st.markdown("")

indoor_lux_chart = eh.charts.environment_lux_inside()
st.altair_chart(indoor_lux_chart)

st.markdown(
    """The most reliable way to determine the intensity of ambient light in a given
environment is to use a dedicated light meter. The human eye is not a reliable judge of
the intensity of ambient light, particularly in dimmer ranges where a difference of tens
of lux may significantly impact energy harvesting sensor availability and runtime.
Although light meter smartphone apps exist, their accuracy does not approach that of
dedicated light meters, particularly when taking readings in low light conditions.
Further, there are a variety of factors that affect the intensity of light that a PV
cell can detect in a given environment and position within that environment, including:
the distance from a light source, the type of light source, and the position of the
light source relative to the PV cell."""
)

st.markdown(
    f"""For sustained energy harvesting sensor availability, it is paramount to consider
the environment lux level, the position in which a sensor is placed within the
environment, and how the ambient light of the environment varies over time. Except for
indoor settings with continuous, artificial-only lighting, environment ambient light
will change depending on a variety of factors: for instance, the time of day, time of
year, the weather, or variable obstruction of a light source. Acceptable sensor
availability and performance becomes a question of whether the environment profile supports the sensor
harvesting and storing enough energy during well-lit periods such that it can run in the
absence of light until light is restored, for example, overnight."""
)

## A Simple Energy Model ############################################
st.markdown("---")
st.header("Energy Harvesting Sensor Power Management")

st.subheader("""Power Usage and Mode of Operation""")

st.markdown(
    f"""An available sensor consumes energy to perform work. The sensor power is the the
rate at which the sensor consumes energy, calculated as the energy consumption over time."""
)

st.latex(r"""P = \dfrac{E}{t}""")

st.markdown(
    """Sensor work comprises different operations, for example: taking a measurement,
transmitting a data packet, running inference using a TinyML model, or receiving an
over-the-air update. These operations all require differing amounts of energy to
complete. When completed over the same period of time, sensor operations requiring a
higher energy consumption will use more power, and operations requiring a lower energy
consumption will use less power."""
)

st.markdown(
    f"""The **mode of operation** of a sensor is defined by the operations that the
sensor performs while in that mode. The average power usage of a mode is defined by the
power required for each of its constituent operations. For instance, a sensor that takes
environmental readings, transmits those readings, and receives over-the-air updates
might use the following modes:"""
)
st.markdown("")

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

col1.markdown("**Measurement Mode**")
col1.markdown("`medium power`")
col1.markdown(
    """* take reading
* store reading"""
)

col2.markdown("**Transmit Mode**")
col2.markdown("`medium power`")
col2.markdown("* transmit reading data packet")

col3.markdown("**Update Mode**")
col3.markdown("`high power`")
col3.markdown(
    """* download update
* install update"""
)

col4.markdown("**Standby Mode**")
col4.markdown("`low power`")
col4.markdown("""* wait on clock to trigger event""")

st.markdown("")
st.markdown(
    """Sensor power usage changes as a sensor transitions between different modes of
operation."""
)

st.markdown("")
st.subheader("""A Simple Sensor Power Usage Model""")

st.markdown(
    f"""To define a simplified power usage model for an energy harvesting sensor,
consider a theoretical sensor with two modes: **active** and **idle**. In active mode,
the sensor *samples*&mdash;it takes and transmits one reading. In idle mode, the sensor
listens for a request to trigger its next sample. (Assume that the request signal is
generated at a consistent frequency). The sensor uses more power to sample in active
mode than when waiting in idle mode.

In idle mode, the sensor waits to receive a request, consuming minimal power. Once a
request for a sample arrives, the sensor exits idle mode and enters active mode. While
in active mode, the sensor takes and transmits a reading, consuming more power than when
previously in idle mode. When its active sampling operations are completed, the sensor
returns to idle mode and low power usage, until it receives its next reading request.
These transitions are illustrated in the chart below."""
)

col1, col2, col3, col4 = st.columns([1, 1, 1.25, 2])
idle_power = col1.number_input(
    f"Idle Power ({eh.utils.MU}W)", min_value=10, max_value=60, step=1, value=10
)

active_power = col2.number_input(
    f"Active Power ({eh.utils.MU}W)",
    min_value=idle_power + 1,
    max_value=75,
    step=1,
    value=60,
)

reading_seconds = col3.number_input(
    f"Sampling Operation (s)", min_value=5, max_value=25, step=1, value=15
)

event_frequencies = collections.OrderedDict(
    {
        "every 30 seconds": 30,
        "every minute": 60,
        "every 5 minutes": 60 * 5,
        "every 15 minutes": 60 * 15,
        "every half hour": 60 * 30,
    }
)

sampling_frequency = col4.selectbox(
    "Sampling Frequency", list(event_frequencies.keys()), index=1
)

power_profile_chart, duty_cycle, average_load_power = eh.charts.power_profile(
    idle_power=idle_power,
    active_power=active_power,
    active_operation_seconds=reading_seconds,
    active_operation_frequency=event_frequencies[sampling_frequency],
)

col1, col2, _ = st.columns([1, 2, 5])
col1.metric("Duty Cycle", round(duty_cycle, 2))
col2.metric("Average Load Power", f"{round(average_load_power)} {eh.utils.MU}W")

st.altair_chart(power_profile_chart)

st.markdown("")
st.markdown(
    """The **duty-cycle**, $D$, is the rate at which the sensor is active. It is
calculated as the fraction of one *period* in which the sensor is active. In the above
example, duty cycle is driven by the sampling frequency; one period is a single cycle
of: taking a reading, transmitting the reading, and waiting for the next reading
request. $t_{active}$ is the time spent by the sensor taking and transmitting a reading
in active mode, and $t_{idle}$ is the time spent in idle mode waiting for the next reading
request."""
)

st.latex(r"""D=\dfrac{t_{active}}{t_{idle} + t_{active}}""")

st.markdown("")
st.markdown(
    """The **average load power** is the average of the powers used during each mode of
operation. $P_{active}$ is the power consumed while in active mode, and $P_{idle}$ is
the power consumed while in idle mode."""
)

st.latex(r"""P_{load} = D \cdot P_{active} + (1-D) \cdot P_{idle}""")

st.markdown("")
st.subheader("""Power Management and Energy Harvesting Zones""")

st.markdown(
    """In energy harvesting systems, available power can scale across many orders of
magnitude&mdash;far more so than conventional battery-powered systems. This presents
both challenges, and opportunities, for energy harvesting system designers to scale
power usage across the same orders of magnitude. Power management is at the heart of
effective and efficient energy harvesting sensors and systems."""
)

st.markdown(
    """Consider a theoretical, ideal energy harvesting sensor that functions such that
the power consumed (the load power) is equal to the power harvested. Further,
this sensor is "**always-on**." If the sensor is available, then it continuously
performs "always-on" operations that consume a baseline level of power. An example of
an always-on operation might be listening for a wakeup signal to perform a task, or
harvesting and storing energy. The always-on power is the minimum amount of power that
the sensor requires to remain available. For as long as the sensor remains available,
its power consumption is at least the always-on power."""
)

caption_text = """*The chart below uses a* `log` scale *for power, so that a very wide range
of power values&mdash;from one nanowatt (10$^{-9}$ watts) to one watt&mdash;can be
displayed compactly.*"""

st.caption(caption_text)

example_load_power_vs_harvested_power_chart = (
    eh.charts.example_load_power_vs_harvested_power()
)
st.altair_chart(example_load_power_vs_harvested_power_chart)

st.markdown(
    """Next, consider the modes of the ideal sensor. In addition to its always-on
operations, the sensor has a variety of modes that enable it to perform other
operations, such as taking readings or transmitting data. Work done in these modes is
generally frequency- or event-driven, for example, taking a reading once a minute. The
work done for a given mode consumes power in addition to the power consumed by the
always-on operations. The power consumption of the sensor across different modes is
plotted in the chart below."""
)

st.markdown(
    """Each mode consumes varying levels of load power at increasing duty cycles. When
the sensor is fully active in a given mode, its load power is equal to the **active
power** of that mode. When the sensor is partially active in the given mode, the load
power varies between the sensor always-on power and the mode active power. When the duty
cycle is negligible and the sensor is minimally (or not) active in a given mode, the
sensor load power settles at the always-on power."""
)

st.caption(
    """The chart below plots the `log` of load power against the `log` of duty
cycle. Recall that duty cycle is the ratio of time that the sensor is active (in the
given mode); using `log(duty cycle)` normalizes the duty cycle between 0 and 1. As the
`log(duty cycle)` nears 1, the sensor nears continuous activity for a given mode. Click
on the mode name in the legend to isolate its power curve on the chart."""
)

example_power_modes_chart = eh.charts.example_power_modes()
st.altair_chart(example_power_modes_chart)


st.markdown(
    """The [energy harvesting zones](#fundamentals-of-energy-harvesting-sensors) that
were covered earlier in the primer can now be defined and calculated based on the
concepts covered in this section. These energy harvesting zones are calculated relative to
load power of the sensor and can be defined in terms of harvestable power. When the
expected power consumption of a sensor is known, based on the desired operating mode and
the rate at which the sensor operates in that mode, then one can define the real-world
boundaries of the three zones:
1. Plentiful energy harvesting
2. Limited energy harvesting
3. No energy harvesting"""
)

st.markdown(
    """In the interactive chart below, experiment with changes to sensor mode of
operation and always-on power and explore the effects of these variables on energy
harvesting zones, for the ideal sensor."""
)
st.markdown("")

df_power_list = pd.DataFrame(
    [
        {"label": "10 nanowatts (10 nW)", "value": 1e-8},
        {"label": "100 nanowatts (100 nW)", "value": 1e-7},
        {"label": "1 microwatt (1 \u03bcW)", "value": 1e-6},
        {"label": "10 microwatts (10 \u03bcW)", "value": 1e-5},
        {"label": "100 microwatts (100 \u03bcW)", "value": 1e-4},
        {"label": "1 milliwatt (1 mW)", "value": 1e-3},
        {"label": "10 milliwatts (10 mW)", "value": 1e-2},
        {"label": "100 milliwatts (100 mW)", "value": 1e-1},
        # {"label": "1 watt (1W)", "value": 1e0},
    ]
)

col1, col2 = st.columns([1, 1])

selected_p_always_on = col1.selectbox(
    "Sensor Always-On Power",
    options=df_power_list[df_power_list["value"] < 1e-1],
    index=2,
)
p_always_on = df_power_list[df_power_list["label"] == selected_p_always_on].iloc[0][
    "value"
]

len_active_power_list = len(df_power_list[df_power_list["value"] > p_always_on])
active_power_index = (
    len_active_power_list - 1 if ((len_active_power_list - 1) < 2) else 2
)

selected_p_active = col2.selectbox(
    "Sensor Mode of Operation: Active Power",
    options=df_power_list[df_power_list["value"] > p_always_on],
    index=active_power_index,
)
p_active = df_power_list[df_power_list["label"] == selected_p_active].iloc[0]["value"]

power_operating_space_chart = eh.charts.power_operating_space(p_always_on, p_active)
st.altair_chart(power_operating_space_chart)

st.markdown(
    """Once the required harvested power is known for the three zones, given
the range of expected sensor load power, it is possible to use the specifics of the
energy harvesting sensor to convert required harvestable power to the required
environmental conditions. For example, for a sensor equipped with a PV cell, one could
use the operating characteristics of the PV cell to calculate the lux level required for
a desired harvestable power. Similarly, if the lux levels of the sensor deployment
environment were known and translated into available harvestable power, it would be
possible to predict the availability and performance of an energy harvesting sensor in
that environment, based on its expected power consumption."""
)

## The ENV+ Environmental Sensor ################################
st.markdown("---")
st.header(
    f"The Everactive Environmental+ Batteryless IoT Evaluation Kit and Eversensor"
)

st.markdown(
    f"""[**The Everactive Environmental+ Batteryless IoT Evaluation Kit**](https://everactive.com/product/environmental-evaluation-kit/)
(EvalKit) is a new offering from Everactive that enables hardware and software
developers to learn how to design robust, self-powered Internet of Thing (IoT) products
without the constraints of batteries. Our EvalKits, powered by
{sensor_profile.manufacturer} {sensor_profile.full_display_name} nodes, offer the
following capabilities:"""
)

tech_spec_column_ratio = [1, 5]
icon_dir = f"{IMAGE_DIR}/icons"

col1, col2 = st.columns(tech_spec_column_ratio)
col1.image(f"{icon_dir}/photovoltaic_icon.png")

col2.markdown(
    f"""**Photovoltaic Energy Harvesting**{ST_LINE_BREAK}The
{sensor_profile.display_name} uses an AM1454 solar cell to harvest energy by converting
available light into electricity."""
)

col1, col2 = st.columns(tech_spec_column_ratio)
col1.image(f"{icon_dir}/environmental_sensing_icon.png")
col2.markdown(
    f"""**Environmental Sensing**{ST_LINE_BREAK}The {sensor_profile.display_name} uses
a BME280 environmental sensor to measure temperature, humidity, and barometric pressure.
It also uses an ultra-low power accelerometer, the ADXL362, to measure acceleration
along three axes."""
)

col1, col2 = st.columns(tech_spec_column_ratio)
col1.image(f"{icon_dir}/energy_storage_icon.png")

col2.markdown(
    f"""**Energy Storage**{ST_LINE_BREAK}The {sensor_profile.display_name} has an
operating capacitance of 2.5mF and 800mF of storage capacitance. The sensor node's
operating capacitance is supported by a bank of 100uF low&#8209;leakage ceramic
capacitors, and its storage capacitance is supported by a CAP&#8209;XX&nbsp;HA130F
supercapacitor."""
)

st.markdown(
    f"""When the {sensor_profile.display_name} takes an environmental reading, it
transmits the reading as a data packet to the Mini Evergateway, which uses a
virtual gateway running on the user's computer to send the reading to the
Everactive cloud. The reading data is then accessible via the Everactive Developer
Console, the Everactive API, or a webhook connection."""
)

st.image(f"{IMAGE_DIR}/everactive_evalkit_data_flow.png")

st.markdown(
    f"""The EvalKit provides developers and designers with hands-on experience of the
building blocks of hyperscale IoT applications, including the energy harvesting sensor
concepts covered in this primer."""
)


## Energy Harvesting Scenarios ######################################
st.markdown("---")
st.header(
    f"Energy Harvesting in Action with the {sensor_profile.manufacturer} {sensor_profile.display_name}"
)

st.markdown(
    f"""The {sensor_profile.manufacturer} {sensor_profile.display_name} is one example
of a real-world, always-on energy harvesting sensor. The {sensor_profile.display_name}
uses a PV cell to harvest light energy from the environment. Harvested energy is used by
the sensor to sample; it takes environmental readings and transmits the data to the
Everactive cloud (via the Mini Evergateway)."""
)

st.markdown(
    f"""The **sampling frequency** is the rate at which the {sensor_profile.display_name}
takes and transmits a reading. As the intensity of the available ambient light (lux)
increases, the {sensor_profile.display_name} is able to harvest increased amounts of
energy that are used for harvestable power to satisfy the power consumed by the
{sensor_profile.display_name} when sampling. Increased lux levels provide increased
harvestable power, which enables the sensor to increase its sampling frequency."""
)

st.markdown(
    f"""When there is ample lux to operate in the plentiful energy harvesting zone at a
given sampling frequency, then the {sensor_profile.display_name} is able to achieve
infinite runtime and operate indefinitely at that sampling frequency."""
)

st.markdown(
    f"""The performance figures$^{4}$ showcased below are dependent on the
characteristics of the current {sensor_profile.display_name} hardware, notably the
capacitor and supercapacitor size."""
)

lux_slider_increments = [50, 100, 105, 110, 115, 125, 150, 200, 300]
df_lux_values = pd.DataFrame(
    [{"display_value": f"{x} lux", "lux": x} for x in lux_slider_increments]
)

selected_lux = st.select_slider("Ambient Light", df_lux_values, value="100 lux")
harvestable_lux = df_lux_values[df_lux_values["display_value"] == selected_lux].iloc[0][
    "lux"
]

runtime_variable_lux_chart = eh.charts.runtime_variable_lux(
    sensor_profile, harvestable_lux
)
st.altair_chart(runtime_variable_lux_chart)


## Introduction #####################################################
st.markdown("---")
st.header("Continue the Exploration")

st.markdown(
    """If this primer has piqued your interest and aided your understanding of energy
harvesting sensors and systems, head over to [everactive.com](https://everactive.com/)
to learn more about how you can adopt Everactive Edge technology to power your own
solutions."""
)

st.markdown(
    "* [Our Batteryless Technology](https://everactive.com/batteryless-technology/)"
)
st.markdown(
    "* [Real-World, Industrial IoT Solutions Using Our Technology](https://everactive.com/applications/)"
)
st.markdown(
    "* [How You Can Start Developing with Everactive Edge](https://everactive.com/self-powered-iot-developers/)"
)

st.markdown(
    """Stay tuned for further additions to Everactive's Energy Harvesting Sensors &
Systems curriculum."""
)

## Footnotes ########################################################
st.markdown("---")

st.caption(
    "$^{1}$ Chart References: [Engineering Toolbox: Outdoor Light Levels](https://www.engineeringtoolbox.com/light-level-rooms-d_708.html)"
)
st.caption("$^{2}$" f"The {sensor_profile.display_name} is rated for indoor use.")
st.caption(
    """$^{3}$ Chart References: EN 12464-1:2021, [EnOcean Application Notes: AN201 Indoor Lighting Conditions](https://www.enocean.com/wp-content/uploads/application-notes/AN201_INDOOR_LIGHTING_CONDITIONS_2020.pdf)"""
)
st.caption("""$^{4}$ Sensor performance was measured at room temperature.""")
