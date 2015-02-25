from sys import argv


def print_usage():
    print('Usage: python server.py <port>')


def server():
    if len(argv) < 2:
        print_usage()
        return
    port = argv[1]
    print('Port: ', port)

# Hvis vi kjører filen med `python server.py`
if __name__ == '__main__':
    server()
