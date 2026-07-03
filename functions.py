# functions.py
"""
Her fonksiyon, ham data_list'i (seri porttan gelen string parçaları)
işleyip anlamlı isimlerle (key) bir dict döndürür. Hangi key'in hangi
göstergeye/etikete gideceği artık burada değil, indicators_config.py
içindeki indicatorsList'te tanımlıdır.
"""
'''

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

    '''


# functions.py
"""
Her fonksiyon, ham data_list'i (seri porttan gelen string parçaları)
işleyip anlamlı isimlerle (key) bir dict döndürür. Hangi key'in hangi
göstergeye/etikete gideceği artık burada değil, indicators_config.py
içindeki indicatorsList'te tanımlıdır.
"""

'''
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
    return {"speed": round(float(data_list[0]) * 0.005,2)}


def tempValues(data_list):
    if not data_list:
        return {"temp": 0}
    return {"temp": round((float(data_list[0]) * 0.005) - 10,2)}


def altValues(data_list):
    if not data_list:
        return {"alt": 0}
    return {"alt":  float(data_list[0])}
    

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



    '''

# functions.py
"""
Her fonksiyon, ham data_list'i (seri porttan gelen string parçaları)
işleyip anlamlı isimlerle (key) bir dict döndürür. Hangi key'in hangi
göstergeye/etikete gideceği artık burada değil, indicators_config.py
içindeki indicatorsList'te tanımlıdır.

Sayısal değerler burada FLOAT olarak döndürülür (string değil) -
ondalık basamak formatlaması (örn. "%.2f") display_bar.py'de,
tek bir yerden yapılır. Böylece bu katman sade veri üretir,
gösterim detayına karışmaz.
"""


def _safe_get(data_list, index, default=0.0):
    """Listeden veriyi güvenli şekilde float olarak çeker; index yoksa/bozuksa default döner."""
    try:
        return float(data_list[index])
    except (IndexError, ValueError):
        return default


def servoValues(data_list):
    if not data_list:
        return {"pos": 0.0, "setPt": 0.0, "srvStatus": "0", "sensorStatus": "0"}

    # Veri gelmezse gauge'lar uca değil ortaya (0'a) düşsün diye default=5000.0
    raw_pos = _safe_get(data_list, 0, default=5000.0)
    raw_setpt = _safe_get(data_list, 1, default=5000.0)

    # pos: ham 0-10000 aralığını -> -10..+10 aralığına çeviriyoruz
    mapped_pos = round((raw_pos * 0.002) - 10.0, 2)
    # setPt: ham 0-10000 aralığını -> -15..+15 aralığına çeviriyoruz
    mapped_setpt = round((raw_setpt * 0.003) - 15.0, 2)

    return {
        "pos": mapped_pos,
        "setPt": mapped_setpt,
        "srvStatus": data_list[2] if len(data_list) > 2 else "0",
        "sensorStatus": data_list[3] if len(data_list) > 3 else "0",
    }


def speedValues(data_list):
    if not data_list:
        return {"speed": 0.0}
    return {"speed": round(_safe_get(data_list, 0) * 0.005, 2)}


def tempValues(data_list):
    if not data_list:
        return {"temp": 0.0}
    return {"temp": round((_safe_get(data_list, 0) * 0.005) - 10, 2)}


def altValues(data_list):
    if not data_list:
        return {"alt": 0.0}
    return {"alt": round(_safe_get(data_list, 0), 2)}


# --- FARKLI TİPLERİ AYNI ANDA GETİREN FONKSİYONLAR ---

def flightStatus(data_list):
    """Hız + sıcaklık + irtifa + bir gauge + iki metin durumu aynı anda."""
    if not data_list:
        return {"spd": 0.0, "tmp": 0.0, "alt": 0.0, "roll": 0.0, "engineStatus": "0", "gpsStatus": "0"}

    # roll bir gauge olduğu için veri gelmezse ortada (0'da) dursun diye default=5000.0
    raw_roll = _safe_get(data_list, 3, default=5000.0)
    mapped_roll = round((raw_roll * 0.003) - 15.0, 2)

    return {
        "spd": round(_safe_get(data_list, 0) * 0.005, 2),
        "tmp": round((_safe_get(data_list, 1) * 0.005) - 10, 2),
        "alt": round(_safe_get(data_list, 2), 2),
        "roll": mapped_roll,
        "engineStatus": data_list[4] if len(data_list) > 4 else "0",
        "gpsStatus": data_list[5] if len(data_list) > 5 else "0",
    }


def servoAndTemp(data_list):
    """Servo pozisyonu (gauge) + ortam sıcaklığı (thermometer) birlikte."""
    if not data_list:
        return {"servoPos": 0.0, "ambientTemp": 0.0}

    # servoPos bir gauge olduğu için veri gelmezse ortada (0'da) dursun diye default=5000.0
    raw_pos = _safe_get(data_list, 0, default=5000.0)
    mapped_pos = round((raw_pos * 0.002) - 10.0, 2)

    # NOT: tempValues ile aynı katsayıyı (0.005) kullandım - gerçek donanımına göre kontrol et.
    ambient_temp = round((_safe_get(data_list, 1) * 0.005) - 10, 2)

    return {
        "servoPos": mapped_pos,
        "ambientTemp": ambient_temp,
    }
