import xbmc
import os


def isTOGBinstalled():
    ogb_check = xbmc.translatePath("special://home/userdata/ogbversion.xml")
    if os.path.exists(ogb_check):
        return True
    else:
        return False



if isTOGBinstalled():
    xbmc.executebuiltin("Skin.SetBool(%s)" % ("isBuildInstalled"))
else:
    xbmc.executebuiltin("Skin.Reset(%s)" % ("isBuildInstalled"))
