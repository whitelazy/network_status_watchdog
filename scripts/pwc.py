from scripts.status_notifier import notify
from scripts.network_tools import check_network_connection
from scripts.discover import discover, gendevice
from scripts.utils import get_datetime_string, set_default_timezone
import argparse
import time
from pytz import timezone


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--network_test_url', help='default uri : http://clients3.google.com/generate_204', default='http://clients3.google.com/generate_204')
    parser.add_argument('--network_timeout', help='default: 5', default=5)
    parser.add_argument('-d', '--device', help='default SP2', default='SP2')
    parser.add_argument('--host', help='device host (default: none, discoversy device)')
    parser.add_argument('--mac', help='device mac address')
    parser.add_argument('--type', help='device type, (default=0x2712 SP2)', default=0x753e)
    parser.add_argument('--timeout', help='device discovery timeout, default=5', default=5)
    parser.add_argument('--name', help='device alias')
    parser.add_argument('-s', '--slack', help='slack incoming webhooc url')
    parser.add_argument('--timezone')
    return parser.parse_args()


def main():
    print("\n\n")
    args = init_args()
    if args.host is None:
        dev = discover(args.device, timeout=args.timeout)
    else:
        if args.type is str:
            dev_type = int(args.type, 0)
        else:
            dev_type = args.type
        dev = gendevice(dev_type, args.host, bytearray.fromhex(args.mac))

    if dev is None:
        print('No device founded')
        exit(1)

    # print(dev.host)
    # print(''.join('{:02x}'.format(x) for x in dev.mac))

    if args.timezone:
        set_default_timezone(timezone(args.timezone))

    if check_network_connection(url=args.network_test_url, timeout=args.network_timeout):
        print("{} Network status is good!".format(get_datetime_string()))
    else:
        print("{} Network status is disconnected\nreset cable modem".format(get_datetime_string()))
        dev.auth()
        print("Power Off")
        dev.set_power(False)
        time.sleep(2)
        print("Power On")
        dev.set_power(True)

        print('wait for network connected')
        for i in range(0, 300, 5):
            print('check network connection status')
            args.network_test_url = 'http://clients3.google.com/generate_204'
            if check_network_connection(url=args.network_test_url, timeout=args.network_timeout):
                print('network connected')
                targets = {}
                if args.slack:
                    targets['slack'] = args.slack

                notify('Network recovered', args.name, targets)
                exit(0)
                break
            else:
                time.sleep(5)
        print('network recovery failed')
        exit(1)


if __name__ == "__main__":
    main()


