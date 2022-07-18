import pysftp
import os

host = '<enter host here>'
port = 22
username = '<username>'
password = '<password>'

latest = 0
latestfile = None

# From a security perspective, this is not wise to do but I never fixed it properly...
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

with pysftp.Connection(host=host, username=username, password=password, cnopts=cnopts) as sftp:
    for fileattr in sftp.listdir_attr():
        if fileattr.st_mtime > latest:
            latest = fileattr.st_mtime
            latestfile = fileattr.filename
            localFilePath = "/IT8951-ePaper/Raspberry/pic/1440x1072_0.bmp"

    if latestfile is not None:
        local_modification_time = os.path.getmtime(localFilePath)

        # Compare the last image on the FTP with the local file, retrieve file if image is newer on ftp than on local FS
        if latest > local_modification_time:
            print("downloading file", latestfile)
            sftp.get(latestfile, "/IT8951-ePaper/Raspberry/pic/" + latestfile)
            print("success fetching", latestfile)

            # showing new image on e-paper screen
            cmd = 'sudo /home/pi/photoframe/IT8951-ePaper/Raspberry/epd -2.30 0'
            os.system(cmd)

        else:
            print("no newer file available")
