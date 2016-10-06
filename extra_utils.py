import os
import json



def get_secrets(loc = 'secrets.json'):
    f = open('secrets.json', 'r')
    j = json.loads(f.read())
    f.close()
    return j


def send_mail(message,  target_mail, subject = 'RBPI message',):
    os.system('echo "{}" | mail -s "{}" {}'.format(message,subject,target_mail))

def folder_size(folder = '/data/numpy_arrays'):
    folder_size = 0
    for (path, dirs, files) in os.walk(folder):
        for file in files:
            filename = os.path.join(path, file)
            folder_size += os.path.getsize(filename)
    return folder_size/(1024*1024.0)


if __name__ == '__main__':
    print(EMAIL)
