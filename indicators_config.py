"""Configuration module for telemetry indicators and data routing mappings.

This module defines the blueprint instances for various graphical indicators
(such as gauges, speedometers, and thermometers) along with their operating
ranges. It also maps telemetry parsing functions to their respective output
keys and graphical widgets, dictating how data is visually represented on
the user interface.

Attributes:
    servoGauge_1 (IndicatorWidget): A gauge indicator ranging from -10 to +10.
    servoGauge_2 (IndicatorWidget): A gauge indicator ranging from -15 to +15.
    rollGauge (IndicatorWidget): A gauge indicator ranging from -15 to +15.
    speedometer_ind (IndicatorWidget): A speedometer ranging from 0 to 50.
    thermometer_ind (IndicatorWidget): A thermometer ranging from -10 to 40.
    altitude_ind (IndicatorWidget): An altitude bar ranging from 0 to 3000.
    indicatorsList (list of list): A mapping table dictating the UI layout. 
        Format: [function_name, data_key, indicator_instance, display_label].
        Multiple rows with the same function name are rendered simultaneously.
        An indicator value of None results in a text-only status display.
    FUNCTION_DISPLAY_NAMES (dict): A dictionary for overriding internal function 
        names with custom UI display text.
"""

from indicator_widgets import IndicatorWidget

# Define indicator blueprints: type, minimum value, maximum value
servoGauge_1    = IndicatorWidget("gauge", -10, +10)
servoGauge_2    = IndicatorWidget("gauge", -15, +15)
rollGauge       = IndicatorWidget("gauge", -15, +15)
speedometer_ind = IndicatorWidget("speedometer", 0, 50)
thermometer_ind = IndicatorWidget("thermometer", -30, 60)
altitude_ind    = IndicatorWidget("altitude", 0, 3000)
artificial_horizon = IndicatorWidget("artificial_horizon", 0, 30)
lidar_alt_ind = IndicatorWidget("altitude",0,200)
pitot_speed_ind = IndicatorWidget("speedometer",0,30)


# Configuration mapping: [parser_function_name, output_key, widget_blueprint, ui_label]
indicatorsList = [
    ["servoValues", "pos",           servoGauge_1, "Position"],
    ["servoValues", "setPt",         servoGauge_2, "Setpoint"],
    ["servoValues", "srvStatus",     None,         "Servo Status"],
    ["servoValues", "sensorStatus",  None,         "Sensor Status"],

    ["speedValues", "speed",         speedometer_ind, "Speed(km/h)"],
    ["tempValues",  "temp",          thermometer_ind, "Temp(°C)"],
    ["altValues",   "alt",           altitude_ind,    "Altitude(m)"],

    # Combined routing: One function populates multiple diverse widgets and text flags simultaneously
    ["flightStatus", "spd",            speedometer_ind, "Speed(km/h)"],
    ["flightStatus", "tmp",            thermometer_ind, "Temp(°C)"],
    ["flightStatus", "alt",            altitude_ind,    "Altitude(m)"],
    ["flightStatus", "roll",           rollGauge,        "Gauge(V)"],
    ["flightStatus", "engineStatus",   None,             "Engine"],
    ["flightStatus", "gpsStatus",      None,             "GPS"],
    
    ["servoAndTemp", "servoPos",       servoGauge_1,     "Servo Pos"],
    ["servoAndTemp", "ambientTemp",    thermometer_ind,  "Ambient Temp"],
    ["attitudeValues", "attitude",     artificial_horizon, "Artificial Horizon(pitch,roll)"],
    ["lidar_function","lidar_distance", lidar_alt_ind, "Lidar Alt(m)"],
    ["pitot_function","pitot_speed",pitot_speed_ind,  "Airspeed(m/s)"],
    ["pitot_function","temperature", thermometer_ind, "Pitot Temp(°C)"]
]

FUNCTION_DISPLAY_NAMES = {}
