import urllib.request
import sys


def check_network_connection(url='http://clients3.google.com/generate_204', timeout=5):
    try:
        print('Sending request to {}'.format(url))
        response = urllib.request.urlopen(url, timeout=timeout)

        status = response.status
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        # Generally using a catch-all is a bad practice but
        # I think it's ok in this case
        print(e)
        print('Request to {} failed'.format(url))
        status = 0

    if status == 204:
        return True
    else:
        return False


def test():
    print(check_network_connection())


if __name__ == "__main__":
    test()

