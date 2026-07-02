# functions.py
"""
Her fonksiyon, ham data_list'i (seri porttan gelen string parçaları)
işleyip anlamlı isimlerle (key) bir dict döndürür. Hangi key'in hangi
göstergeye/etikete gideceği artık burada değil, indicators_config.py
içindeki indicatorsList'te tanımlıdır.
"""


def servoValues(data_list):
    # TODO: gerçek parse mantığı data_list'in formatına göre yazılacak.
    # Şimdilik hocanın verdiği örnek sabit değerlerle iskelet:
    if not data_list:
        return {"pos": 0, "setPt": 0, "srvStatus": 0, "sensorStatus": 0}

    return {
        "pos": float(data_list[0]) if len(data_list) > 0 else 0,
        "setPt": float(data_list[1]) if len(data_list) > 1 else 0,
        "srvStatus": data_list[2] if len(data_list) > 2 else "0",
        "sensorStatus": data_list[3] if len(data_list) > 3 else "0",
    }


def speedValues(data_list):
    if not data_list:
        return {"speed": 0}
    return {"speed": float(data_list[0]) * 0.005}


def tempValues(data_list):
    if not data_list:
        return {"temp": 0}
    return {"temp": (float(data_list[0]) * 0.005) - 10}


def altValues(data_list):
    if not data_list:
        return {"alt": 0}
    return {"alt": float(data_list[0])}
    

# --- FARKLI TİPLERİ AYNI ANDA GETİREN FONKSİYON ÖRNEKLERİ ---
# Tek fonksiyon, birden fazla FARKLI tip widget'ı aynı anda besleyebilir.
# indicators_config.py'de aynı fonksiyon adına birden fazla satır tanımlayarak
# hangi key'in hangi widget'a (hangi tipte olursa olsun) gideceğini eşliyoruz.

def flightStatus(data_list):
    """Hız + sıcaklık + irtifa + bir gauge + iki metin durumu aynı anda."""
    if not data_list:
        return {"spd": 0, "tmp": 0, "alt": 0, "roll": 0, "engineStatus": "0", "gpsStatus": "0"}

    def _f(idx, default=0.0):
        try:
            return float(data_list[idx])
        except (IndexError, ValueError):
            return default

    return {
        "spd": _f(0) * 0.005,           # -> speedometer
        "tmp": (_f(1) * 0.005) - 10,    # -> thermometer
        "alt": _f(2),                   # -> altitude bar
        "roll": _f(3),                  # -> gauge (-15..15 gibi)
        "engineStatus": data_list[4] if len(data_list) > 4 else "0",   # -> düz metin
        "gpsStatus": data_list[5] if len(data_list) > 5 else "0",      # -> düz metin
    }


def servoAndTemp(data_list):
    """Servo pozisyonu (gauge) + ortam sıcaklığı (thermometer) birlikte."""
    if not data_list:
        return {"servoPos": 0, "ambientTemp": 0}

    def _f(idx, default=0.0):
        try:
            return float(data_list[idx])
        except (IndexError, ValueError):
            return default

    return {
        "servoPos": _f(0),
        "ambientTemp": (_f(1) * 0.01) - 10, 
    }