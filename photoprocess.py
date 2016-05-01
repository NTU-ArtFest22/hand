from imgurpython import ImgurClient
from firebase import firebase
from wand.image import Image
from wand.drawing import Drawing
from wand.display import display
import subprocess as sp
import os.path as path
import requests
import yaml

COMPOSE_IMAGE_GAP = 20

with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

class PhotoProcess:

    def __init__(self):
        auth = firebase.FirebaseAuthentication(config['firebase']['secret'], None, admin=True)

        self.__client = ImgurClient(config['imgur']['client_id'], config['imgur']['secret'])
        self.__firebaseRef = firebase.FirebaseApplication(config['firebase']['url'], authentication=auth)

    # gphoto2 output:
    # if success it'll have 3 lines of message
    # 1st: New file is in location ... on the camera
    # 2nd: Saving file as ...
    # 3rd: Deleting file ...
    # 4th: \n
    def take_pic(self):
        out, err = sp.Popen(['gphoto2', '--capture-image-and-download', '--no-keep', \
            '--filename', './public/images/photos/photo-%Y%m%d-%H%M%S.JPG'], \
            stdout=sp.PIPE, stderr=sp.PIPE).communicate()

        if out:
            print out
            fullpath = out.split('\n')[1].split()[-1]
        else:
            print err
            raise RuntimeError('There is some problem. Can\'t take picture')

        return fullpath

    def pic_compose_logo(self, fullpath):
        name_detail = path.splitext(path.basename(fullpath))
        dirname = path.dirname(fullpath)

        new_name = name_detail[0] + '-result' + name_detail[1]
        result_path = dirname + '/' + new_name

        bg = Image(filename=fullpath)
        bg.transform(resize='1600x>')
        logo = Image(filename='./logo.png')
        logo.transform(resize='200x')

        with Drawing() as draw:
        	draw.composite(operator='atop',
                           left=bg.width-logo.width-COMPOSE_IMAGE_GAP,
                           top=COMPOSE_IMAGE_GAP,
                           width=logo.width,
                           height=logo.height,
                           image=logo)
        	draw(bg)
        	bg.save(filename=result_path)

        return result_path

    def upload_pic(self, fullpath):
        server_path = '/' + '/'.join(fullpath.split('/')[2:])

        result = self.__client.upload_from_path(fullpath, {'album': config['imgur']['album_deletehash']})
        payload = {'hits': 0, 'imgur_link': result['link'], 'real_path': server_path}
        self.__firebaseRef.put('/photos', result['id'], payload)

        return result['link']
