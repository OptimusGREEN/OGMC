import os, xbmcaddon, urllib, urllib2, xbmc
from distutils.version import LooseVersion


################################################################################
################################################################################
#####                   Check if addon is up-to-date                       #####
################################################################################
################################################################################

def addon_update_avail(addonID, repo_addonsfile_url):
    current = check_addon_current_ver(addonID)
    latest = check_addon_latest_ver(addonID, repo_addonsfile_url)
    if not latest:
        return False
    elif compare_versions(current, latest):
        return True
    else:
        return False

def check_addon_latest_ver(addonID, repo_addonsfile_url):
    addonline = 'addon id="%s"' % (addonID)
    saved = xbmc.translatePath("special://home/userdata/repoaddonsfile.txt")
    if not url_exists(repo_addonsfile_url):
        return False
    urllib.urlretrieve(repo_addonsfile_url, saved)
    if os.path.exists(saved):
        try:
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
        except:
            xbmc.log("#################  OGMC Updater: check_addon_latest_ver: couldn't read file    #####################")


def check_addon_current_ver(addonID):
    Addon = xbmcaddon.Addon(addonID)
    ver = Addon.getAddonInfo('version')
    return ver



def compare_versions(current, latest):
    if LooseVersion(current) < LooseVersion(latest):
        return True
    else:
        return False


def url_exists(url):
    request = urllib2.Request(url)
    request.get_method = lambda: 'HEAD'
    try:
        response = urllib2.urlopen(request)
        return True
    except:
        return False
################################################################################
################################################################################
#####                           Call using This                            #####
################################################################################
################################################################################


# if addon_update_avail("putYour_AddonIDhere", "putYour_RepoAddonsXML_url_Here"):
#     xbmc.executebuiltin("UpdateAddonRepos()")
#     xbmc.executebuiltin("UpdateLocalAddons()")