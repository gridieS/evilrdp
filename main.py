import sys
import logging
import socket
import concurrent.futures

from aardwolf import logger
from aardwolf.commons.iosettings import RDPIOSettings
from aardwolf.commons.queuedata.constants import VIDEO_FORMAT
from evilrdp.gui import EvilRDPGUI, RDPClientConsoleSettings
from PyQt5.QtWidgets import QApplication, qApp

def create_rdp_gui(url, user, password, site_url):
    """
    This function creates and returns an EvilRDPGUI instance.
    It does NOT start the application loop.
    """
    formatted_url = f"rdp+plain://{user}@{url}"
    logger.setLevel(logging.INFO)
    
    height = 1024
    width = 768

    iosettings = RDPIOSettings()
    iosettings.video_width = width
    iosettings.video_height = height
    iosettings.video_out_format = VIDEO_FORMAT.PIL
    iosettings.client_keyboard = 'enus'
    
    settings = RDPClientConsoleSettings(formatted_url, iosettings)
    settings.mhover = True
    settings.keyboard = True
    
    qtclient = EvilRDPGUI([user, password, site_url], settings)
    return qtclient

# This is the worker function for checking ports. It is safe to run this in a thread.
def check_port_open(host, port, timeout=10):
    """Checks if a given port is open on a host."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # 1 second timeout
        result = sock.connect_ex((host, port))
        if result == 0:
            return True
        else:
            return False
    except socket.error as e:
        return False
    finally:
        sock.close()

def main():
    """
    The main function of the program.
    """
    ADDRESSES = [
        *[{"host": f"TECH5-{str(i).zfill(2)}NEW", "user": "StudentT5", "password": ""} for i in range(1, 41)],
        *[{"host": f"TECH2-{str(i).zfill(2)}NEW", "user": "StudentT2", "password": ""} for i in range(1, 41)],
        {"host": "localhost", "user": "Docker", "password": "admin"},
        {"host": "peerdebian", "user": "Docker", "password": "admin"}
    ]
    PORT = 3389

    viable_addresses = []
    
    for address in ADDRESSES:
        host = address["host"]
        if check_port_open(host, PORT):
            print(f"Port open at {host}, adding to list...")
            viable_addresses.append(address)
        else:
            print(f"Port closed at {host}")
    
    # This is the new part.
    if viable_addresses:
        app = QApplication(sys.argv)
        windows = []
        for address in viable_addresses:
            window = create_rdp_gui(address["host"], address["user"], address["password"], "https://youtube.com")
            window.show()
            windows.append(window)
        
        # The single call to app.exec_() manages all open windows.
        app.exec_()
        qApp.quit()
    else:
        print("\nNo viable RDP addresses found.")

if __name__ == "__main__":
    main()