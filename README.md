# ДЗ 3: Docker

HTTP-счётчик с хранением данных в Redis. Исходники — в [app](../app),
сборка — [Dockerfile](Dockerfile), сервисы `hw_app` и `redis` —
в [docker-compose.yaml](docker-compose.yaml). Код приложения не изменён.

## Запуск

Нужны Docker с Compose и curl. Из корня репозитория:

```sh
cp .env.example .env
docker compose up --build --wait
curl http://localhost:8080/
curl -X POST http://localhost:8080/increment
docker compose logs hw_app
```

Настройки в `.env`:

| Переменная | По умолчанию | Назначение |
| --- | --- | --- |
| `GREETING` | `Hello, Docker!` | Приветствие в ответе |
| `APP_VERSION` | `latest` | Тег образа приложения |
| `HOST_PORT` | `8080` | Порт на компьютере |
| `PORT` | `8000` | Порт внутри контейнера; оставьте 8000 |

Если меняете `HOST_PORT`, замените порт и в командах curl.
Redis использует AOF и именованный volume `redis_data`.

```sh
docker compose down
docker compose up --wait
```

Счётчик сохраняется после этих команд. `docker compose down -v` удаляет данные.

## Автоматическая проверка

Для скрипта нужен Python 3.8+ без дополнительных пакетов:

```sh
python scripts/check.py
```

Если Python установлен как `python3`, используйте это имя команды.
Скрипт создаёт отдельный проект, проверяет счётчик 0 → 5, пересоздание приложения
и отключение/запуск Redis. После штатной остановки сервисов сохраняет весь каталог
Redis в `backups/<проект>.tar` и удаляет тестовый проект вместе с volumes.
Есть тайм-ауты, ненулевой код при ошибке и очистка через `finally` и обработчики сигналов.

## Короткий отчёт

- Один контейнер: запросы и увеличение счётчика отражены в [логах](reports/logs.txt).
- SQLite: счётчик вырос до 5 и сохранился после пересоздания — [вывод](reports/sqlite_working_report.md).
- Redis: после `down/up` сохранилось 23; при отключении ответы 200/503/503,
  после запуска следующий POST вернул 24 — [вывод](reports/redis_working_report.md).
- Автопроверка прошла два раза подряд с кодом 0 — [полный вывод](reports/check-report.md).

Для приложения настроены UID 1000, корневая файловая система только для чтения,
лимиты памяти 256 MiB и CPU 1 ядро. У обоих сервисов есть healthcheck.
