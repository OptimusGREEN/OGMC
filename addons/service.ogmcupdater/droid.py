import xbmc, xbmcgui, os

dialog              = xbmcgui.Dialog()





################################################################################
################################################################################
#####                             Android                                  #####
################################################################################
################################################################################


def get_android_codename():
    if '14' in get_build_prop_api():
        return 'Ice Cream Sandwitch'
    elif '15' in get_build_prop_api():
        return 'Ice Cream Sandwitch'
    elif '16' in get_build_prop_api():
        return 'Jelly Bean'
    elif '17' in get_build_prop_api():
        return 'Jelly Bean'
    elif '18' in get_build_prop_api():
        return 'Jelly Bean'
    elif '19' in get_build_prop_api():
        return 'KitKat'
    elif '20' in get_build_prop_api():
        return 'KitKat'
    elif '21' in get_build_prop_api():
        return 'Lollipop'
    elif '22' in get_build_prop_api():
        return 'Lollipop'
    elif '23' in get_build_prop_api():
        return 'Marshmallow'
    elif '24' in get_build_prop_api():
        return 'Nougat'
    elif '25' in get_build_prop_api():
        return 'Nougat'
    else:
        return 'Unknown'


def check_build_prob_path():
    pathA = '/system/build.prop'
    if os.path.exists(pathA):
        dialog.ok("[COLORgreen]OptimusGREEN Tools[/COLOR]", "Build Prop Path Exists"," ","Using Path A")
    else:
        dialog.ok("[COLORgreen]OptimusGREEN Tools[/COLOR]", "Build Prop Path INACCESSIBLE"," ","Using Path A")
    # text = file_reader(pathA)
    # release                = 'OS Version:[COLORgold] %s[/COLOR]' % (text)
    # dialog.ok("[COLORgreen]OptimusGREEN Tools[/COLOR]", "[COLORgold]OPERATING SYSTEM DETAILS[/COLOR]","",""+release)


def get_build_prop_release():
    prop    = '/system/build.prop'
    rstr       = 'ro.build.version.release'
    with open(prop) as f:
        content = f.readlines()
    for line in content:
        line = line.strip('\n')
        line = line.strip('\r')
        # xbmc.log('################# The line is : %s' % (line))
        if rstr in line:
            release = line.split("=", 1)[1]
            f.close()
            return release


def get_build_prop_api():
    prop    = '/system/build.prop'
    apistr = 'ro.build.version.sdk'
    with open(prop) as f:
        content = f.readlines()
    for line in content:
        line = line.strip('\n')
        line = line.strip('\r')
        # xbmc.log('################# The line is : %s' % (line))
        if apistr in line:
            api = line.split("=", 1)[1]
            f.close()
            return api


def show_api_release():
    myapi     = get_build_prop_api()
    myrelease = get_build_prop_release()
    api                    = 'API:[COLORgold] %s[/COLOR]' % (myapi)
    release                = 'Android Version:[COLORgold] %s[/COLOR]' % (myrelease)
    dialog.ok("[COLORgreen]OptimusGREEN Tools[/COLOR]", "[COLORgold]OPERATING SYSTEM DETAILS[/COLOR]"," "+release," "+api)


def get_new_ogmc_path():
    if os.path.exists('/storage/emulated/0/Android/data/'):
        return '/storage/emulated/0/Android/data/tk.optimusgreen.ogmc/files/.ogmc/'
    elif os.path.exists('/storage/sdcard0/Android/data/'):
        return '/storage/sdcard0/Android/data/tk.optimusgreen.ogmc/files/.ogmc/'
    elif os.path.exists('/sdcard/Android/data/'):
        return '/sdcard/Android/data/tk.optimusgreen.ogmc/files/.ogmc/'
    else:
        xbmc.log('UNABLE TO FIND ANDROID PATH TO OGMC')


def get_old_ogmc_path():
    if os.path.exists('/storage/emulated/0/Android/data/'):
        return '/storage/emulated/0/Android/data/tk.optimusgreen.ogmc/files/.kodi/'
    elif os.path.exists('/storage/sdcard0/Android/data/'):
        return '/storage/sdcard0/Android/data/tk.optimusgreen.ogmc/files/.kodi/'
    elif os.path.exists('/sdcard/Android/data/'):
        return '/sdcard/Android/data/tk.optimusgreen.ogmc/files/.kodi/'
    else:
        xbmc.log('UNABLE TO FIND ANDROID PATH TO OGMC')


def get_dlfolder_path():
    if os.path.exists('/storage/emulated/0/Android/data/'):
        return '/storage/emulated/0/Download'
    elif os.path.exists('/storage/sdcard0/Android/data/'):
        return '/storage/sdcard0/Download'
    elif os.path.exists('/storage/sdcard0/Android/data/'):
        return '/sdcard/Download'
    else:
        xbmc.log('UNABLE TO FIND ANDROID DOWNLOAD DIRECTORY')


def android_path_details():
    newogmc            = 'new: %s' % (get_new_ogmc_path())
    oldogmc            = 'old: %s' % (get_old_ogmc_path())
    dlpath             = 'dl: %s' % (get_dlfolder_path())
    dialog.ok("[COLORgreen]OptimusGREEN Tools[/COLOR]", "new,old,dl",""+newogmc+" - "+oldogmc,""+dlpath)


def android_ver_details(): 
    codname                = 'Codename: %s' % (get_android_codename())
    release                = 'Version: %s' % (get_build_prop_release())
    sdk                    = 'API: %s' % (get_build_prop_api())
    dialog.ok("[COLORgreen]OptimusGREEN Tools[/COLOR]", "Android OS Details",""+codname,""+release+"\n"+sdk)


def do_old_and_new_ogmc_exist():
    if not os.path.exists(get_new_ogmc_path()):
        return False
    elif not os.path.exists(get_old_ogmc_path()):
        return False
    else:
        return True