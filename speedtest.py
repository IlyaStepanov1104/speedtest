import sys
import time
import urllib.request

REQUESTS = 10
DEFAULT_URL = "https://upload.wikimedia.org/wikipedia/commons/3/3f/Fronalpstock_big.jpg"


def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": "speedtest/1.0"})
    start = time.perf_counter()
    size = 0
    with urllib.request.urlopen(req, timeout=60) as resp:
        expected = resp.headers.get("Content-Length")
        while True:
            chunk = resp.read(64 * 1024)
            if not chunk:
                break
            size += len(chunk)
    elapsed = time.perf_counter() - start

    # сервер иногда рвёт соединение посреди ответа, такой замер не считаем
    if expected and size != int(expected):
        raise IOError(f"получено {size} байт из {expected}")
    return size, elapsed


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    print(f"url: {url}")

    total_bytes = 0
    total_time = 0.0

    ok = 0

    for i in range(1, REQUESTS + 1):
        try:
            size, elapsed = download(url)
        except Exception as e:
            print(f"{i:2}) ошибка: {e}")
            continue
        ok += 1
        total_bytes += size
        total_time += elapsed
        print(f"{i:2}) {size / 1024 / 1024:.2f} МБ за {elapsed:.2f} с")

    if not ok:
        print("ни один запрос не прошёл")
        sys.exit(1)

    mb = total_bytes / 1024 / 1024
    print()
    if ok < REQUESTS:
        print(f"успешных запросов: {ok} из {REQUESTS}")
    print(f"среднее время запроса: {total_time / ok:.2f} с")
    print(f"скачано всего: {mb:.2f} МБ")
    print(f"скорость: {mb / total_time:.2f} МБ/с ({mb * 8 / total_time:.1f} Мбит/с)")


if __name__ == "__main__":
    main()
