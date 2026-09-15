from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlsplit

PORT = 3002
SERVER_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = SERVER_DIR / 'public'

#явна таблиця відповідності "шлях на файл", без довільного доступу до файлової системи
ROUTES = {
    '/': 'index.html',
    '/about': 'about.html',
    '/styles.css': 'styles.css',
}

CONTENT_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
}


def content_type_for(file_name: str) -> str:
    ext = Path(file_name).suffix
    return CONTENT_TYPES.get(ext, 'application/octet-stream')


def read_public_file(file_name: str) -> str:
    return (PUBLIC_DIR / file_name).read_text(encoding='utf-8')


#файл сторінки 404 читаємо одразу, бо він потрібен для будь-якого невідомого шляху
NOT_FOUND_BODY = read_public_file('404.html')


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        #відкидаємо query string: '/about?source=test' -> '/about'
        path = urlsplit(self.path).path

        file_name = ROUTES.get(path)

        if file_name:
            body = read_public_file(file_name)
            self.send(200, content_type_for(file_name), body)
            return

        #невідомий шлях: повертаємо сторінку помилки зі статусом 404,без Location-заголовка та без зміни адреси в браузері
        self.send(404, 'text/html; charset=utf-8', NOT_FOUND_BODY)

    def send(self, status: int, content_type: str, body: str):
        encoded = body.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format, *args):
        print(f'{self.client_address[0]} - {format % args}')

if __name__ == '__main__':
    server = HTTPServer(('localhost', PORT), Handler)
    print(f'Python server running at http://localhost:{PORT}')
    server.serve_forever()
