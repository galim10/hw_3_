import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import uuid

N = 5
os.chdir(Path(__file__).resolve().parents[1])
project = "hw3-check-" + uuid.uuid4().hex[:12]
env = {k: v for k, v in os.environ.items() if not k.startswith("COMPOSE_")}
env.update(APP_VERSION=project, PORT="8000", HOST_PORT="127.0.0.1:0", GREETING="Check")
compose = ["docker", "compose", "-p", project]
archive = Path("backups") / (project + ".tar")
partial = archive.with_suffix(".partial")


def run(command, timeout=120, output=None):
    with subprocess.Popen(command, env=env, stdout=output or subprocess.PIPE,
                          stderr=subprocess.PIPE, start_new_session=True) as process:
        try:
            out, err = process.communicate(timeout=timeout)
        except BaseException:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait(timeout=5)
            raise
        if process.returncode:
            raise RuntimeError(err.decode(errors="replace"))
        return out.decode().strip() if out else ""


def dc(*args, **kwargs):
    return run(compose + list(args), **kwargs)


def http(path="/", method="GET", status=200, count=None):
    response = run(["curl", "--max-time", "5", "-X", method,
                    "-w", "\n%{http_code}", url + path], timeout=7)
    body, actual = response.rsplit("\n", 1)
    if int(actual) != status:
        raise RuntimeError(f"{method} {path}: ожидался HTTP {status}, получен {actual}: {body}")
    if count is not None:
        data = json.loads(body)
        if data.get("count") != count or data.get("storage") != "redis":
            raise RuntimeError(f"Ожидался счётчик Redis {count}, получено: {body}")
    print(f"{method} {path} -> {actual} {body}")


def ready():
    global url
    url = "http://" + dc("port", "hw_app", "8000")
    http("/readyz")


def step(text):
    global stage
    stage = text
    print(f"\n{stage}")


def interrupted(signum, frame):
    raise KeyboardInterrupt(f"Сигнал {signum}")


signals = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)
for sig in signals:
    signal.signal(sig, interrupted)
code = 0
try:
    step(f"1. Новый проект {project}")
    dc("up", "--wait", "--wait-timeout", "90", timeout=600)
    ready()

    step(f"2. Счётчик 0 → {N}")
    http(count=0)
    for count in range(1, N + 1):
        http("/increment", "POST", count=count)
    http(count=N)

    step("3. Пересоздание только приложения")
    dc("up", "--no-deps", "--force-recreate", "--wait", "--wait-timeout", "90", "hw_app")
    ready()
    http(count=N)

    step("4. Отключение и повторный запуск Redis")
    dc("stop", "redis")
    http("/healthz")
    http("/readyz", status=503)
    http("/increment", "POST", status=503)
    dc("start", "--wait", "--wait-timeout", "90", "redis")
    ready()
    http(count=N)
    http("/increment", "POST", count=N + 1)

    step("5. Резервная копия")
    dc("kill", "--signal", "SIGINT", "hw_app")
    dc("stop", "hw_app", "redis")
    state = json.loads(run(["docker", "inspect", dc("ps", "-aq", "redis")]))[0]["State"]
    if state["Status"] != "exited" or state["ExitCode"] != 0:
        raise RuntimeError("Redis не завершился штатно; копия отменена")
    archive.parent.mkdir(exist_ok=True)
    with partial.open("xb") as output:
        dc("run", "--rm", "--no-deps", "-T", "--entrypoint", "tar",
           "redis", "-cf", "-", "-C", "/data", ".", output=output)
    partial.replace(archive)
    print(f"Архив: {archive}")
except (Exception, KeyboardInterrupt) as error:
    code = 1
    print(f"ОШИБКА, этап {stage}: {error}", file=sys.stderr)
finally:
    for sig in signals:
        signal.signal(sig, signal.SIG_IGN)
    step("6. Очистка: down -v")
    try:
        dc("down", "-v", "--remove-orphans")
        if run(["docker", "image", "ls", "-q", "app:" + project]):
            run(["docker", "image", "rm", "--no-prune", "app:" + project])
        partial.unlink(missing_ok=True)
    except Exception as error:
        code = 1
        print(f"ОШИБКА очистки: {error}", file=sys.stderr)
if code == 0:
    print("УСПЕХ: все 6 этапов пройдены.")
sys.exit(code)
