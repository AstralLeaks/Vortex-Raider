import requests



url = "https://api.hcoptcha.online/api/getUserData"


body = {
    "api_key": "" #Bro forgot his api key lmao, wont leak it tho :fire:
}


resp = requests.post(url, json=body)


print (resp.text)