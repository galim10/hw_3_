# Проверка scripts/check.py

## Запуск 1

```text
$ python3 scripts/check.py

1. Новый проект hw3-check-4f2dd67d7844
GET /readyz -> 200 {"status": "ready", "storage": "redis"}

2. Счётчик 0 → 5
GET / -> 200 {"greeting": "Check", "count": 0, "hostname": "95cb4d7ffdd0", "storage": "redis"}
POST /increment -> 200 {"greeting": "Check", "count": 1, "hostname": "95cb4d7ffdd0", "storage": "redis"}
POST /increment -> 200 {"greeting": "Check", "count": 2, "hostname": "95cb4d7ffdd0", "storage": "redis"}
POST /increment -> 200 {"greeting": "Check", "count": 3, "hostname": "95cb4d7ffdd0", "storage": "redis"}
POST /increment -> 200 {"greeting": "Check", "count": 4, "hostname": "95cb4d7ffdd0", "storage": "redis"}
POST /increment -> 200 {"greeting": "Check", "count": 5, "hostname": "95cb4d7ffdd0", "storage": "redis"}
GET / -> 200 {"greeting": "Check", "count": 5, "hostname": "95cb4d7ffdd0", "storage": "redis"}

3. Пересоздание только приложения
GET /readyz -> 200 {"status": "ready", "storage": "redis"}
GET / -> 200 {"greeting": "Check", "count": 5, "hostname": "99d95cfaf1f5", "storage": "redis"}

4. Отключение и повторный запуск Redis
GET /healthz -> 200 {"status": "alive"}
GET /readyz -> 503 {"error": "storage_unavailable"}
POST /increment -> 503 {"error": "storage_unavailable"}
GET /readyz -> 200 {"status": "ready", "storage": "redis"}
GET / -> 200 {"greeting": "Check", "count": 5, "hostname": "99d95cfaf1f5", "storage": "redis"}
POST /increment -> 200 {"greeting": "Check", "count": 6, "hostname": "99d95cfaf1f5", "storage": "redis"}

5. Резервная копия
Архив: backups/hw3-check-4f2dd67d7844.tar

6. Очистка: down -v
УСПЕХ: все 6 этапов пройдены.
Код завершения: 0
```

## Запуск 2

```text
$ python3 scripts/check.py

1. Новый проект hw3-check-ceacf84b4a02
GET /readyz -> 200 {"status": "ready", "storage": "redis"}

2. Счётчик 0 → 5
GET / -> 200 {"greeting": "Check", "count": 0, "hostname": "6bbe7271f284", "storage": "redis"}
POST /increment -> 200 {"greeting": "Check", "count": 1, "hostname": "6bbe7271f284", "storage": "redis"}
POST /increment -> 200 {"greeting": "Check", "count": 2, "hostname": "6bbe7271f284", "storage": "redis"}
POST /increment -> 200 {"greeting": "Check", "count": 3, "hostname": "6bbe7271f284", "storage": "redis"}
POST /increment -> 200 {"greeting": "Check", "count": 4, "hostname": "6bbe7271f284", "storage": "redis"}
POST /increment -> 200 {"greeting": "Check", "count": 5, "hostname": "6bbe7271f284", "storage": "redis"}
GET / -> 200 {"greeting": "Check", "count": 5, "hostname": "6bbe7271f284", "storage": "redis"}

3. Пересоздание только приложения
GET /readyz -> 200 {"status": "ready", "storage": "redis"}
GET / -> 200 {"greeting": "Check", "count": 5, "hostname": "a2ba6bbdfce9", "storage": "redis"}

4. Отключение и повторный запуск Redis
GET /healthz -> 200 {"status": "alive"}
GET /readyz -> 503 {"error": "storage_unavailable"}
POST /increment -> 503 {"error": "storage_unavailable"}
GET /readyz -> 200 {"status": "ready", "storage": "redis"}
GET / -> 200 {"greeting": "Check", "count": 5, "hostname": "a2ba6bbdfce9", "storage": "redis"}
POST /increment -> 200 {"greeting": "Check", "count": 6, "hostname": "a2ba6bbdfce9", "storage": "redis"}

5. Резервная копия
Архив: backups/hw3-check-ceacf84b4a02.tar

6. Очистка: down -v
УСПЕХ: все 6 этапов пройдены.
Код завершения: 0
```
