import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs,time
import urllib, urllib2
from distutils.version import LooseVersion
from upgrader import build_upgrader
import droid


installed2       = xbmc.translatePath("special://home/userdata/ogmc_installed.txt")
latest           = xbmc.translatePath("special://home/userdata/ogmc_latest.txt")
installed        = xbmc.translatePath("special://xbmc/userdata/ogmc_installed_version.txt")
codename         = xbmc.translatePath("special://xbmc/userdata/ogmc_codename.txt")

upgrade_minapi   = 21
thisapi          = int(droid.get_build_prop_api())

if thisapi < upgrade_minapi:
    maxapi_jarv      = 20
    ogmc_url         = 'https://archive.org/download/Legacy_Archive/OGMC/Jarvis/OGMC_Jarvis_Legacy.apk'
else:
    ogmc_url         = 'https://archive.org/download/OGMCLatest/OGMC_Latest.apk'
    ogmc_pvr_url     = 'https://archive.org/download/OGMCLatest/OGMC_PVR_Latest.apk'
    
build_url1       = "https://archive.org/download/OptimusGREENbuildLATEST/OptimusGREENbuildLATEST.zip"
build_url2       = "https://www.dropbox.com/s/kd1r1cqpcgnzglq/OptimusGREENbuildLATEST.zip?dl=1"





################################################################################
################################################################################
#####                            Read File                                 #####
################################################################################
################################################################################

def file_reader(filename):
    readfile = open(filename, 'r')
    content  = readfile.read()
    readfile.close()
    return content

################################################################################
################################################################################
#####                            Write File                                #####
################################################################################
################################################################################

def file_writer(current, new):
    read_file = open(new, 'r')
    write_file = open(current, 'w')
    reader = read_file.read()
    write_file.write(reader)
    read_file.close()
    write_file.close()

################################################################################
################################################################################
#####                            Checker                                   #####
################################################################################
################################################################################

def vers_upgrade_check():
    dialog              = xbmcgui.Dialog()
    dpbg      = xbmcgui.DialogProgressBG()
    codename_latest_url = 'https://www.dropbox.com/s/efl9yvs3t5qtxbx/ogmc_latest_codename.txt?dl=1'
    codename_file       = xbmc.translatePath("special://home/userdata/codename_latest.txt")

    if not os.path.exists(codename):
        codename_current = 'Jarvis'
        xbmc.log('#######    OGMC - CODENAME FILE DOESN\'T EXIST - THEREFOR MUST BE JARVIS     #######')
    else:
        codename_current  = file_reader(codename)
        xbmc.log('#######    OGMC - READING CODENAME FILE     #######')

    if file_exists(codename_latest_url) is False:
        dpbg.create("[COLORgreen]OGMC[/COLOR] [COLORred]Server timed out[/COLOR]")
        time.sleep(2)
        dpbg.close()
        quit()
        xbmc.log('####### OGMC - COULDN\'T RETRIEVE ONLINE CODENAME FILE #######')
    else:
        pass
    
    urllib.urlretrieve(codename_latest_url, codename_file)
    xbmc.log('#######    OGMC - DOWNLOADING CODENAME FILE   #######')
    codename_latest   = file_reader(codename_file)

    if thisapi < upgrade_minapi:
        if not codename_latest == 'Jarvis':
            xbmc.log('###################################   OGMC - This device\' API is %s and minimum API is %s : Your device OS is too old to upgrade to the new version of OGMC. Starting Legacy Checker.  #########################################' % (thisapi,upgrade_minapi))
            legacy_update_checker()
            quit()
    else:
        pass

    xbmc.log('###################################   OGMC - This device\' API is %s and minimum API is %s : Continuing Upgrade Check  #########################################' % (thisapi,upgrade_minapi))
    if codename_current == codename_latest:
        xbmc.log('####### CODENAMES MATCH - RUNNING STANDARD UPDATE CHECKER #######')
        update_checker()
    elif 'Jarvis' in codename_current and 'Krypton' in codename_latest:
        upgrade_q = dialog.yesno("[COLORgreen]OGMC Updater[/COLOR]", "OGMC Krypton is now available for upgrade.", "The existing version of OGMC will soon be discontinued.", "A build upgrade will also be required.","Later","Upgrade")
        if upgrade_q == True:
            xbmc.log('####### OGMC VERSION JUMP COMMENCING #######')
            ogmc_ver_jump(ogmc_url)
        else:
            xbmc.log('####### OGMC VERSION FILES DIDN\'T MATCH AND WERE ALSO NOT WHAT THEY WERE SUPPOSED TO BE #######')
            quit()
            xbmc.log('####### OGMC VERSION FILES DIDN\'T MATCH AND WERE ALSO NOT WHAT THEY WERE SUPPOSED TO BE #######')
    elif 'Krypton' in codename_current and 'Jarvis' in codename_latest:
        dpbg.create("[COLORgreen]OGMC[/COLOR] [COLORred]BETA CODENAME - ENDING.[/COLOR]")
        time.sleep(4)
        dpbg.close()
        xbmc.log('#######    OGMC - BETA CODENAME - ENDING     #######')
    else:
        dpbg.create("[COLORgreen]OGMC[/COLOR] [COLORred]Unable to check for updates to OGMC at this time.[/COLOR]")
        time.sleep(4)
        dpbg.close()
        xbmc.log('#######    OGMC - CHECK LINE 104 OF COMMON - EXITING   #######')
        quit()

    


def update_checker():
    name      = 'ogmcupdate'
    path      = xbmc.translatePath('special://home/userdata/')
    dialog    = xbmcgui.Dialog()
    dpbg      = xbmcgui.DialogProgressBG()
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(installed):
        ask = dialog.yesno("[COLORgreen]OGMC Updater[/COLOR]", "Hmmm! Your OGMC version seems corrupt", "If this app is OGMC then you need to update to the new version", "Is this OGMC or another app like Kodi/SPMC?","OTHER","OGMC")
        if ask == True:
            ogmc(ogmc_url)
            exit()
        else:
            ask2 = dialog.ok("[COLORgreen]OGMC Updater[/COLOR]", "This updater should only be installed on the OGMC Android app.", "Please disable this add-on in settings or uninstall to avoid this dialog in the future.")
            exit()
    url_latest = 'https://www.dropbox.com/s/xgdv0fwrekgktgw/ogmc_latest.txt?dl=1'
    if file_exists(url_latest) is False:
        dpbg.create("[COLORgreen]OGMC[/COLOR] [COLORred]Server timed out[/COLOR]")
        time.sleep(2)
        dpbg.close()
        quit()
    else:
        pass
    urllib.urlretrieve(url_latest, latest)
    xbmc.log('#######    OGMC - Getting Lastest Version File     #######')
    file_current  = file_reader(installed)
    file_latest   = file_reader(latest)
    if LooseVersion(file_current) == LooseVersion(file_latest):
        xbmc.log('#######    OGMC - You are running the latest version    #######')
        pass
    elif LooseVersion(file_current) > LooseVersion(file_latest):
        dpbg.create("[COLORgreen]OGMC Updater[/COLOR]", "You are running a beta version of OGMC")
        xbmc.log('#######    OGMC - You are running a beta version    #######')
        time.sleep(5)
        dpbg.close()
    else:
        xbmc.log('#######    OGMC - Starting updater   #######')
        ogmc(ogmc_url)

# For devices that can't run the latest version
def legacy_update_checker():
    # checker
    name      = 'ogmcupdate'
    path      = xbmc.translatePath('special://home/userdata/')
    dialog    = xbmcgui.Dialog()
    dpbg      = xbmcgui.DialogProgressBG()
    if not thisapi <= maxapi_jarv:
        xbmc.log('#######    OGMC - Legacy Checker quitting as your API can run the latest version. lease report this to us.     #######')
        quit()
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(installed):
        ask = dialog.yesno("[COLORgreen]OGMC Legacy Updater[/COLOR]", "Hmmm! Your OGMC version seems corrupt", "If this app is OGMC then you need to update to the new version", "Is this OGMC or another app like Kodi/SPMC?","OTHER","OGMC")
        if ask == True:
            ogmc(ogmc_url)
            exit()
        else:
            ask2 = dialog.ok("[COLORgreen]OGMC Legacy Updater[/COLOR]", "This updater should only be installed on the OGMC Android app.", "Please disable this add-on in settings or uninstall to avoid this dialog in the future.")
            exit()
    url_latest = 'https://www.dropbox.com/s/qxyl5ffy8mey6c5/ogmc_legacy_version.txt?dl=1'
    if file_exists(url_latest) is False:
        dpbg.create("[COLORgreen]OGMC[/COLOR] [COLORred]Server timed out[/COLOR]")
        time.sleep(2)
        dpbg.close()
        quit()
    else:
        pass
    xbmc.log('#######    OGMC - Getting Lastest Legacy Version File     #######')
    urllib.urlretrieve(url_latest, latest)
    file_current  = file_reader(installed)
    file_latest   = file_reader(latest)
    if LooseVersion(file_current) >= LooseVersion('3.0.0'):
        xbmc.log('#######    OGMC - Checking current version (%s) with Legacy version (%s)     #######' % (file_current,file_latest))
        xbmc.log('#######    OGMC - Current version is %s so continuing to update as version file was overwritten at some point     #######' % (file_current))
        ogmc(ogmc_url,'true')
    else:
        pass
    xbmc.log('#######    OGMC - Checking current version (%s) with Legacy version (%s)     #######' % (file_current,file_latest))
    if LooseVersion(file_current) == LooseVersion(file_latest):
        xbmc.log('#######    OGMC - You are running the latest legacy version available for your device   #######')
        pass
    elif LooseVersion(file_current) > LooseVersion(file_latest):
        dpbg.create("[COLORgreen]OGMC Legacy Updater[/COLOR]", "You are running a beta version of OGMC")
        xbmc.log('#######    OGMC - You are running a beta version    #######')
        time.sleep(5)
        dpbg.close()
    else:
        xbmc.log('#######    OGMC - Starting legacy updater   #######')
        ogmc(ogmc_url,'true')


def file_exists(url):
    request = urllib2.Request(url)
    request.get_method = lambda : 'HEAD'
    try:
        response = urllib2.urlopen(request)
        return True
    except:
        return False

################################################################################
################################################################################
#####                            Updater                                   #####
################################################################################
################################################################################

def ogmc(url,leg='false'):
    newver   = file_reader(latest)
    dp       = xbmcgui.DialogProgress()
    dest     = xbmc.translatePath("special://home/addons/packages/OGMCLatest.apk")
    dialog   = xbmcgui.Dialog()
    update_q = dialog.yesno("[COLORgreen]OGMC Updater[/COLOR]", "[COLORgold]UPDATE AVAILABLE:[/COLOR] Version %s of OGMC is available." % (newver.split("r", 1)[0]), "It is always advised to run the latest version.", "Would you like to download the update now?","Later","Download")
    if update_q == True:
        
        if leg == 'false':
            if dialog.yesno("[COLORgreen]OGMC Updater[/COLOR]", "Would you like to install the standard or pvr version?", "Please select standard if you are unsure.", "","STANDARD","PVR"):
                url   = ogmc_pvr_url
            
        dp.create('[COLORgreen]OGMC DOWNLOADER[/COLOR]', '')
        
        if leg == 'true':
            dp.update(0,'Downloading: [COLORgold]OGMC Legacy v%s[/COLOR]' % (newver.split("r", 1)[0]))
        else:
            if url == ogmc_pvr_url:
                dp.update(0,'Downloading: [COLORgold]OGMC v%s PVR[/COLOR]' % (newver.split("r", 1)[0]))
            else:
                dp.update(0,'Downloading: [COLORgold]OGMC v%s[/COLOR]' % (newver.split("r", 1)[0]))

        xbmc.log('#######    OGMC - Downloading from : %s     #######' % (url))
        download(url,dest,dp)
        # urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
        dialog.ok('[COLORgreen]OGMC DOWNLOADER[/COLOR]', 'Download Complete.', ' ', 'Click OK to launch the installer.')
        xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:'+dest+'")')
        xbmc.executebuiltin("Quit")
    else:
        pass

# The one below is for when the new app has the same package name but a different .folder name.

def ogmc_ver_jump(url):
    dp        = xbmcgui.DialogProgress()
    dest      = xbmc.translatePath("special://home/addons/packages/OGMCLatest.apk")
    dialog    = xbmcgui.Dialog()
    upgrade_q = dialog.yesno("[COLORgreen]OGMC Updater[/COLOR]", "It is STRONGLY ADVISED to backup your userdata.", "You can backup Userdata (Buildsafe) in OGTools.", "Would you like to update now?","Backup","Update")
    if upgrade_q == True:
        dp.create('[COLORgreen]OGMC DOWNLOADER[/COLOR]', 'Downloading the latest version of OGMC...',' ', 'Please be patient.')
        download(url,dest,dp)
        # urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
        dialog.ok('[COLORgreen]OGMC DOWNLOADER[/COLOR]', 'Download Complete.', ' ', 'Click OK to install.')
        xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:'+dest+'")')
        xbmc.executebuiltin("Quit")
    else:
        dialog.ok('[COLORgreen]OGMC Updater[/COLOR]', 'You will be taken to OGTools - Select Backup/Restore.', 'Backup your faves, trakt and userdata (OG Build safe option)', 'Restart the app after backing up to continue with upgrade.')
        xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.program.ogtools/")')

        


# The one below is for when the new app has a different package name.

# def ogmc_ver_jump(url):
#     dp        = xbmcgui.DialogProgress()
#     dest      = xbmc.translatePath("special://home/addons/packages/OGMCLatest.apk")
#     dialog    = xbmcgui.Dialog()
#     dp.create('[COLORgreen]OGMC DOWNLOADER[/COLOR]', 'Downloading the latest version of OGMC...',' ', 'Please be patient.')
#     urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
#     dialog.ok('[COLORgreen]OGMC DOWNLOADER[/COLOR]', 'Download Complete.', ' ', 'This has installed as a seperate app.')
#     dialog.ok('[COLORgreen]OGMC DOWNLOADER[/COLOR]', 'It is advised to backup your userdata in the old app.', 'Backup in OGTools (buildsafe)', 'Then restore in the new app after installing the build.')
#     xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:'+dest+'")')
#     file_writer(installed, latest)
#     killxbmc()


# The one below is for when the app has the same package name.

# def ogmc_ver_jump(url,buildurl1,buildurl2):
#     dp        = xbmcgui.DialogProgress()
#     dest      = xbmc.translatePath("special://home/addons/packages/OGMCLatest.apk")
#     dialog    = xbmcgui.Dialog()
#     dp.create('[COLORgreen]OGMC DOWNLOADER[/COLOR]', 'Downloading the latest version of OGMC...',' ', 'Please be patient.')
#     urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
#     build_upgrader(buildurl1,buildurl2)
#     dialog.ok('[COLORgreen]OGMC DOWNLOADER[/COLOR]', 'Download Complete.', ' ', 'Click OK to launch the installer.')
#     xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:'+dest+'")')
#     file_writer(installed, latest)
#     killxbmc()
    

# def _pbhook(numblocks, blocksize, filesize, url, dp):
#     try:
#         percent = min((numblocks*blocksize*100)/filesize, 100)
#         dp.update(percent)
#     except:
#         percent = 100
#         dp.update(percent)
#     if dp.iscanceled():
#         dp.close()

def download(url, dest, dp = None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("[COLORgold]Download In Progress[/COLOR]"' ',' ', ' ')
    dp.update(0)
    start_time=time.time()
    urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))

def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try:
            percent = min(numblocks * blocksize * 100 / filesize, 100)
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024)
            kbps_speed = numblocks * blocksize / (time.time() - start_time)
            if kbps_speed > 0:
                eta = (filesize - numblocks * blocksize) / kbps_speed
            else:
                eta = 0
            kbps_speed = kbps_speed / 1024
            mbps_speed = kbps_speed / 1024
            total = float(filesize) / (1024 * 1024)
            mbs = '[COLOR green]%.02f MB[/COLOR] of [COLOR white][B]%.02f MB[/B][/COLOR]' % (currently_downloaded, total)
            e = '[COLOR white][B]Speed: [/B][/COLOR][COLOR green]%.02f Mb/s ' % mbps_speed  + '[/COLOR]'
            e += '[COLOR white][B]ETA: [/B][/COLOR][COLOR green]%02d:%02d' % divmod(eta, 60)  + '[/COLOR]'
            dp.update(percent, "",mbs, e)
        except:
            percent = 100
            dp.update(percent)
        if dp.iscanceled():
            dialog.ok(AddonTitle, 'The download was cancelled.')
            dp.close()
            quit()


###############################################################
###FORCE CLOSE KODI - ANDROID ONLY WORKS IF ROOTED#############
#######LEE @ COMMUNITY BUILDS##################################

def killxbmc():
    home_f     = xbmc.translatePath('special://home/')
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android
        print "############   try android force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('adb shell am force-stop tk.optimusgreen.ogmc')
        except: pass
        try: os.system('adb shell am force-stop tk.optimusgreen.ogmc')
        except: pass
        try: os.system('adb shell am force-stop tk.optimusgreen')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass
        try: os.system('adb shell am force-stop com.semperpax.spmc16')
        except: pass
        if 'ogmc' in home_f:
            dialog.ok("[COLORgreen]Force Stop Didn't Work[/COLOR]", "You can manually [COLORred]Force Stop[/COLOR] [COLORgreen]OGMC[/COLOR] in 'app settings'.", "On the following screen, scroll to and select [COLORgreen]OGMC[/COLOR] and click [COLORred]Force Stop[/COLOR], then just re-launch the app.", "Alternatively you can just kill the power to your box/stick.")
            try: xbmc.executebuiltin('StartAndroidActivity("","android.settings.APPLICATION_DETAILS_SETTINGS","","package:tk.optimusgreen.ogmc")')
            except: pass
        elif 'spmc' in home_f:
            dialog.ok("[COLORgreen]Force Stop Didn't Work[/COLOR]", "You can manually [COLORred]Force Stop[/COLOR] [COLORmediumblue]SPMC[/COLOR] in 'app settings'.", "On the following screen, scroll to and select [COLORmediumblue]SPMC[/COLOR] and click [COLORred]Force Stop[/COLOR], then just re-launch the app.", "Alternatively you can just kill the power to your box/stick.")
            try: xbmc.executebuiltin('StartAndroidActivity("","android.settings.APPLICATION_DETAILS_SETTINGS","","package:com.semperpax.spmc16")')
            except: pass
        elif 'kodi' in home_f:
            dialog.ok("[COLORgreen]Force Stop Didn't Work[/COLOR]", "You can manually [COLORred]Force Stop[/COLOR] [COLORdeepskyblue]KODI[/COLOR] in 'app settings'.", "On the following screen, scroll to and select [COLORdeepskyblue]KODI[/COLOR] and click [COLORred]Force Stop[/COLOR], then just re-launch the app.", "Alternatively you can just kill the power to your box/stick.")
            try: xbmc.executebuiltin('StartAndroidActivity("","android.settings.APPLICATION_DETAILS_SETTINGS","","package:org.xbmc.kodi")')
            except: pass
        elif dialog.ok("[COLORgreen]Force Stop Didn't Work[/COLOR]", "You can manually [COLORred]Force Stop[/COLOR] the app in 'app settings'.", "On the following screen, scroll to and select [COLORgreen]this app[/COLOR] and click [COLORred]Force Stop[/COLOR], then just re-launch the app.", "Alternatively you can just kill the power to your box/stick."):
            try: xbmc.executebuiltin('StartAndroidActivity(,android.settings.APPLICATION_SETTINGS)')
            except: pass
        else:
            pass
        time.sleep(2)
        dialog.ok("[COLOR=green][B]Still Here?[/COLOR][/B]", "Box/Stick user should turn your device off at the mains. Alternatively, Press the HOME key on your device/remote, Settings > Apps > OGMC/Kodi/SPMC > Force Stop then open the app")
        try: xbmc.executebuiltin('StartAndroidActivity(,android.settings.APPLICATION_SETTINGS)')
        except: pass
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close [COLOR=lime]DO NOT[/COLOR] exit via the menu.","iOS detected.  Press and hold both the Sleep/Wake and Home button for at least 10 seconds, until you see the Apple logo.")

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