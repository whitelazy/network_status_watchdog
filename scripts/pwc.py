import network_tools
import discover
import argparse
import time
import datetime


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--network_test_url', help='default uri : http://clients3.google.com/generate_204', default='http://clients3.google.com/generate_204')
    parser.add_argument('--network_timeout', help='default: 5', default=5)
    parser.add_argument('-d', '--device', help='default SP2', default='SP2')
    parser.add_argument('--host', help='device host (default: none, discoversy device)')
    parser.add_argument('--mac', help='device mac address')
    parser.add_argument('--type', help='device type, (default=0x2712 SP2)', default=0x753e)
    parser.add_argument('--timeout', help='device discovery timeout, default=5', default=5)
    return  parser.parse_args()


def main():
    args = init_args()
    if args.host is None:
        dev = discover.discover(args.device, timeout=args.timeout)
    else:
        if args.type is str:
            type = int(args.type, 0)
        else:
            type = args.type
        dev = discover.gendevice(type, args.host, bytearray.fromhex(args.mac))

    if dev is None:
        print('No device founded')
        exit(1)
    #
    # print(dev.host)
    # print(''.join('{:02x}'.format(x) for x in dev.mac))

    if network_tools.check_network_connection(url=args.network_test_url, timeout=args.network_timeout):
        print("{} Network status is good!".format(datetime.datetime.now()))
    else:
        print("{} Network status is disconnected\nreset cable modem".format(datetime.datetime.now()))
        dev.auth()
        print("Power Off")
        dev.set_power(False)
        time.sleep(2)
        print("Power On")
        dev.set_power(True)

    print("\n\n")


if __name__ == "__main__":
    main()


