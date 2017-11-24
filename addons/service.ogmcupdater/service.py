import xbmc

app  = 'tk.optimusgreen.ogmc'
home = xbmc.translatePath("special://home/")

##########################
###DETERMINE PLATFORM#####
##########################

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


def selfDestruct():
    if platform() == 'android':
        pass
    else:
        import shutil, os, time
        try: shutil.rmtree(os.path.join(home,"addons/service.ogmcupdater/"))
        except: pass
        time.sleep(1)
        xbmc.executebuiltin('UpdateLocalAddons()')
        time.sleep(1)
        xbmc.executebuiltin('UpdateAddonRepos()')
        time.sleep(1)
        xbmc.executebuiltin("ReloadSkin()")
        quit()

##########################
###    RUN SERVICE   #####
##########################

selfDestruct()

if not app in home:
    quit()

from isAddonUpToDate import addon_update_avail

if addon_update_avail("service.ogmcupdater", "http://raw.github.com/OptimusGREEN/OGMC_repo/master/_repository/addons.xml"):
    xbmc.executebuiltin("UpdateAddonRepos()")
    xbmc.executebuiltin("UpdateLocalAddons()")
    quit()

from common import vers_upgrade_check

if app in home:
    vers_upgrade_check()
else:
    exit()
    xbmc.log('####### NOT OGMC - STOPPING UPDATER SERVICE #######')



