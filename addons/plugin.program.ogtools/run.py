####################################################
############       GLOBAL IMPORTS     ##############
####################################################

import xbmc
import xbmcgui
import os
import time
import common


####################################################
############      GLOBAL VARIABLES    ##############
####################################################

TESTING_MODE       = False


id_OGT             = 'plugin.program.ogtools'
id_repo67          = 'repository.repo67'
id_beta67          = 'repository.repo67beta'
id_koding          = 'script.module.python.koding.aio'

repo67_zip_url1    = "https://archive.org/download/ogmcapp_gmail_Ogt/repo67.zip"
repo67_zip_url2    = "http://optimusgreen.tk/tools/Repo67.zip"
repo67_zip_url3    = "http://optimusgreen.com/tools/Repo67.zip"
beta67_zip_url1    = "http://optimusgreen.com/repo67/repository.repo67beta.zip"
repo67_xml_url     = "https://raw.githubusercontent.com/OptimusGREEN/repo67/master/_repository/addons.xml"


init_message1      = "Please wait while the repo and dependencies are installed and activated."
init_message2      = "This could take a few of minutes."

HOME               = xbmc.translatePath('special://home/')
dialog             = xbmcgui.Dialog()
dpbg               = xbmcgui.DialogProgressBG()
dp                 = xbmcgui.DialogProgress()

TITLE              = "OptimusGREEN Tools"
Ver_Current        = common.check_addon_current_ver(id_OGT)
Ver_Latest         = common.check_addon_latest_ver(id_OGT, repo67_xml_url)


################################################################################
################################################################################
#####                         Tools Update Check                           #####
################################################################################
################################################################################

if TESTING_MODE:
    id_repo67       = id_beta67
    repo67_zip_url1 = beta67_zip_url1
    # repo67_zip_url2 = beta67_zip_url2
    # repo67_zip_url3 = beta67_zip_url3

def initialise():
    if not common.compare_versions(Ver_Current, Ver_Latest):
        xbmc.log("#################   OGTOOLS INSTALLER SERVICE: FUNCTION: Initialise - CODE: 1 - OGTools Up To Date : Hmmmmm you shouldn't be seeing this ###########################", xbmc.LOGNOTICE)
        quit()
    else:
        common.markTerritory()
        popUpDisplay(first="true")
        if xbmc.getCondVisibility("System.HasAddon(%s)" % id_repo67):
            xbmc.log("#################   OGTOOLS INSTALLER SERVICE:  FUNCTION: Initialise - CODE: 2 - OGTools Update Available : Refreshing Addons ###########################", xbmc.LOGNOTICE)
            xbmc.executebuiltin("UpdateAddonRepos()")
            xbmc.executebuiltin("UpdateLocalAddons()")
            common.dis_or_enable_addon(id_repo67, enable="true")
            xbmc.log("#################   OGTOOLS INSTALLER SERVICE:  FUNCTION: Initialise - CODE: 3 - Entering The Loop ###########################", xbmc.LOGNOTICE)
        else:
            if common.url_exists(repo67_zip_url1):
                url = repo67_zip_url1
            elif common.url_exists(repo67_zip_url2):
                url = repo67_zip_url2
            elif common.url_exists(repo67_zip_url3):
                url = repo67_zip_url3
            xbmc.log("#################   OGTOOLS INSTALLER SERVICE:  FUNCTION: Initialise - CODE: 4 - Get repo 67 dirty using %s ###########################" % (url), xbmc.LOGNOTICE)
            common.get_Addon('repo67', url)
            xbmc.executebuiltin("UpdateLocalAddons()")
            time.sleep(2)
            xbmc.log("#################   OGTOOLS INSTALLER SERVICE:  FUNCTION: Initialise - CODE: 5 - Enabling Repo67 %s ###########################" % (url), xbmc.LOGNOTICE)
            common.dis_or_enable_addon(id_repo67, enable="true")
            xbmc.log("#################   OGTOOLS INSTALLER SERVICE:  FUNCTION: Initialise - CODE: 6 - Awaiting Part 2 and OGT Service Starting ###########################", xbmc.LOGNOTICE)



def popUpDisplay(first=None, second=None):
    if first:
        fn = os.path.join(os.path.dirname(__file__), 'gtr.jpg')
        xbmc.executebuiltin('ShowPicture(%s)' % (fn))
    elif second:
        if not first:
            fn = os.path.join(os.path.dirname(__file__), 'fanart.jpg')
            xbmc.executebuiltin('ShowPicture(%s)' % (fn))
