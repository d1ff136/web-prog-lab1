import http from 'node:http';
import { readFileSync } from 'node:fs';

const PORT = 3001;

// Явна таблиця відповідності "шлях -> файл", без довільного доступу до файлової системи
const routes = {
  '/': 'index.html',
  '/about': 'about.html',
  '/styles.css': 'styles.css',
};

// Content-Type за розширенням файлу
const contentTypes = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
};

function getContentType(fileName) {
  const ext = fileName.slice(fileName.lastIndexOf('.'));
  return contentTypes[ext] ?? 'application/octet-stream';
}

function readPublicFile(fileName) {
  const fileUrl = new URL(`./public/${fileName}`, import.meta.url);
  return readFileSync(fileUrl, 'utf-8');
}

// Файл сторінки 404 читаємо одразу, бо він потрібен для будь-якого невідомого шляху
const notFoundBody = readPublicFile('404.html');

const server = http.createServer((req, res) => {
  // Відкидаємо query string: '/about?source=test' -> '/about'
  const path = new URL(req.url, `http://${req.headers.host}`).pathname;

  const fileName = routes[path];

  if (fileName) {
    const body = readPublicFile(fileName);
    res.writeHead(200, { 'Content-Type': getContentType(fileName) });
    res.end(body);
    return;
  }

  // Невідомий шлях: повертаємо сторінку помилки зі статусом 404,
  // без Location-заголовка та без зміни адреси в браузері
  res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(notFoundBody);
});

server.listen(PORT, () => {
  console.log(`Node.js server running at http://localhost:${PORT}`);
});
