# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
from subprocess import run
import json
import psutil
#
from readsources import get_sources_from

repertoire_selon_disque = [
    # {'dest': "mypassport",
    #  'repertoire': "rsync_02.06.23"},
    {'dest': "Secure_HDD",
     'repertoire': "rsync_11.04.24"},
    {'dest': "intenso",
     'repertoire': "rsync_02.06.23"},
]
def determine_target():

    f_out = open('output.txt', 'w')
    if True:
        with f_out :
            command = ['lsblk',  '--json']  # '--list-columns', '-S',
            run(command, stdout=f_out)
    else:  # except:
        print('ERREUR !')
    f_out.close()

    f_in = open('output.txt', 'r')
    content = f_in.read()
    f_in.close()
    donnees = json.loads(content)

    blockdevices = donnees['blockdevices']

    # for blockdevice in blockdevices:
    #     for k in blockdevice.keys():
    #         print(k, blockdevice[k])
    #     print('------')

    external_disk_name = \
        this_mountpoint = \
        repertoire = None

    for blockdevice in blockdevices:
        if blockdevice['name'] in ("sdb", "sdc"): #
            for child in blockdevice['children']:
                # print(child['name'])

                for mountpoint in child['mountpoints']:
                    external_disk_name = mountpoint.split('/')[-1]
                    this_mountpoint = mountpoint
                    break

                for entry in repertoire_selon_disque:
                    if external_disk_name == entry['dest']:
                        repertoire = entry['repertoire']
                        break

        if external_disk_name is not None and \
                this_mountpoint is not None and \
                repertoire is not None:
            break

    return external_disk_name, this_mountpoint , repertoire


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    external_disk_name, this_mountpoint , repertoire = determine_target()
    if external_disk_name is not None and repertoire is not None:
        print('\trsynch to:', ' external_disk_name: {}, this_mountpoint: {}, repertoire: {}'.format(external_disk_name, this_mountpoint, repertoire))
    else:
        print('External disk not found or not allowed. Exiting')
        exit()

    sources = get_sources_from('sources.txt')
    if len(sources) == 0:
        print('No source found. Exiting')
        exit()

    # sources = [
    #     "/home/pp/Documents",
    #     "/home/pp/dev",
    #     "/home/pp/.pyzo",
    #     "/home/pp/pico",
    #     "/home/pp/ash",
    #     "/home/pp/Bureau",
    #     "/home/pp/Musique",
    #     "/home/pp/.ssh",
    #     "/home/pp/Images",
    #     "/home/pp/Vidéos",
    #     "/home/pp/Modèles",
    #     "/home/pp/Public",
    #     "/home/pp/Téléchargements",
    #     "/home/pp/appimage"
    # ]

    # # cwd = os.getcwd()
    # # print("Current working directory:", cwd)
    for source in sources:
        # commande_ = r'rsync -a {source} "{this_mountpoint}/{repertoire}"'.format(source=source, this_mountpoint=this_mountpoint, repertoire=repertoire)
        # print(commande_)

        commande_rsynch = ['rsync', '-a', source, "{this_mountpoint}/{repertoire}".format(this_mountpoint=this_mountpoint, repertoire=repertoire) ]
        print(' '.join(a for a in commande_rsynch))
        try:
            proc = psutil.Popen(commande_rsynch).wait()
        except:
            print('erreur')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


