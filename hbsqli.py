import argparse
import requests
from rich.console import Console

# Rich Console
console = Console()

# Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list', help='To provide list of urls as an input')
parser.add_argument('-u', '--url', help='To provide single url as an input')
parser.add_argument('-p', '--payloads', help='To provide payload file having Blind SQL Payloads with delay of 30 sec', required=True)
parser.add_argument('-H', '--headers', help='To provide header file having HTTP Headers which are to be injected', required=True)
parser.add_argument('-v', '--verbose', help='Run on verbose mode', action='store_true')
args = parser.parse_args()

# Header Payload Creation
try:
    with open(args.payloads, 'r') as file:
        payloads = [line.strip() for line in file]
except FileNotFoundError as e:
    print(str(e))
except PermissionError as e:
    print(str(e))
except IOError as e:
    print(str(e))

try:
    with open(args.headers, 'r') as file:
        headers = [line.strip() for line in file]
except FileNotFoundError as e:
    print(str(e))
except PermissionError as e:
    print(str(e))
except IOError as e:
    print(str(e))

headers_list = []

for header in headers:
    for payload in payloads:
        var = header + ": " + payload
        headers_list.append(var)

headers_dict = {header: header.split(": ")[1] for header in headers_list}

# For File as an Input
def onfile():
    with open(args.list, 'r') as file:
        urls = [line.strip() for line in file]

    for url in urls:
        for header in headers_dict:
            cust_header = {header.split(": ")[0]: header.split(": ")[1]}
            try:
                response = requests.get(url, headers=cust_header, timeout=60, allow_redirects=True)
                res_time = response.elapsed.total_seconds()

                if 25 <= res_time <= 50:
                    console.print("🌐 [bold][cyan]Testing for URL: [/][/]", url)
                    console.print("💉 [bold][cyan]Testing for Header: [/][/]", repr(header))
                    console.print("⏱️ [bold][cyan]Response Time: [/][/]", repr(res_time))
                    console.print("🐞 [bold][cyan]Status: [/][red]Vulnerable[/][/]")
                    print()
            except (UnicodeDecodeError, AssertionError, TimeoutError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                print(f"The request was not successful due to: {e}")
                print()
                pass

# For File as an Input-Verbose
def onfile_v():
    with open(args.list, 'r') as file:
        urls = [line.strip() for line in file]

    for url in urls:
        for header in headers_dict:
            cust_header = {header.split(": ")[0]: header.split(": ")[1]}
            console.print("🌐 [bold][cyan]Testing for URL: [/][/]", url)
            console.print("💉 [bold][cyan]Testing for Header: [/][/]", repr(header))
            try:
                response = requests.get(url, headers=cust_header, timeout=60, allow_redirects=True)
                console.print("🔢 [bold][cyan]Status code: [/][/]", response.status_code)
                res_time = response.elapsed.total_seconds()
                console.print("⏱️ [bold][cyan]Response Time: [/][/]", repr(res_time))

                if 25 <= res_time <= 50:
                    console.print("[🐞bold][cyan]Status: [/][red]Vulnerable[/][/]")
                    print()
                else:
                    console.print("🐞[bold][cyan]Status: [/][green]Not Vulnerable[/][/]")
                    print()
            except (UnicodeDecodeError, AssertionError, TimeoutError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                print(f"The request was not successful due to: {e}")
                print()
                pass

# For URL as an Input
def onurl():
    url = args.url

    for header in headers_dict:
        cust_header = {header.split(": ")[0]: header.split(": ")[1]}
        try:
            response = requests.get(url, headers=cust_header, timeout=60, allow_redirects=True)
            res_time = response.elapsed.total_seconds()

            if 25 <= res_time <= 50:
                console.print("🌐 [bold][cyan]Testing for URL: [/][/]", url)
                console.print("💉 [bold][cyan]Testing for Header: [/][/]", repr(header))
                console.print("⏱️ [bold][cyan]Response Time: [/][/]", repr(res_time))
                console.print("🐞 [bold][cyan]Status: [/][red]Vulnerable[/][/]")
                print()
        except (UnicodeDecodeError, AssertionError, TimeoutError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            print(f"The request was not successful due to: {e}")
            print()
            pass

# For URL as an Input-Verbose
def onurl_v():
    url = args.url

    for header in headers_dict:
        cust_header = {header.split(": ")[0]: header.split(": ")[1]}
        console.print("🌐 [bold][cyan]Testing for URL: [/][/]", url)
        console.print("💉 [bold][cyan]Testing for Header: [/][/]", repr(header))
        try:
            response = requests.get(url, headers=cust_header, timeout=60, allow_redirects=True)
            console.print("🔢 [bold][cyan]Status code: [/][/]", response.status_code)
            res_time = response.elapsed.total_seconds()
            console.print("⏱️ [bold][cyan]Response Time: [/][/]", repr(res_time))

            if 25 <= res_time <= 50:
                console.print("🐞 [bold][cyan]Status: [/][red]Vulnerable[/][/]")
                print()
            else:
                console.print("🐞[bold][cyan]Status: [/][green]Not Vulnerable[/][/]")
                print()
        except (UnicodeDecodeError, AssertionError, TimeoutError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            print(f"The request was not successful due to: {e}")
            print()
            pass

if args.url is not None:
    if args.verbose:
        onurl_v()
    else:
        onurl()
elif args.list is not None:
    if args.verbose:
        onfile_v()
    else:
        onfile()
else:
    print("Error: One out of the two flag -u or -l is required")
