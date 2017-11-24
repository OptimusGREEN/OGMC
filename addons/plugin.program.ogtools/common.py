####################################################
############       GLOBAL IMPORTS     ##############
####################################################

import xbmc
import xbmcaddon
import xbmcgui
import urllib
import os
import urllib2
import downloader
import time
import extract


####################################################
############      GLOBAL VARIABLES    ##############
####################################################


HOME   = xbmc.translatePath('special://home/')
ADDONS = xbmc.translatePath('special://home/addons/')
dialog = xbmcgui.Dialog()
dpbg   = xbmcgui.DialogProgressBG()
dp     = xbmcgui.DialogProgress()


####################################################
############          FUNCTIONS       ##############
####################################################


############    DETERMINE PLATFORM    ##############


def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'


############        URL TOOLS        ##############


def url_exists(url):
    request = urllib2.Request(url)
    request.get_method = lambda: 'HEAD'
    try:
        urllib2.urlopen(request)
        return True
    except:
        return False


############         VERSIONS         ##############

def check_addon_latest_ver(addonID, repo_addonsfile_url):
    addonline = 'addon id="%s"' % (addonID)
    saved = xbmc.translatePath("special://home/userdata/repoaddonsfile.txt")
    if not url_exists(repo_addonsfile_url):
        return False
    urllib.urlretrieve(repo_addonsfile_url, saved)
    with open(saved) as f:
        content = f.readlines()
    for line in content:
        line = line.strip('\n')
        line = line.strip('\r')
        if addonline in line:
            prever = line.split('version="', 1)[1]
            ver = prever.split('" provider', 1)[0]
            f.close()
            os.remove(saved)
            return ver


def check_addon_current_ver(addonID):
    Addon = xbmcaddon.Addon(addonID)
    ver = Addon.getAddonInfo('version')
    return ver


def addon_update_avail(addonID, repo_addonsfile_url):
    current = check_addon_current_ver(addonID)
    latest = check_addon_latest_ver(addonID, repo_addonsfile_url)
    if latest is False:
        return False
    elif compare_versions(current, latest):
        return True
    else:
        return False


def compare_versions(current, latest):
    from distutils.version import LooseVersion
    if LooseVersion(current) < LooseVersion(latest):
        return True
    else:
        return False


############         Misc       ##############

def isAddonInstalled(addonID):
    path = os.path.join(ADDONS, addonID)
    if os.path.exists(path):
        return True
    else:
        return False


def getInfo(label):
    try:
        return xbmc.getInfoLabel(label)
    except:
        return False


def dis_or_enable_addon(addon_id, enable="true"):  # code by Q
    import json
    addon = '"%s"' % addon_id
    if xbmc.getCondVisibility("System.HasAddon(%s)" % addon_id) and enable == "true":
        return xbmc.log("### Skipped %s, reason = allready enabled" % addon_id)
    elif not xbmc.getCondVisibility("System.HasAddon(%s)" % addon_id) and enable == "false":
        return xbmc.log("### Skipped %s, reason = not installed" % addon_id)
    else:
        do_json = '{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{"addonid":%s,"enabled":%s}}' % (addon, enable)
        query = xbmc.executeJSONRPC(do_json)
        response = json.loads(query)
        if enable == "true":
            xbmc.log("### Enabled %s, response = %s" % (addon_id, response))
        else:
            xbmc.log("### Disabled %s, response = %s" % (addon_id, response))
    # return xbmc.executebuiltin('Container.Update(%s)' % xbmc.getInfoLabel('Container.FolderPath'))


def get_Addon(name, url):
    path = xbmc.translatePath(os.path.join('special://home/addons', 'packages'))
    lib = os.path.join(path, name + '.zip')
    try:
        os.remove(lib)
    except:
        pass
    downloader.download(url, lib)
    addonfolder = xbmc.translatePath('special://home/addons/')
    time.sleep(2)
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib, addonfolder)


def makeFile(file, text):
    xbmc.log("########### MAKING FILE : Writing %s to %s" % (text, file))
    write_file = open(file, 'w')
    write_file.write(text)
    write_file.close()


def markTerritory():
    file = os.path.join(HOME, "preInstallerPissStain.txt")
    text = "This is a temporary file which will be removed upon addon update."
    if not os.path.exists(file):
        makeFile(file, text)
