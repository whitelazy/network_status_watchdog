import network_tools
import discover
import argparse
import time


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '-network_test_url', help='default uri : http://clients3.google.com/generate_204', default='http://clients3.google.com/generate_204')
    parser.add_argument('-network_timeout', help='default: 5', default=5)
    parser.add_argument('-d', '-device', help='default SP2', default='SP2')
    parser.add_argument('-a', '-address', help='device address (default: none, discoversy device)', default=None)
    parser.add_argument('-t', '-timeout', help='device discovery timeout, default=5', default=5)
    return  parser.parse_args()


def main():
    args = init_args()
    device = discover.discover(args.device, timeout=args.timeout, device_address=args.address)

    if device is None:
        print('No device founded')
        exit(1)

    if network_tools.check_network_connection():
        print("Network status is good!")
    else:
        print("Network status is disconnected\nreset cable modem")
        device.auth()
        print("Power Off")
        device.set_power(False)
        time.sleep(2)
        print("Power On")
        device.set_power(True)


if __name__ == "__main__":
    main()


