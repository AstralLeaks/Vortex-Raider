import requests

proxies = [
    {
        'http': 'http://itayhvsx-rotate:dems862q400p@p.webshare.io:80',
        'https': 'http://itayhvsx-rotate:dems862q400p@p.webshare.io:80'
    },
    {
        'http': 'http://ahoffbbu-rotate:ub9fv9ntqa7i@p.webshare.io:80',
        'https': 'http://ahoffbbu-rotate:ub9fv9ntqa7i@p.webshare.io:80'
    },
    {
        'http': 'http://klnvdhaj-rotate:nu8oirwshcwl@p.webshare.io:80',
        'https': 'http://klnvdhaj-rotate:nu8oirwshcwl@p.webshare.io:80'
    }
]

for proxy in proxies:
    try:
        response = requests.get('https://www.google.com', proxies=proxy)
        if response.status_code == 200:
            print("Proxy is valid.")
        else:
            print("Proxy is invalid.")
    except requests.exceptions.RequestException as e:
        print("Error occurred while checking the proxy:", str(e))