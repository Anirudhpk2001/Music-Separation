
import requests
import json
import time
import sys
import base64

def separateMP3(address, filename, debug=False):
    headers = {'content-type': 'application/json'}
    music = open('../data/' + filename, 'rb').read()
    encoded_music = base64.b64encode(music).decode()

    separate_url = address + '/separate/' + filename
    print(separate_url)
    response = requests.post(separate_url, json={'music_data': encoded_music}, headers=headers)
    if debug:
        print('Response is', response)
        print(json.loads(response.text))

def getQueue(address, debug=False):
    headers = {'content-type': 'application/json'}
    queue_url = address + '/queue'
    response = requests.get(queue_url, headers=headers)
    if debug:
        print('Response is', response)
        print(json.loads(response.text))

def getTrack(address, hash_val, track, debug=False):
    url = address + '/track/' + hash_val + '/' + track
    response = requests.get(url)
    if response.headers['Content-type'] == 'audio/mpeg':
        with open('./downloads/' + hash_val + '-' + track + '.mp3', 'wb') as binary_file:
            binary_file.write(response.content)
        print('Response is', response)
        print('Downloaded file')
    else:
        print('Response is', response)
        print(json.loads(response.text))

def removeTrack(address, hash_val, debug=False):
    url = address + '/delete/' + hash_val
    response = requests.delete(url)
    if debug:
        print('Response is', response)
        print(json.loads(response.text))

def healthCheck(address, debug=False):
    url = address
    response = requests.get(url)
    if debug:
        print('Response is', response)
        print(response.text)

host = sys.argv[1]
command = sys.argv[2]
address = 'http://{}:8080'.format(host)

if command == 'separate':
    filename = sys.argv[3]
    start = time.perf_counter()
    separateMP3(address, filename, True)
    delta = ((time.perf_counter() - start)) * 1000
    print('Took', delta, 'ms per operation')
elif command == 'queue':
    start = time.perf_counter()
    getQueue(address, True)
    delta = ((time.perf_counter() - start)) * 1000
    print('Took', delta, 'ms per operation')
elif command == 'track':
    hash_val = sys.argv[3]
    track = sys.argv[4]
    start = time.perf_counter()
    getTrack(address, hash_val, track, True)
    delta = ((time.perf_counter() - start)) * 1000
    print('Took', delta, 'ms per operation')
elif command == 'remove':
    hash_val = sys.argv[3]
    start = time.perf_counter()
    removeTrack(address, hash_val, True)
    delta = ((time.perf_counter() - start)) * 1000
    print('Took', delta, 'ms per operation')
elif command == 'healthcheck':
    healthCheck(address, True)
else:
    print('Unknown option', command)
