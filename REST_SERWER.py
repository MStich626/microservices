from flask import Flask, request
 
app = Flask(__name__)
 
@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save('/home/kali/uploaded_files/plik.txt')
    return 'Plik został wysłany.'
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
