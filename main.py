import sys
import logging

from aardwolf import logger
from aardwolf.commons.iosettings import RDPIOSettings
from aardwolf.commons.queuedata.constants import VIDEO_FORMAT
#from aardwolf.extensions.RDPEDYC.vchannels.socksoverrdp import SocksOverRDPChannel
from evilrdp._version import __banner__
from evilrdp.gui import EvilRDPGUI, RDPClientConsoleSettings
#from evilrdp.consolehelper import EVILRDPConsole
from PyQt5.QtWidgets import QApplication, qApp
    
def run(url, user, password, site_url):
    formatted_url = f"rdp+plain://{user}@{url}"
    logger.setLevel(logging.INFO)

    height = 1024
    width = 768

    iosettings = RDPIOSettings()
    iosettings.video_width = width
    iosettings.video_height = height
    iosettings.video_out_format = VIDEO_FORMAT.PIL
    iosettings.client_keyboard = 'enus'

    #from evilrdp.vchannels.pscmd import PSCMDChannel
    #iosettings.vchannels['PSCMD'] = PSCMDChannel('PSCMD')
    #from aardwolf.extensions.RDPEDYC.vchannels.socksoverrdp import SocksOverRDPChannel
    #iosettings.vchannels['PROXY'] = SocksOverRDPChannel(args.sockschannel, args.socksip, args.socksport)


    settings = RDPClientConsoleSettings(formatted_url, iosettings)
    settings.mhover = True
    settings.keyboard = True

    app = QApplication(sys.argv)
    qtclient = EvilRDPGUI([user, password, site_url],settings)
    qtclient.show()
    app.exec_()
    qApp.quit()

run("localhost:3389","Docker","admin", "https://youtube.com")

