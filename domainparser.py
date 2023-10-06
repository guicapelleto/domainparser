import sys
import urllib3
import socket
import colorama
import base64
import os
from colorama import Fore,Back,Style
from grep import grep
colorama.init()

my_header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47"}


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def decode_b64(code):
    enc_msg = base64.b64decode(code)
    msg = enc_msg.decode('ascii')
    return msg


def print_banner():
    banner = b'X19fICBfX19fIF8gIF8gX19fXyBfIF8gIF8gICAgX19fICBfX19fIF9fX18gX19fXyBfX19fIF9fX18gCnwgIFwgfCAgfCB8XC98IHxfX3wgfCB8XCB8ICAgIHxfX10gfF9ffCB8X18vIFtfXyAgfF9fXyB8X18vIAp8X18vIHxfX3wgfCAgfCB8ICB8IHwgfCBcfCAgICB8ICAgIHwgIHwgfCAgXCBfX19dIHxfX18gfCAgXCAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg'
    print ('\n', Fore.LIGHTBLUE_EX + decode_b64(banner) + Style.RESET_ALL , '\nby: guicapelleto','\n\n')


def get_domain():
    usage = 'Usage: python domainparser.py your_domain.com\n\n'
    error = 'Could not access the domain:'
    try:
        domain = sys.argv[1]
    except Exception:
        sys.exit(usage)
    try:
        print (Fore.RED + 'Parsing on ' + Fore.GREEN + domain + Style.RESET_ALL + '\n')
        http = urllib3.PoolManager()
        req = http.request('GET', domain, headers = my_header).data.decode('utf-8', errors='ignore')
        return req
    except:
        sys.exit(error, domain)


def print_result(domain, host):
    total_bytes = 80
    space = 30
    len_domain = space - len(domain)
    p1 = Fore.RED  + 'Domain: ' + Style.RESET_ALL + domain + (len_domain * ' ') + Back.BLUE + ':' + Style.RESET_ALL
    len_host = total_bytes - (len(host) + len(p1))
    print(p1 + (len_host * ' ') + Fore.GREEN + host)


def parse_request(data):
    links = grep(pattern='href=', text=data)
    checked = []
    for link in links:
        link = link.split('href="')
        for result in grep(pattern='//', text=link):
            try:
                result = result.split('//')[1].split('"')[0].split('/')[0]
                if not result in checked:
                    checked.append(result)
                    host = socket.gethostbyname(result)
                    print_result(result,host)
            except Exception:
                pass
    print ('\n\n')


def main():
    clear_terminal()
    print_banner()
    data = get_domain()
    parse_request(data)


main()