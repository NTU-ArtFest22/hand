from imgurpython import ImgurClient
from os.path import basename
from firebase import firebase
import subprocess as sp
import requests
import yaml

with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

class PhotoProcess:

    def __init__(self):
        auth = firebase.FirebaseAuthentication(config['firebase']['secret'], None, admin=True)

        self.__client = ImgurClient(config['imgur']['client_id'], config['imgur']['secret'])
        self.__firebaseRef = firebase.FirebaseApplication(config['firebase']['url'], authentication=auth)

    def take_pic(self):
        out, err = sp.Popen(['gphoto2', '--capture-image-and-download', '--no-keep', \
            '--filename', './public/images/photos/photo-%Y%m%d-%H%M%S.JPG'], \
            stdout=sp.PIPE, stderr=sp.PIPE).communicate()

        # if success it'll have 3 lines of message
        # 1st: New file is in location ... on the camera
        # 2nd: Saving file as ...
        # 3rd: Deleting file ...
        # 4th: \n

        if out:
            print out
            fullpath = out.split('\n')[1].split()[-1]
        else:
            print err
            raise RuntimeError('There is some problem. Can\'t take picture')

        return fullpath


    def upload_pic(self, fullpath):
        server_path = '/' + '/'.join(fullpath.split('/')[2:])

        result = self.__client.upload_from_path(fullpath, {'album': config['imgur']['album_deletehash']})
        payload = {'hits': 0, 'imgur_link': result['link'], 'real_path': server_path}
        self.__firebaseRef.put('/photos', result['id'], payload)

        return result['link']
