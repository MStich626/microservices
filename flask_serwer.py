from flask import Flask, request
app = Flask(__name__)

# Definicja endpointu /upload_file, obsługującego żądania typu POST
@app.route('/upload_file', methods=['POST'])
def upload_file():
    # Otrzymanie pliku z żądania POST
    file = request.files['file']

    # Zapis pliku na serwerze w określonym miejscu
    file.save('/home/kali/uploaded_files/plik.txt')

    # Zwrócenie odpowiedzi potwierdzającej przesłanie pliku
    return 'Plik został wysłany.'

# Uruchomienie aplikacji Flask na porcie 80, dostępnym dla wszystkich interfejsów sieciowych
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
