# Проверка sqlite с docker compose

```text
➜  hw3_idt git:(main) ✗ docker compose up -d
[+] up 3/3
 ✔ Volume hw3_idt_counter_data Created                                                                                                                                       0.0s
 ✔ Network hw3_idt_default     Created                                                                                                                                       0.0s
 ✔ Container hw3_idt-hw_app-1  Started                                                                                                                                       0.1s
➜  hw3_idt git:(main) ✗ curl -fsS http://127.0.0.1:8080/

{"greeting": "i love ami", "count": 0, "hostname": "07466d421690", "storage": "sqlite"}%
➜  hw3_idt git:(main) ✗ curl -fsS POST http://127.0.0.1:8080/increment
curl: (6) Could not resolve host: POST
curl: (22) The requested URL returned error: 404
➜  hw3_idt git:(main) ✗ curl -fsS -X POST http://127.0.0.1:8080/increment

{"greeting": "i love ami", "count": 1, "hostname": "07466d421690", "storage": "sqlite"}%                                                                                         ➜  hw3_idt git:(main) ✗ curl -fsS -X POST http://127.0.0.1:8080/increment

{"greeting": "i love ami", "count": 2, "hostname": "07466d421690", "storage": "sqlite"}%                                                                                         ➜  hw3_idt git:(main) ✗ curl -fsS -X POST http://127.0.0.1:8080/increment

{"greeting": "i love ami", "count": 3, "hostname": "07466d421690", "storage": "sqlite"}%                                                                                         ➜  hw3_idt git:(main) ✗ curl -fsS -X POST http://127.0.0.1:8080/increment

{"greeting": "i love ami", "count": 4, "hostname": "07466d421690", "storage": "sqlite"}%                                                                                         ➜  hw3_idt git:(main) ✗ curl -fsS -X POST http://127.0.0.1:8080/increment

{"greeting": "i love ami", "count": 5, "hostname": "07466d421690", "storage": "sqlite"}%
➜  hw3_idt git:(main) ✗ docker compose down
[+] down 2/2
 ✔ Container hw3_idt-hw_app-1 Removed                                                                                                                                        3.1s
 ✔ Network hw3_idt_default    Removed                                                                                                                                        0.1s
➜  hw3_idt git:(main) ✗ docker compose up -d
[+] up 2/2
 ✔ Network hw3_idt_default    Created                                                                                                                                        0.0s
 ✔ Container hw3_idt-hw_app-1 Started                                                                                                                                        0.1s
➜  hw3_idt git:(main) ✗ curl -fsS http://127.0.0.1:8080/

{"greeting": "i love ami", "count": 5, "hostname": "522a839fe288", "storage": "sqlite"}%
```
