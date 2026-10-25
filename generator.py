import os
import requests

# Создаем папку overhub, если её нет
os.makedirs("overhub", exist_ok=True)

# Описываем группы, их raw-ссылки и целевые файлы
groups = {
    "overhub/white.txt": [
        "https://hub.mos.ru/akelladejavu/bunker/-/raw/main/WHITE_LIST.txt",
        "https://gitverse.ru/api/repos/Pizduk/PizdukVPN/raw/branch/master/WlSubPiz.txt",
        "https://github.com/vessel-web/CoolSubs/raw/refs/heads/main/Cool-White.txt",
        "https://hub.mos.ru/akelladejavu/bunker/-/raw/main/WHITE_LIST.txt",
        # Сюда можешь дописать сколько угодно сыллок для группы white
    ],
    "overhub/servers.txt": [
        "https://hub.mos.ru/akelladejavu/bunker/-/raw/main/BLACK_LIST.txt",
        "https://gitverse.ru/api/repos/Pizduk/PizdukVPN/raw/branch/master/sub.txt",
        "https://raw.githubusercontent.com/MrMisha4048/pizdukspecial/refs/heads/main/vpn.txt",
        "https://raw.githubusercontent.com/vessel-web/CoolSubs/refs/heads/main/Cool-Black.txt",
        # Сюда сыллки для группы servers
    ]
}

# Префиксы валидных конфигов, которые нужно собирать
valid_prefixes = ("vless://", "vmess://", "trojan://", "ss://", "ssr://", "tuic://", "hysteria://", "hy2://")

for output_file, urls in groups.items():
    all_configs = []
    
    for url in urls:
        try:
            print(Cat_msg := f"Скачиваем из: {url}")
            response = requests.get(url, timeout=20)
            
            if response.status_code == 200:
                for line in response.text.splitlines():
                    clean_line = line.strip()
                    # Проверяем, что строка начинается с одного из нужных протоколов
                    if clean_line.startswith(valid_prefixes):
                        all_configs.append(clean_line)
            else:
                print(f"Ошибка {response.status_code} при скачивании {url}")
        except Exception as e:
            print(f"Не удалось получить данные с {url}: {e}")
            
    # Убираем дубликаты, сохраняя порядок
    unique_configs = list(dict.fromkeys(all_configs))
    
    # Сохраняем в целевой файл
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(unique_configs) + "\n")
        
    print(f"Готово! Записано {len(unique_configs)} конфигов в {output_file}\n")
