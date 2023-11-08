import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import ICON_POWER
from .. import CONF_PIPSOLAR_ID, PIPSOLAR_COMPONENT_SCHEMA, pipsolar_ns

DEPENDENCIES = ["uart"]

CONF_OUTPUT_SOURCE_PRIORITY = "output_source_priority"
CONF_SOLAR_POWER_PRIORITY = "solar_power_priority"
CONF_CHARGER_SOURCE_PRIORITY_SOLARFIRST = "charger_source_priority_solarfirst"
CONF_CHARGER_SOURCE_PRIORITY_UTILITY = "charger_source_priority_utility"
CONF_CHARGER_SOURCE_PRIORITY_SOLARONLY = "charger_source_priority_solaronly"

CONF_SILENCE_BUZZER_OPEN_BUZZER = "silence_buzzer_open_buzzer"
CONF_LCD_ESCAPE_TO_DEFAULT = "lcd_escape_to_default"
CONF_OVERLOAD_BYPASS_FUNCTION = "overload_bypass_function"
CONF_OVERLOAD_RESTART_FUNCTION = "overload_restart_function"
CONF_OVERHEAT_RESTART_FUNCTION = "overheat_restart_function"
CONF_BACKLIGHT_ON = "backlight_on"
CONF_ALARM_ON_WHEN_PRIMARY_SOURCE_INTERRUPT = "alarm_on_when_primary_source_interrupt"
CONF_FAULT_CODE_RECORD = "fault_code_record"
CONF_MACHINE_TYPE = "machine_type" # E: Grid-Tie, D: Off-Grid Tie
# CONF_LIBAT_IMMEDIATELY_TURNON = "libat_immediately_turnon"
# CONF_LIBAT_AUTO_TURNON = "libat_auto_turnon"

CONF_LOAD_CONNECTION = "load_connection"

CONF_INPUT_VOLTAGE_RANGE = "input_voltage_range" # m - 0: Appliance, 1: UPS
CONF_CLEAR_ENERGY_DATA = "clear_energy_data"

TYPES = {
    # 0: Solar-Utility-Battery, 1: Solar-Battery-Utility
    CONF_OUTPUT_SOURCE_PRIORITY: ("^S007POP1", "^S007POP0"),

    # 0: Battery-Load-Utility, 1: Load-Battery-Utility
    CONF_SOLAR_POWER_PRIORITY: ("^S007PSP1", "^S007PSP0"),

    # 0: Solar first
    CONF_CHARGER_SOURCE_PRIORITY_SOLARFIRST: ("^S009PCP0,0", None),
    # 1: Solar and Utility,
    CONF_CHARGER_SOURCE_PRIORITY_UTILITY: ("^S009PCP0,1", None),
    # 2: Only solar
    CONF_CHARGER_SOURCE_PRIORITY_SOLARONLY: ("^S009PCP0,2", None),

    CONF_SILENCE_BUZZER_OPEN_BUZZER: ("^S006PEA", "^S006PDA"),
    CONF_OVERLOAD_BYPASS_FUNCTION: ("^S006PEB", "^S006PDB"),
    CONF_LCD_ESCAPE_TO_DEFAULT: ("^S006PEC", "^S006PDC"),
    CONF_OVERLOAD_RESTART_FUNCTION: ("^S006PED", "^S006PDD"),
    CONF_OVERHEAT_RESTART_FUNCTION: ("^S006PEE", "^S006PDE"),
    CONF_BACKLIGHT_ON: ("^S006PEF", "^S006PDF"),
    CONF_ALARM_ON_WHEN_PRIMARY_SOURCE_INTERRUPT: ("^S006PEG", "^S006PDG"),
    CONF_FAULT_CODE_RECORD: ("^S006PEH", "^S006PDH"),
    CONF_MACHINE_TYPE: ("^S006PEI", "^S006PDI"),
    # CONF_LIBAT_IMMEDIATELY_TURNON: ("^S006PEJ", "^S006PDJ"),
    # CONF_LIBAT_AUTO_TURNON: ("^S006PEK", "^S006PDK"),

    CONF_LOAD_CONNECTION: ("^S007LON1", "^S007LON0"),
    CONF_INPUT_VOLTAGE_RANGE: ("^S007PGR0", "^S007PGR1"),
    CONF_CLEAR_ENERGY_DATA: ("^S006CLE", None),
}

PipsolarSwitch = pipsolar_ns.class_("PipsolarSwitch", switch.Switch, cg.Component)

PIPSWITCH_SCHEMA = switch.switch_schema(
    PipsolarSwitch, icon=ICON_POWER, block_inverted=True
).extend(cv.COMPONENT_SCHEMA)

CONFIG_SCHEMA = PIPSOLAR_COMPONENT_SCHEMA.extend(
    {cv.Optional(type): PIPSWITCH_SCHEMA for type in TYPES}
)


async def to_code(config):
    paren = await cg.get_variable(config[CONF_PIPSOLAR_ID])

    for type, (on, off) in TYPES.items():
        if type in config:
            conf = config[type]
            var = await switch.new_switch(conf)
            await cg.register_component(var, conf)
            cg.add(getattr(paren, f"set_{type}_switch")(var))
            cg.add(var.set_parent(paren))
            cg.add(var.set_on_command(on))
            if off is not None:
                cg.add(var.set_off_command(off))
