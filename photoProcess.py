from subprocess import Popen
from imgurpython import ImgurClient
from os.path import basename
from firebase import firebase
import requests

IMGUR_CLIENT_ID = 'ede560b54cbbca2'
IMGUR_CLINET_SECRET = '92ccea0c918c5769ba7ad28904bf14d59d5ce597'
IMGUR_ALBUM_DELETEHASH = 'bavG8RxBuOHoMcs'

FIREBASE_SECRET = '9SxGgVAA60TXNHGIwBx72PP2kGOpBmQrpF7kcd9o'

class PhotoProcess:

    def __init__(self):
        auth = firebase.FirebaseAuthentication(FIREBASE_SECRET, None, admin=True)

        self.__client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLINET_SECRET)
        self.__firebaseRef = firebase.FirebaseApplication('https://ntuaf-hand.firebaseio.com/', authentication=auth)

    def takePic(self):
        out, err = Popen(['gphoto2', '--capture-image-and-download', '--no-keep', \
            '--filename', './public/images/photos/photo-%Y%m%d-%H%M%S.JPG'], \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        # if success it'll have 3 lines of message
        # 1st: New file is in location ... on the camera
        # 2nd: Saving file as ...
        # 3rd: Deleting file ...
        # 4th: \n

        if out:
            filename = out.split('\n')[1].split()[-1]
            self.setFileName(filename)
        else:
            raise RuntimeError('There is some problem. Can\'t take picture')

        return self.getFileName


    def uploadPic(self, fullpath):
        result = self.__client.upload_from_path(fullpath, {'album': IMGUR_ALBUM_DELETEHASH})
        payload = {'hits': 0, 'imgur_link': result.link, 'realpath': fullpath}
        self.__firebaseRef.put('/photos', result.id, payload)
        return result.link
