import datetime
from colorama import Fore
import time
import requests
import urllib.parse
from requests.exceptions import JSONDecodeError
import json

W = Fore.RESET
C = "\033[38;2;75;0;130m"
L = Fore.LIGHTYELLOW_EX
V = Fore.GREEN
B = Fore.LIGHTBLACK_EX
I = Fore.LIGHTRED_EX

def headers(token):
    return {
        'Accept': '*/*',
        'Accept-Language': 'en-EN,cs;q=0.9,en;q=0.8',
        'Authorization': token,
        'Cookie': '__dcfduid=bcdcc21048ec11eeb28aadb2936bc589; __sdcfduid=bcdcc21148ec11eeb28aadb2936bc58939681dcd50112431f1dc800e50f374628b27f03a40107a46ebf3a05065becb2c; _ga_Q149DFWHT7=GS1.1.1693589213.1.0.1693589414.0.0.0; __stripe_mid=a614d196-bfdf-4093-be94-44b2567c7c312dff1a; _ga_XXP2R74F46=GS1.2.1702481998.1.0.1702481998.0.0.0; _gid=GA1.2.1957939489.1702654470; _ga_YL03HBJY7E=GS1.1.1702654469.11.0.1702654469.0.0.0; _ga=GA1.1.1994256083.1693589213; OptanonConsent=isIABGlobal=false&datestamp=Fri+Dec+15+2023+16%3A34%3A29+GMT%2B0100+(czas+%C5%9Brodkowoeuropejski+standardowy)&version=6.33.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0&AwaitingReconsent=false; __cfruid=7c526e008192466f8ca27de600811cb9f9a9b039-1702664289; _cfuvid=ut98lvE6CAZQkcpuAaMXk7oTUSVGktwTdF16TRtT.EQ-1702664289884-0-604800000; cf_clearance=G65_tgviKwqVw0qNdhw0byG9ATZLTfAEAszCfqd.CMk-1702664599-0-1-3b6189e5.cb55b875.78db4fb0-0.2.1702664599; locale=en',
        'Referer': 'https://discord.com/channels/@me',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Safari/537.36',
        'X-Debug-Options': 'bugReporterEnabled',
        'X-Discord-Locale': 'en',
        'X-Discord-Timezone': 'Europe/London',
        'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InBsLVBMIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExOS4wLjYwNDUuMTk5IFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIxMTkuMC42MDQ1LjE5OSIsIm9zX3ZlcnNpb24iOiIxMCIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNTQ4ODgsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9'
}

def solve_hcaptcha(captcha_sitekey, hCaptcha_api_key):
    task_data = {
        "task_type": "hcaptchaEnterprise",
        "api_key": hCaptcha_api_key,
        "data": {
            "sitekey": captcha_sitekey,
            "url": "https://discord.com/channels/@me",
            "proxy": "p.webshare.io:80:iiggasvm-rotate:71iv92jt6dyn"
        }
    }

    task_response = requests.post("https://api.hcoptcha.online/api/createTask", json=task_data)
    print (task_response.json())    
    if not task_response.json().get("error"):
        task_id = task_response.json().get("task_id")
        time.sleep(5)
        result_data = {
            "api_key": hCaptcha_api_key,
            "task_id": task_id
        }
        result_response = requests.post("https://api.hcoptcha.online/api/getTaskData", json=result_data)
        print (result_response.json())
        if not task_response.json().get("error"):
            captcha_key = result_response.json().get("task", {}).get("captcha_key")
            return captcha_key

    return None

def join_guild_with_captcha(token, invite, hCaptcha_api_key):
    invite = invite.split("/")[-1]
    invite_url = f"https://discord.com/api/v9/invites/{invite}"
    proxies = {
    "http": "http://rjnjisng-rotate:p2uszd9sfh88@p.webshare.io:80",
    "https": "http://rjnjisng-rotate:p2uszd9sfh88@p.webshare.io:80"
}
    
    response = requests.post(invite_url, headers=headers(token), proxies=proxies)
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    if response.content:
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            print(response.text)
            print(f"{W}{current_time}{C}||{I}Cloudflare blocked you ggs.")
            return

        if "captcha_key" in response_json or "captcha needed" in response.text.lower():
            print(f"{W}{current_time}{C}||{I}CAPTCHA challenge detected. Solving...")
            captcha_sitekey = response.json().get('captcha_sitekey', 'default_sitekey')
            print(captcha_sitekey)
            solved_captcha_key = solve_hcaptcha(captcha_sitekey, hCaptcha_api_key)
            print(f"{solved_captcha_key}")
            if solved_captcha_key:
                response = requests.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers(token), data={'h-captcha-response': solved_captcha_key}, proxies=proxies)
                if response.status_code == 200:
                    print(f"{W}{current_time}{C}||{V}Successfully joined the server after solving CAPTCHA! {response.status_code}")
                else:
                    print(f"{W}{current_time}{C}||{I}Failed to join the server after solving CAPTCHA: {response.status_code}")
            else:
                print(f"{W}{current_time}{C}||{I}Failed to retrieve CAPTCHA key.")
        else:
            print(f"{W}{current_time}{C}||{I}Error in creating task: {response.text}")
    elif response.status_code == 200:
        print(f"{W}{current_time}{C}||{V}Successfully joined the server! {response.status_code}")
    elif response.status_code == 403:
        print(f"{W}{current_time}{C}||{I}Failed, blocked by Discord: {response.status_code}")
    elif response.status_code == 401:
        print(f"{W}{current_time}{C}||{I}Failed, dead token: {response.status_code}")
    else:
        print(f"{W}{current_time}{C}||{I}Failed, unknown error: {response.status_code}")

# Example usage of the function
join_guild_with_captcha("ODc1MzMxNDQzNjUwMzYzNDAy.G6q_CJ.YET0GL4OMBcAgg7Av9H94QjbgGhbZeP2elC28w", "https://discord.gg/MRTgawsG", "343a9a87-f0ff-46ee-af64-01671acf21a8")