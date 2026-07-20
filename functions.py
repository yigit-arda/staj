import struct 

def _safe_get(data_list, index, default=0.0):
    """Safely extracts a value from a list at a given index and converts it to float.

    Args:
        data_list (list): The source list containing raw data strings or numbers.
        index (int): The target index position to access.
        default (float, optional): Fallback value if an index error or conversion 
            error occurs. Defaults to 0.0.

    Returns:
        float: The extracted float value, or the default value upon failure.
    """
    try:
        return float(data_list[index])
    except (IndexError, ValueError):
        return default


def servoValues(data_list):
    """Parses servo position, setpoint, and status values from raw telemetry data.

    Maps the 0-10000 raw input range onto specific coordinate boundaries tailored 
    for visualization components.

    Args:
        data_list (list): Raw telemetry fields where index 0 is position, index 1 
            is setpoint, index 2 is servo status, and index 3 is sensor status.

    Returns:
        dict: Parsed telemetry packet containing mapped position, setpoint, 
            and status string indicators.
    """
    if not data_list:
        return {"pos": 0.0, "setPt": 0.0, "srvStatus": "0", "sensorStatus": "0"}

    # Use 5000.0 as default so gauges center themselves at 0.0 if data is missing
    raw_pos = _safe_get(data_list, 0, default=5000.0)
    raw_setpt = _safe_get(data_list, 1, default=5000.0)

    # Map raw 0-10000 range to a physical range of -10.0 to +10.0
    mapped_pos = round((raw_pos * 0.002) - 10.0, 2)
    # Map raw 0-10000 range to a physical range of -15.0 to +15.0
    mapped_setpt = round((raw_setpt * 0.003) - 15.0, 2)

    return {
        "pos": mapped_pos,
        "setPt": mapped_setpt,
        "srvStatus": data_list[2] if len(data_list) > 2 else "0",
        "sensorStatus": data_list[3] if len(data_list) > 3 else "0",
    }


def speedValues(data_list):
    """Extracts and scales speed information from telemetry data.

    Args:
        data_list (list): Raw telemetry fields where index 0 is raw speed.

    Returns:
        dict: Dictionary containing the scaled speed value under the key 'speed'.
    """
    if not data_list:
        return {"speed": 0.0}
    return {"speed": round(_safe_get(data_list, 0) * 0.005, 2)}


def tempValues(data_list):
    """Extracts and scales temperature metrics from telemetry data.

    Args:
        data_list (list): Raw telemetry fields where index 0 is raw temperature.

    Returns:
        dict: Dictionary containing the scaled temperature value under the key 'temp'.
    """
    if not data_list:
        return {"temp": 0.0}
    return {"temp": round((_safe_get(data_list, 0) * 0.005) - 10, 2)}


def altValues(data_list):
    """Extracts and formats altitude readings from telemetry data.

    Args:
        data_list (list): Raw telemetry fields where index 0 is raw altitude.

    Returns:
        dict: Dictionary containing the formatted altitude value under the key 'alt'.
    """
    if not data_list:
        return {"alt": 0.0}
    return {"alt": round(_safe_get(data_list, 0), 2)}


def flightStatus(data_list):
    """Extracts combined flight metrics including speed, temperature, altitude, and status codes.

    Processes multiple instrument parameters packed within a single telemetry frame.

    Args:
        data_list (list): Raw sequence fields mapped as: index 0 (speed), 
            index 1 (temp), index 2 (altitude), index 3 (roll), index 4 (engine), 
            and index 5 (gps).

    Returns:
        dict: A comprehensive overview dictionary containing scaled metrics and status keys.
    """
    if not data_list:
        return {"spd": 0.0, "tmp": 0.0, "alt": 0.0, "roll": 0.0, "engineStatus": "0", "gpsStatus": "0"}

    # Use 5000.0 as default so gauge centers itself at 0.0 if data is missing
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
    """Extracts a combined payload dataset for servo positioning and ambient temperature.

    Args:
        data_list (list): Raw telemetry fields where index 0 is raw servo position 
            and index 1 is raw ambient temperature.

    Returns:
        dict: Parsed dictionary containing 'servoPos' and 'ambientTemp' keys.
    """
    if not data_list:
        return {"servoPos": 0.0, "ambientTemp": 0.0}

    # Use 5000.0 as default so gauge centers itself at 0.0 if data is missing
    raw_pos = _safe_get(data_list, 0, default=5000.0)
    mapped_pos = round((raw_pos * 0.002) - 10.0, 2)

    # Convert raw data into temperature metric using a standard 0.005 scaling coefficient
    ambient_temp = round((_safe_get(data_list, 1) * 0.005) - 10, 2)

    return {
        "servoPos": mapped_pos,
        "ambientTemp": ambient_temp,
    }

def attitudeValues(data_list):
    """Parses and scales pitch and roll data for the artificial horizon indicator.

    Extracts raw orientation metrics from the telemetry payload, applies a scaling 
    transformation to map the values to a physical degree range, and packs them 
    into a single tuple for the widget to unpack.

    Args:
        data_list (list): Raw telemetry fields where index 0 is the raw pitch 
            value and index 1 is the raw roll value.

    Returns:
        dict: A dictionary containing a tuple of scaled (pitch, roll) values 
            under the key 'attitude'.
    """
    if not data_list or len(data_list) < 2:
        return {"attitude": (0.0, 0.0)} 

    raw_pitch = _safe_get(data_list, 0, default=5000.0) 
    mapped_pitch = round((raw_pitch * 0.006 - 30), 2)
    
    raw_roll = _safe_get(data_list, 1, default=5000.0)
    mapped_roll = round((raw_roll * 0.006 - 30), 2)

    return {
        "attitude": (mapped_pitch, mapped_roll)
    }


def lidar_function(data_list):
    """Parses and scales Lidar distance from raw telemetry data."""
    if not data_list:
        return {"lidar_distance": 0.0}

    try:
        # VALIDATION: Remove any empty or whitespace-only elements
        clean_data = [x for x in data_list if str(x).strip() != '']
        
        if len(clean_data) < 4:
            return {"lidar_distance": 0.0}

        target_data = clean_data[0:4]
        
        if isinstance(target_data[0], str):
            raw_bytes = bytes([int(x, 16) if 'x' in x.lower() else int(x) for x in target_data])
        else:
            raw_bytes = bytes(target_data)
        
        distance = struct.unpack('<f', raw_bytes)[0]
        return {"lidar_distance": round(distance, 2)}
    
    except Exception as e:
        # Log the exception for debugging instead of failing silently
        print(f"[WARNING] Corrupt Lidar Packet Discarded. Error: {e} | Data: {data_list}")
        return {"lidar_distance": 0.0}


def pitot_function(data_list):
    """Parses airspeed and temperature metrics from raw Pitot telemetry data."""
    if not data_list:
        return {"pitot_speed": 0.0, "temperature": 0}

    try:
        # VALIDATION: Remove any empty or whitespace-only elements
        clean_data = [x for x in data_list if str(x).strip() != '']
        
        if len(clean_data) < 6:
            return {"pitot_speed": 0.0, "temperature": 0}

        speed_data = clean_data[0:4]
        temp_data = clean_data[4:6]
        
        if isinstance(speed_data[0], str):
            speed_bytes = bytes([int(x, 16) if 'x' in x.lower() else int(x) for x in speed_data])
        else:
            speed_bytes = bytes(speed_data)

        if isinstance(temp_data[0], str):
            temp_bytes = bytes([int(x, 16) if 'x' in x.lower() else int(x) for x in temp_data])
        else:
            temp_bytes = bytes(temp_data)
        
        pitot_speed = struct.unpack('<f', speed_bytes)[0]
        temperature = struct.unpack('<h', temp_bytes)[0]
        temperature = temperature / 1000.0
        
        return {
            "pitot_speed": round(pitot_speed, 2),
            "temperature": temperature
        }
        
    except Exception as e:
        # Log the exception for debugging instead of failing silently
        print(f"[WARNING] Corrupt Pitot Packet Discarded. Error: {e} | Data: {data_list}")
        return {"pitot_speed": 0.0, "temperature": 0}
