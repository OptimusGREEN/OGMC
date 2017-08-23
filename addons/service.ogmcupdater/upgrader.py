import xbmcgui, xbmc
import urllib
import os
import shutil

def download(url, dest, dp = None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("[COLORgreen]The OptimusGREEN Build[/COLOR]","Downloading & Copying Files",' ', ' ')
    dp.update(0)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))

def _pbhook(numblocks, blocksize, filesize, url, dp):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled():
        raise Exception("Canceled")
        dp.close()





################################################################################
################################################################################
#####                Build Upgrade to new codename version                 #####
################################################################################
################################################################################

def build_upgrader(url,url2):
    dialog    = xbmcgui.Dialog()
    ogb_check = xbmc.translatePath("special://home/userdata/ogbversion.xml")
    add_lst   = 'https://www.dropbox.com/s/tqyytq10ylks5uu/addon_list.txt?dl=1'
    name      = "The_OptimusGREEN_Build"
    dp        = xbmcgui.DialogProgress()
    

    dp.create("[COLORgreen]The OptimusGREEN Build Installer[/COLOR]", "Checking server 1.......")
    if file_exists(url) is True:
        OGB_installer(name, url)
    else:
        dp.update(0,"Checking Server 2......")
        if file_exists(url2) is True:
            OGB_installer(name, url2)
        else:
            dp.update(0,"WOW!! Both servers are unreachable, Please try again later.")
            time.sleep(5)
            dp.update(0,"[COLORred]The app will now close[/COLOR], Closing.......")
            xbmc.executebuiltin("Quit")



def OGB_installer(name,url):
    dialog        = xbmcgui.Dialog()
    home_fldr   = xbmc.translatePath(os.path.join('special://','home'))
    addons_fldr = xbmc.translatePath('special://home/addons')
    device_q = dialog.yesno("[COLORgreen]OptimusGREEN Installer[/COLOR]", "Please Choose A Build", "[COLORgreen]FULL FAT[/COLOR] - Everything included. For more powerful devices.", "[COLORgreen]SEMI-SKIMMED[/COLOR] - Lighter for low end devices like fire stick 1 and boxes with 1gb ram.","Full Fat","Semi-Skimmed")
    if device_q == True:
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        dp        = xbmcgui.DialogProgress()
        dp.create("[COLORgreen]The OptimusGREEN Build[/COLOR]","Processing.... ",'', 'Please Wait')
        dp.update(0,"", "[COLORgold]Downloading.....[/COLOR]")
        lib=os.path.join(path, name+'.zip')
        try:
           os.remove(lib)
        except:
           pass
        download(url, lib, dp)
        time.sleep(2)
        dp.update(0,"", "[COLORgold]Extracting Zip Please Wait[/COLOR]")
        print '======================================='
        print addonfolder
        print '======================================='
        extract.all(lib,home_fldr,dp)
        LtL_install(addons_fldr)
        purge_old_stuff_auto(addons_fldr)
    else:
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        dp = xbmcgui.DialogProgress()
        dp.create("[COLORgreen]The OptimusGREEN Build[/COLOR]","Processing.... ",'', 'Please Wait')
        dp.update(0,"", "[COLORgold]Downloading.....[/COLOR]")
        lib=os.path.join(path, name+'.zip')
        try:
           os.remove(lib)
        except:
           pass
        download(url, lib, dp)
        addonfolder = xbmc.translatePath(os.path.join('special://','home'))
        time.sleep(2)
        dp.update(0,"", "[COLORgold]Extracting Zip Please Wait[/COLOR]")
        print '======================================='
        print addonfolder
        print '======================================='
        extract.all(lib,home_fldr,dp)
        purge_old_stuff_auto(addons_fldr)
        

################################################################################
################################################################################
#####                             Cleanup tools                            #####
################################################################################
################################################################################

def LtL_install(local_folder):
    remote_file   = 'https://www.dropbox.com/s/xs3lltbe5mq3yz1/LtL.txt?dl=1'
    ogtools       = 'plugin.program.ogtools'
    path          = xbmc.translatePath('special://home/userdata/addon_data/plugin.program.ogtools')
    remote        = xbmc.translatePath("special://home/userdata/addon_data/plugin.program.ogtools/ltl.txt")
    addon_data    = xbmc.translatePath('special://home/userdata/addon_data/')
    addons        = xbmc.translatePath('special://home/userdata/addons/')
    dialog        = xbmcgui.Dialog()
    dp            = xbmcgui.DialogProgress()
    remote_list   = []
    local_list    = []
    dp.create('[COLORgreen]OptimusGREEN Tools[/COLOR]', 'Lightening The Load...')
    if not os.path.exists(path):
        os.mkdir(path)
    urllib.urlretrieve(remote_file, remote)
    xbmc.log('### retrieving %s to %s' % (remote_file, remote))
    rfile = open(remote, 'r')
    for dirs in os.listdir(local_folder):
        if os.path.isfile(dirs):
            pass
        else:
            local_list.append(dirs)
            xbmc.log('### adding %s to %s' % ('local dirs', local_list))
        for line in rfile.readlines():
            line = line.strip('\n')
            line = line.strip('\r')
            remote_list.append(line)
            xbmc.log('### copying %s to %s' % ('file lines', remote_list))
    theload = [x for x in local_list if x in remote_list]

    for item in theload:
        path = os.path.join(local_folder, item)
        if os.path.isfile(path) == True:
            pass
        elif 'packages' in path:
            pass
        else:
            shutil.rmtree(path)
            xbmc.log('### removing %s from %s' % (item, local_folder))
    rfile.close()
    dp.close()


def purge_old_stuff_auto(local_folder):
    remote_file   = 'https://www.dropbox.com/s/tqyytq10ylks5uu/addon_list.txt?dl=1'
    remote        = xbmc.translatePath("special://home/userdata/addon_data/plugin.program.ogtools/remote_file.txt")
    addons        = xbmc.translatePath('special://home/addons/')
    addon_data    = xbmc.translatePath('special://home/userdata/addon_data/')
    dialog        = xbmcgui.Dialog()
    dp            = xbmcgui.DialogProgress()
    local_list    = []
    remote_list   = []
    
    dp.create('[COLORgreen]OptimusGREEN Tools[/COLOR]', 'Purging old build data...')
    urllib.urlretrieve(remote_file, remote)
    xbmc.log('### retrieving %s to %s' % (remote_file, remote))
    rfile = open(remote, 'r')
    for dirs in os.listdir(local_folder):
        if os.path.isfile(dirs):
            pass
        else:
            local_list.append(dirs)
            xbmc.log('### adding %s to %s' % ('local dirs', local_list))
    for line in rfile.readlines():
        line = line.strip('\n')
        line = line.strip('\r')
        remote_list.append(line)
        xbmc.log('### copying %s to %s' % ('file lines', remote_list))
    leftovers = [x for x in local_list if x not in remote_list]

    for item in leftovers:
        path = os.path.join(local_folder, item)
        if os.path.isfile(path) == True:
            pass
        else:
            shutil.rmtree(path)
            xbmc.log('### removing %s from %s' % (item, local_folder))
    else:
        pass
    rfile.close()
    dp.close()