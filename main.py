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
    formatted_url = f"rdp+ntlm-password://{user}:{password}@{url}"
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
    
    qtclient = EvilRDPGUI([url ,user, password, site_url], settings)
    return qtclient

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
        *[{"host": f"TECH5-{str(i).zfill(2)}NEW", "user": "BENGURION\StudentT5", "password": ""} for i in range(1, 31)],
        *[{"host": f"TECH2-{str(i).zfill(2)}NEW", "user": "BENGURION\StudentT2", "password": ""} for i in range(1, 31)],
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
    
    if viable_addresses:
        app = QApplication(sys.argv)
        windows = []
        for address in viable_addresses:
            window = create_rdp_gui(address["host"], address["user"], address["password"], "https://youtube.com")
            window.show()
            windows.append(window)
        
        app.exec_()
        qApp.quit()
    else:
        print("\nNo viable RDP addresses found.")

if __name__ == "__main__":
    main()