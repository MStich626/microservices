import requests

# Adres URL endpointu na serwerze, do którego wysyłamy plik
url = 'http://192.168.43.103/upload_file'

# Definicja pliku do wysłania
files = {'file': open('plik.txt', 'rb')}

# Wysłanie żądania POST z załączonym plikiem
r = requests.post(url, files=files)

# Sprawdzenie kodu statusu odpowiedzi
if r.status_code == 200:
    print('Plik został wysłany.')
