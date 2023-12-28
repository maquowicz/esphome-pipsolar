import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.components import output
from esphome.const import CONF_ID, CONF_VALUE
from .. import PIPSOLAR_COMPONENT_SCHEMA, CONF_PIPSOLAR_ID, pipsolar_ns
#from numpy import arange

DEPENDENCIES = ["pipsolar"]

PipsolarOutput = pipsolar_ns.class_("PipsolarOutput", output.FloatOutput)
SetOutputAction = pipsolar_ns.class_("SetOutputAction", automation.Action)

CONF_POSSIBLE_VALUES = "possible_values"

# ^S007PBTm<CRC><cr>: Set battery type
# m: 0: AGM, 1: Flooded, 2: User, 3:Pylontech, 5:WECO, 6:Soltaro, 8:LIB, 9:LIC
CONF_BATTERY_TYPE = "battery_type"

# ^S013MCHGCm,nnn<CRC><cr>: Set battery maximum charge current
CONF_MAX_CHARGING_CURRENT = "max_charging_current"

# ^S014MUCHGCm,nnn<CRC><cr>: Set battery maximum AC charge current
CONF_MAX_AC_CHARGING_CURRENT = "max_ac_charging_current"

# ^S014BUCDmmm,nnn
# mmm - battery_recharge_voltage - Battery re-charged voltage when utility is available	m: 0~9, unit: 0.1V
CONF_BATTERY_REDISANDCHARGE_VOLTAGES = "battery_redisandcharge_voltages"
# Selectable value
# 12V unit: 11V/11.3V/11.5V/11.8V/12V/12.3V/12.5V/12.8V 
# 24V unit: 22V/22.5V/23V/23.5V/24V/24.5V/25V/25.5V 
# 48V unit: 44V/45V/46V/47V/48V/49V/50V/51V	
rechargeVoltages = [440, 450, 460, 470, 480, 490, 500, 510]
# nnn - battery_redischarge_voltage - Battery re-discharged voltage when utility is available	n: 0~9, unit: 0.1V
# Selectable value
# 12V unit: 00.0V/12V/12.3V/12.5V/12.8V/13V/13.3V/13.5V/13.8V/14V/14.3V/14.5
# 24V unit: 00.0V/24V/24.5V/25V/25.5V/26V/26.5V/27V/27.5V/28V/28.5V/29V
# 48V unit: 00.0V/48V/49V/50V/51V/52V/53V/54V/55V/56V/57V/58V
redischargeVoltages = [0, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580]

# ^S015MCHGVmmm,nnn<CRC><cr>: Set battery maximum charge voltage
# mmm - Battery constant charge voltage (C.V.) mmm: 480 ~ 584, unit: 0.1V
# nnn - Battery float charge voltage nnn: 480 ~ 594, unit: 0.1V
CONF_BATTERY_CHARGE_VOLTAGES = "battery_charge_voltages"

# ^S010PSDVmmm<CRC><cr>: Set battery cut-off voltage
# mmm - 400 ~ 480, unit: 0.1V
CONF_BATTERY_CUTOFF_VOLTAGE = "battery_cutoff_voltage"

# ^S018DATyymmddhhffss<cr>: Set date time
# ymdhfs {0 -9}
CONF_DATETIME = "datetime"

# ^S016ACCTaaaa,bbbb<cr>: Set AC charge time bucket
# aaaa - Start time for enable AC charger working	aaaa: HH:MM(hour : minute)
# bbbb - Ending time for enable AC charger working	bbbb: HH:MM(hour : minute)
CONF_CHARGE_TIME_BUCKET = "charge_time_bucket"

# ^S016ACLTaaaa,bbbb<cr>: Set AC supply load time bucket
# aaaa - Start time for enable AC supply the load	aaaa: HH:MM(hour : minute)
# bbbb - Ending time for enable AC supply the load	bbbb: HH:MM(hour : minute)
CONF_LOAD_SUPPLY_TIME_BUCKET = "load_supply_time_bucket"

# ^S008Vnnnn<CRC><cr>: Set AC output rated voltage
# nnnn - voltage: unit: 0.1V, nnnn:1100, 1200 ? 2200 / 2300
CONF_AC_OUTPUT_VOLTAGE = "ac_output_voltage"

# ^S007RSaa<CRC><cr>: Set Country Regulations State
# aa - LV: 00：101v range，01：110v range，02：120v range HV: 00: India, 01: Gemany, 02: South American district

# ^S018LEDEn<CRC><cr>: Set On/Off control for RGB LED (only for inifin V IV)
# n - On/Off control for RGB LED	0: disable, 1: enable
# ... and couple of more

TYPES = {
    CONF_BATTERY_TYPE: (
        [0, 1, 2, 3, 5, 6, 8, 9], 
        "^S007PBTm%d"
    ),
    CONF_MAX_CHARGING_CURRENT: (
        [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120],
        "^S013MCHGC0,%03d",
    ),
    CONF_MAX_AC_CHARGING_CURRENT: (
        [2, 10, 20, 30, 40, 50, 60, 70, 80, 90],
        "^S013MUCHGC0,%02d",
    ),
    CONF_BATTERY_REDISANDCHARGE_VOLTAGES: (
        [*rechargeVoltages, *redischargeVoltages],
        "^S014BUCD%03d,%03d"
    ),
    CONF_BATTERY_CHARGE_VOLTAGES: (
        [*range(480, 594)],
        "^S015MCHGV%03d,%03d"
    ),
    CONF_BATTERY_CUTOFF_VOLTAGE: (
        [*range(400, 480)],
        "^S010PSDV%03d",
    ),
    CONF_AC_OUTPUT_VOLTAGE: (
        [*range(400, 480)],
        "^S008Vnnnn%04d",
    ),
}

CONFIG_SCHEMA = PIPSOLAR_COMPONENT_SCHEMA.extend(
    {
        cv.Optional(type): output.FLOAT_OUTPUT_SCHEMA.extend(
            {
                cv.Required(CONF_ID): cv.declare_id(PipsolarOutput),
                cv.Optional(CONF_POSSIBLE_VALUES, default=values): cv.All(
                    cv.ensure_list(cv.positive_float), cv.Length(min=1)
                ),
            }
        )
        for type, (values, _) in TYPES.items()
    }
)


async def to_code(config):
    paren = await cg.get_variable(config[CONF_PIPSOLAR_ID])

    for type, (_, command) in TYPES.items():
        if type in config:
            conf = config[type]
            var = cg.new_Pvariable(conf[CONF_ID])
            await output.register_output(var, conf)
            cg.add(var.set_parent(paren))
            cg.add(var.set_set_command(command))
            if (CONF_POSSIBLE_VALUES) in conf:
                cg.add(var.set_possible_values(conf[CONF_POSSIBLE_VALUES]))


@automation.register_action(
    "output.pipsolar.set_level",
    SetOutputAction,
    cv.Schema(
        {
            cv.Required(CONF_ID): cv.use_id(CONF_ID),
            cv.Required(CONF_VALUE): cv.templatable(cv.positive_float),
        }
    ),
)
def output_pipsolar_set_level_to_code(config, action_id, template_arg, args):
    paren = yield cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    template_ = yield cg.templatable(config[CONF_VALUE], args, float)
    cg.add(var.set_level(template_))
    yield var
