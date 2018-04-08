import broadlink_custom


def discover(device, timeout=5):
    devices = broadlink_custom.discover(timeout=timeout)
    filtered = list(filter(lambda x: x.type == device, devices))
    if len(filtered) == 0:
        return None
    else:
        return filtered[0]


def gendevice(type, host, mac):
    return broadlink_custom.gendevice(type, (host, 80), mac)