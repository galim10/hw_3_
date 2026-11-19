# Проверка redis

## Запуск 1

```text
➜  hw3_idt git:(main) ✗ docker compose up -d
[+] up 3/3
 ✔ Network hw3_idt_default    Created                                                                                                                                        0.0s
 ✔ Container hw3_idt-redis-1  Started                                                                                                                                        0.1s
 ✔ Container hw3_idt-hw_app-1 Started                                                                                                                                        0.1s
➜  hw3_idt git:(main) ✗ curl -fsS -X POST http://127.0.0.1:8080/increment

{"greeting": "i love ami", "count": 20, "hostname": "89c0c2ff4cae", "storage": "redis"}%                                                                                         ➜  hw3_idt git:(main) ✗ curl -fsS -X POST http://127.0.0.1:8080/increment

{"greeting": "i love ami", "count": 21, "hostname": "89c0c2ff4cae", "storage": "redis"}%                                                                                         ➜  hw3_idt git:(main) ✗ curl -fsS -X POST http://127.0.0.1:8080/increment

{"greeting": "i love ami", "count": 22, "hostname": "89c0c2ff4cae", "storage": "redis"}%                                                                                         ➜  hw3_idt git:(main) ✗ curl -fsS -X POST http://127.0.0.1:8080/increment

{"greeting": "i love ami", "count": 23, "hostname": "89c0c2ff4cae", "storage": "redis"}%
➜  hw3_idt git:(main) ✗ docker compose down
[+] down 3/3
 ✔ Container hw3_idt-hw_app-1 Removed                                                                                                                                        3.1s
 ✔ Container hw3_idt-redis-1  Removed                                                                                                                                        0.1s
 ✔ Network hw3_idt_default    Removed                                                                                                                                        0.1s
➜  hw3_idt git:(main) ✗ docker compose up -d
[+] up 3/3
 ✔ Network hw3_idt_default    Created                                                                                                                                        0.0s
 ✔ Container hw3_idt-redis-1  Started                                                                                                                                        0.1s
 ✔ Container hw3_idt-hw_app-1 Started                                                                                                                                        0.1s
➜  hw3_idt git:(main) ✗ curl -fsS http://127.0.0.1:8080/

{"greeting": "i love ami", "count": 23, "hostname": "0d1103c7d265", "storage": "redis"}%                                                                                         ➜  hw3_idt git:(main) ✗ docker compose stop redis
[+] stop 1/1
 ✔ Container hw3_idt-redis-1 Stopped                                                                                                                                         0.1s
➜  hw3_idt git:(main) ✗ curl -fsS http://127.0.0.1:8080/healthz

{"status": "alive"}%
➜  hw3_idt git:(main) ✗ curl -fsS http://127.0.0.1:8080/readyz

curl: (22) The requested URL returned error: 503
➜  hw3_idt git:(main) ✗ curl -fsS -X POST http://127.0.0.1:8080/increment

curl: (22) The requested URL returned error: 503
➜  hw3_idt git:(main) ✗ docker compose start redis
[+] start 1/1
 ✔ Container hw3_idt-redis-1 Started                                                                                                                                         0.1s
➜  hw3_idt git:(main) ✗ curl -fsS http://127.0.0.1:8080/

{"greeting": "i love ami", "count": 23, "hostname": "0d1103c7d265", "storage": "redis"}%
➜  hw3_idt git:(main) ✗ curl -fsS -X POST http://127.0.0.1:8080/increment

{"greeting": "i love ami", "count": 24, "hostname": "0d1103c7d265", "storage": "redis"}%
```