# indicators_config.py
"""
Burada:
  1) Kullanılacak gösterge "tarifleri" (tip + min/max) tanımlanır.
  2) indicatorsList: her satır bir (fonksiyon_adı, veri_key'i, gösterge, etiket)
     eşlemesidir. Aynı fonksiyon_adı ile birden fazla satır olabilir; bir
     fonksiyon seçildiğinde o fonksiyon_adına sahip TÜM satırlar aynı anda
     bar üzerinde gösterilir.
  
  widget alanı None ise, o key sadece metin (durum/flag) olarak gösterilir,
  hiçbir gösterge widget'ı çizilmez.
"""

from indicator_widgets import IndicatorWidget

# --- type, minVal, maxVal ---
servoGauge_1    = IndicatorWidget("gauge", -10, +10)
servoGauge_2    = IndicatorWidget("gauge", -15, +15)
rollGauge       = IndicatorWidget("gauge", -15, +15)
speedometer_ind = IndicatorWidget("speedometer", 0, 50)
thermometer_ind = IndicatorWidget("thermometer", -10, 40)
altitude_ind    = IndicatorWidget("altitude", 0, 3000)

# [function_adı, key_adı, indicator, etiket]
indicatorsList = [
    ["servoValues", "pos",           servoGauge_1, "Position"],
    ["servoValues", "setPt",         servoGauge_2, "Setpoint"],
    ["servoValues", "srvStatus",     None,         "Servo Status"],
    ["servoValues", "sensorStatus",  None,         "Sensor Status"],

    ["speedValues", "speed",         speedometer_ind, "Speed"],
    ["tempValues",  "temp",          thermometer_ind, "Temp"],
    ["altValues",   "alt",           altitude_ind,    "Altitude"],

    # --- Aynı fonksiyon, FARKLI tip widget'ları aynı anda besliyor ---
    ["flightStatus", "spd",            speedometer_ind, "Speed"],
    ["flightStatus", "tmp",            thermometer_ind, "Temp"],
    ["flightStatus", "alt",            altitude_ind,    "Altitude"],
    ["flightStatus", "roll",           rollGauge,        "Roll"],
    ["flightStatus", "engineStatus",   None,             "Engine"],
    ["flightStatus", "gpsStatus",      None,             "GPS"],

    ["servoAndTemp", "servoPos",       servoGauge_1,     "Servo Pos"],
    ["servoAndTemp", "ambientTemp",    thermometer_ind,  "Ambient Temp"],
]

FUNCTION_DISPLAY_NAMES = {}
