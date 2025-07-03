import sys
import socket
from datetime import datetime
import threading

# function to scan a port
def scan_port(target,port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port)) # error indicator - if 0, port is open
        if result == 0:
            print(f"port {port} is open")
            s.close()
    except socket.error as e:
        print(f"socket error on port {port}: {e}")
    except Exception as e:
        print(f"unexpected error on port {port}: {e}")


#main function - argument validation and target definition
def main():
    if len(sys.argv) == 2:
        target = sys.argv[1]
    else:
        print("invalid number of arguments")
        print("usage: python.exe scanner.py <target>")
        sys.exit(1)

    # resolve target hostname to an IP address
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"unable to resolve hostname {target}")
        sys.exit(1)

    # add a pretty banner
    print("-" * 50)
    print(f"scanning target {target_ip}")
    print(f"time started: {datetime.now()}")
    print("-" * 50)

    try:
        # use multithreading to scan ports concurrently
        threads = []
        for port in range(1,65536):
            thread = threading.Thread(target=scan_port, args=(target_ip, port))
            threads.append(thread)
            thread.start()

        # wait for all threads to complete
        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        print("\nExiting program.")
        sys.exit(0)

    except socket.error as e:
        print(f"socket error: {e}")
        sys.exit(1)

    print("\nscan completed!")

if __name__ == "__main__":
    main()