import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init

init(autoreset=True)

def scrape_proxies_from_sslproxies():
    url = "https://www.sslproxies.org/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    proxies = []
    for row in soup.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) >= 2:  
            ip = cols[0].text.strip()
            port = cols[1].text.strip()
            proxies.append(f"{ip}:{port}")

    return proxies

def scrape_proxies_from_freeproxylists():
    url = "https://www.freeproxylists.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    proxies = []
    for row in soup.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) >= 2:
            ip = cols[0].text.strip()
            port = cols[1].text.strip()
            proxies.append(f"{ip}:{port}")

    return proxies

def scrape_proxies_from_usproxy():
    url = "https://www.us-proxy.org/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    proxies = []
    for row in soup.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) >= 2:  
            ip = cols[0].text.strip()
            port = cols[1].text.strip()
            proxies.append(f"{ip}:{port}")

    return proxies

def scrape_proxies_from_proxyscrape():
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=1000&country=all&ssl=all&anonymity=all"
    response = requests.get(url)
    
    proxies = response.text.splitlines()

    return proxies

def check_proxy(proxy):
    try:
        response = requests.get('http://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=10)
        if response.status_code == 200:
            return proxy
    except requests.RequestException:
        return None

def save_working_proxies(proxies, filename):
    with open(filename, 'a') as file:  
        for proxy in proxies:
            file.write(f"{proxy}\n")

def main():
    print(Fore.CYAN + Style.BRIGHT + "Starting Proxy Scraper...\n")
    
    proxies = (
        scrape_proxies_from_sslproxies()
        + scrape_proxies_from_freeproxylists()
        + scrape_proxies_from_usproxy()
        + scrape_proxies_from_proxyscrape()  
    )

    working_proxies = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}
        for future in as_completed(futures):
            result = future.result()
            proxy = futures[future]
            if result:
                working_proxies.append(result)
                print(Fore.GREEN + f"Working Proxy: {result}")
            else:
                print(Fore.RED + f"Failed Proxy: {proxy}")

    save_working_proxies(working_proxies, 'working_proxies.txt')
    print(Fore.YELLOW + f"Saved {len(working_proxies)} working proxies to 'working_proxies.txt'.")

    with open('working_proxies.txt', 'r') as file:
        print(Fore.MAGENTA + "\nList of Working Proxies:\n" + file.read())

if __name__ == "__main__":
    main()
