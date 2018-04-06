from scripts import broadlink_custom


def discover(device, timeout=5, device_address=None):
    devices = broadlink_custom.discover(timeout=timeout, local_ip_address=device_address)
    filtered = list(filter(lambda x: x.type == device, devices))
    if len(filtered) == 0:
        return None
    else:
        return filtered[0]
