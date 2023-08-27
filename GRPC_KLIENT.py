import logging
import os
import grpc
from protos import hello_pb2, hello_pb2_grpc


# Funkcja generująca ścieżkę do pliku na podstawie nazwy i rozszerzenia
def get_filepath(filename, extension):
    return f'{filename}{extension}'


# Funkcja generatora strumienia danych do przesłania na serwer
def read_iterfile(filepath, chunk_size=1024):
    split_data = os.path.splitext(filepath)
    filename = split_data[0]
    extension = split_data[1]

    # Tworzenie metadanych dla pierwszego żądania
    metadata = hello_pb2.MetaData(filename=filename, extension=extension)
    yield hello_pb2.UploadFileRequest(metadata=metadata)

    # Czytanie i przesyłanie danych pliku po fragmentach
    with open(filepath, mode="rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:

                # Wysyłanie fragmentu danych jako żądanie
                entry_request = hello_pb2.UploadFileRequest(chunk_data=chunk)
                yield entry_request
            else:
                # Pusty fragment oznacza koniec pliku
                return


# Funkcja wykonująca logikę klienta gRPC
def run():
    # Nawiązanie połączenia z serwerem
    with grpc.insecure_channel('192.168.43.103:50051') as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)

        # Wywołanie zdalnej funkcji SayHello
        response = stub.SayHello(hello_pb2.HelloRequest(name='Marcin', age=22))
        print("Greeter client received: " + response.message)

        # Wywołanie funkcji UploadFile i przesłanie pliku txt
        response = stub.UploadFile(read_iterfile('/home/kali/test.txt'))
        print("Greeter client received: " + response.message)

        # Pobieranie pliku od serwera po fragmentach i zapisywanie do pliku
        filename = 'test'
        extension = '.txt'
        filepath = get_filepath(filename, extension)
        for entry_response in stub.DownloadFile(hello_pb2.MetaData(filename=filename, extension=extension)):
            with open(filepath, mode="ab") as f:
                f.write(entry_response.chunk_data)


if __name__ == '__main__':
    logging.basicConfig()
    run()
