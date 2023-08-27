from concurrent import futures
import logging
import os
import grpc
from protos import hello_pb2, hello_pb2_grpc


# Funkcja generująca ścieżkę do pliku na podstawie nazwy i rozszerzenia
def get_filepath(filename, extension):
    return f'{filename}{extension}'

# Klasa implementująca zdalny interfejs gRPC
class Greeter(hello_pb2_grpc.GreeterServicer):

    # Utworzenie funkcji zwracającej wiadomość
    def SayHello(self, request, context):
        return hello_pb2.StringResponse(message=f'Hello, Marcin! Your age is 22')

    # Utowrzenie funkcji wysyłającej plik
    def UploadFile(self, request_iterator, context):
        data = bytearray()
        filepath = 'dummy'

        # Iteracja po strumieniu danych przesyłanych przez klienta
        for request in request_iterator:
            if request.metadata.filename and request.metadata.extension:
                filepath = get_filepath(request.metadata.filename, request.metadata.extension)
                continue
            data.extend(request.chunk_data)

        # Zapis danych do pliku
        with open(filepath, 'wb') as f:
            f.write(data)
        return hello_pb2.StringResponse(message='Success!')

    # Utworzenie funkcji pobierającej plik
    def DownloadFile(self, request, context):
        chunk_size = 1024

        # Utworzenie pełnej ścieżki do pliku na podstawie żądania klienta
        filepath = f'{request.filename}{request.extension}'
        if os.path.exists(filepath):
            with open(filepath, mode="rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if chunk:

                        # Wysyłanie fragmentu pliku do klienta za pomocą strumienia
                        entry_response = hello_pb2.FileResponse(chunk_data=chunk)
                        yield entry_response
                    else:
                        # Pusty fragment oznacza koniec pliku
                        return

# Utowrzenie funkcji, która startuje serwer gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
