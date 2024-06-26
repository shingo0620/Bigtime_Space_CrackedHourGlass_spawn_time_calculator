from curl_cffi import requests
from datetime import datetime, timedelta
import traceback
from rich.console import Console
from rich.theme import Theme
import os, sys, time
from dotenv import load_dotenv
from prettytable import PrettyTable

custom_theme = Theme({"info": "dim cyan", "warning": "magenta", "danger": "bold red"})
console = Console(theme=custom_theme)
GREEN = "\033[92m"
RED = "\033[91m"
ENDC = "\033[0m"

load_dotenv()

headers = {
    "authority": "api.openloot.com",
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/json",
    "cookie": os.getenv("COOKIE"),
    "origin": "https://openloot.com",
    "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "X-Client-Id:": "marketplace",
    "X-Device-Id": os.getenv("X-DEVICE-ID"),
    "X-Is-Mobile": "false",
    "X-Session-Id": os.getenv("X-SESSION-ID"),
    "X-User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
}

spawn_times = {
    ("rare", "small"): 72,
    ("rare", "medium"): 66,
    ("epic", "small"): 66,
    ("rare", "large"): 60,
    ("epic", "medium"): 60,
    ("legendary", "small"): 60,
    ("epic", "large"): 54,
    ("legendary", "medium"): 54,
    ("mythic", "small"): 54,
    ("legendary", "large"): 48,
    ("mythic", "medium"): 48,
    ("exalted", "small"): 48,
    ("mythic", "large"): 42,
    ("exalted", "medium"): 42,
    ("exalted", "large"): 36,
}


def calculate_time_difference(timestamp_str, spawn_time, timezone=8):
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    timestamp = timestamp + timedelta(hours=timezone)
    current_time = datetime.now()
    time_difference = current_time - timestamp
    remaining_time = timedelta(hours=spawn_time) - time_difference

    return remaining_time if remaining_time > timedelta(0) else timedelta(0)

def get_openloot_in_game_items(page=1, proxy=None, timeout=3):
    proxies = proxy if proxy else None
    url = f"https://api.openloot.com/v2/market/items/in-game?page={page}&pageSize=1000&sort=name%3Aasc&gameId=56a149cf-f146-487a-8a1c-58dc9ff3a15c&nftTags=NFT.SPACE"
    r = requests.get(
        url,
        proxies=proxies,
        headers=headers,
        impersonate="chrome120",
        timeout=timeout,
    )
    return r.json()

def gen_google_calendar_url(delta):
    current_time = datetime.now()
    new_time = current_time + delta
    formatted_time = new_time.strftime('%Y%m%dT%H%M%S')
    formatted_url = f"https://www.google.com/calendar/event?action=TEMPLATE&dates={formatted_time}%2F{formatted_time}&text=Bigtime Space Drop"
    return formatted_url

def main():
    os.system("cls")
    page = 1
    true_count = 0
    false_count = 0
    result = []

    while True:
        try:
            data = get_openloot_in_game_items(page)
            if "error" in data:
                print("错误: " + data["error"])
                print("按回车键退出")
                input()
                sys.exit()
            items = data["items"]
            for item in items:
                key = item["issuedId"]
                if item["extra"] == None or "attributes" not in item["extra"]:
                    continue
                for att in item["extra"]["attributes"]:
                    if att["name"] == "LastCrackedHourGlassDropTime":
                        timestamp = att["value"]
                        spawn_time = 72
                        item_tags = set(item["metadata"]["tags"])
                        for tags, times in spawn_times.items():
                            if set(tags).issubset(item_tags):
                                spawn_time = times
                                break
                        time_diff = calculate_time_difference(timestamp, spawn_time)
                        item["hourglass_remaining_time"] = time_diff
                    # elif att["name"] == "LastEpochDropTime":
                    #     timestamp = att["value"]
                    #     spawn_time = 48 # 尚不清楚具体掉落时间
                    #     time_diff = calculate_time_difference(timestamp, spawn_time)
                    #     item["epoch_remaining_time"] = time_diff
                
                # item["next_drop_remaining_time"] = min(item["hourglass_remaining_time"], item["epoch_remaining_time"])
                item["next_drop_remaining_time"] = item["hourglass_remaining_time"]
                item["next_drop_remaining_time"] -= timedelta(microseconds=item["next_drop_remaining_time"].microseconds)
                result.append(item)

        except Exception as e:
            console.log(f"处理页面 {page} 时出现错误: {traceback.format_exc()}")
            continue
        page += 1
        if page > data["totalPages"]:
            break
    
    result.sort(key=lambda x: x["next_drop_remaining_time"], reverse=True)
    # table = PrettyTable(field_names=["编号", "名称", "倒计时", "破碎沙漏", "纪元宝箱"])
    table = PrettyTable(field_names=["编号", "名称", "倒计时", "破碎沙漏"])
    table.align = "r"
    table.padding_width = 1 

    loop_count = 0
    for item in result:
        loop_count +=1
        hourglass_time_diff = item["hourglass_remaining_time"]
        # epoch_time_diff = item["epoch_remaining_time"]
        # next_time_diff =  min(hourglass_time_diff, epoch_time_diff) 
        next_time_diff = hourglass_time_diff
        next_time_diff -= timedelta(microseconds=next_time_diff.microseconds)
        # hourglass_time_diff if hourglass_time_diff < epoch_time_diff else epoch_time_diff
        hourglass_time_diff = hourglass_time_diff
        id = item["issuedId"]
        name = item["metadata"]["name"]
        rich_id = f"{GREEN}{id}{ENDC}" if next_time_diff <= timedelta(0) else f"{RED}{id}{ENDC}"
        table.add_row([
            rich_id,
            name,
            "" if next_time_diff <= timedelta(0) else next_time_diff,
            "" if hourglass_time_diff <= timedelta(0) else (datetime.now() + hourglass_time_diff).strftime("%m-%d %H:%M:%S"),
            # "" if epoch_time_diff <= timedelta(0) else (datetime.now() + epoch_time_diff).strftime("%m-%d %H:%M:%S"),
            ])
        if next_time_diff <= timedelta(0):
            true_count+=1 
        else:
            false_count+=1
        # prettytable在数量过多的时候会显示不全 每50条数据拆成一个表
        if (loop_count >= 50):
            print(table)
            table.clear_rows()
            loop_count = 0
    
    if (loop_count != 0):
        print(table)
    
    print(f"{GREEN}■ {true_count}{ENDC} {RED}■ {false_count}{ENDC}")
    if result[-1]['next_drop_remaining_time'] > timedelta(0):
        print(f"最小刷新时间: {result[-1]['next_drop_remaining_time']}")
        # print("添加到谷歌日历: " + gen_google_calendar_url(result[-1]['next_drop_remaining_time']))
    
    print("按回车键退出")
    input()


if __name__ == "__main__":
    main()