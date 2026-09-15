# Лабораторна робота 1. Реалізація простого вебзастосунку

Виконав: Могилін Владислав Олександрович, група 6.1224

## Стеки та версії

- **Node.js** - v24.20.0
- **Python** - Python 3.12.11

## Структура каталогів

```
lab1/
  README.md
  node/
    server.mjs
    public/
      index.html
      about.html
      404.html
      styles.css
  python/
    server.py
    public/
      index.html
      about.html
      404.html
      styles.css
```

## Команди запуску

### Node.js (порт 3001)

```
cd node
node server.mjs
```
Відкрити: http://localhost:3001

### Python (порт 3002)

```
cd python
python3 server.py
```
Відкрити: http://localhost:3002

## Використані приклади лекції

Серверний код обох реалізацій адаптовано з прикладів `02-catalog` першої лекції:
отримання шляху запиту з відкиданням query string, явне зіставлення шляху з файлом
через таблицю маршрутів, читання HTML/CSS-файлів із диска (`readFileSync` для
Node.js, `Path.read_text` для Python) та явне задання статусу і заголовка
`Content-Type` у відповіді.

## Контракт маршрутів

| Шлях | Файл | Статус |
|---|---|---|
| `/` | `index.html` | 200 |
| `/about` | `about.html` | 200 |
| `/styles.css` | `styles.css` | 200 |
| будь-який інший | `404.html` | 404 |

Невідомий шлях повертає сторінку `404.html` за тим самим URL без перенаправлення
(заголовок `Location` відсутній).
