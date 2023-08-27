
import requests
 
url = 'http://192.168.43.103/upload_file'
files = {'file': open('plik.txt', 'rb')}
 
r = requests.post(url, files=files)
 
if r.status_code == 200:
    print('Plik został wysłany.')
