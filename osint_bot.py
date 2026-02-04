import requests
import json
import time
import os
import sys
import urllib.parse
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    banner = f"""
{Fore.CYAN}╔{'═' * 60}╗
{Fore.CYAN}║{Fore.GREEN}{Style.BRIGHT}   ██████  ███████ ██ ███    ██ ████████ {Fore.CYAN}║                             {Fore.CYAN}║{Fore.GREEN}{Style.BRIGHT}  ██    ██ ██      ██ ████   ██    ██    {Fore.CYAN}║
{Fore.CYAN}║{Fore.GREEN}{Style.BRIGHT}  ██    ██ ███████ ██ ██ ██  ██    ██    {Fore.CYAN}║                             {Fore.CYAN}║{Fore.GREEN}{Style.BRIGHT}  ██    ██      ██ ██ ██  ██ ██    ██    {Fore.CYAN}║                             {Fore.CYAN}║{Fore.GREEN}{Style.BRIGHT}   ██████  ███████ ██ ██   ████    ██    {Fore.CYAN}║
{Fore.CYAN}╚{'═' * 60}╝
{Fore.YELLOW}        >> v6.0 | OSINT LINKER | EXIT OPTION ENABLED <<
"""
    print(banner)


def get_user_input():
    print(f"{Fore.WHITE}{Back.RED} 🛠️  MAIN MENU {Style.RESET_ALL}")
    print(f"{Fore.GREEN} [1] 📱 MOBILE NO· LOOKUP")
    print(f"{Fore.BLUE} [2] 🆔 AADHAR ID LOOKUP")
    print(f"{Fore.RED} [0] 🚪 EXIT SYSTEM")

    while True:
        choice = input(f"\n{Fore.MAGENTA}┌──(Select Module)─╼ {Fore.WHITE}").strip()

        if choice == "1":
            term = input(f"{Fore.GREEN}└──╼ Enter Mobile Number: {Style.RESET_ALL}").strip()
            return term, "mobile", "ZYROBR0TH3R", "http://osintx.info/API/krobetahack.php"
        elif choice == "2":
            term = input(f"{Fore.BLUE}└──╼ Enter ID Number: {Style.RESET_ALL}").strip()
            return term, "id_number", "XXYYZZZYRO", "https://osintx.info/API/krobetahack.php"
        elif choice == "0":
            print(f"\n{Fore.RED}🔴 Connection Terminated. Goodbye!")
            sys.exit()
        else:
            print(f"{Fore.RED}⚠️ Invalid choice! Please try again.")

def generate_map_link(address):
    """Convert address to Google Maps search link"""
    if not address or address == "N/A":
        return None
    base_url = "https://www.google.com/maps/search/"
    return base_url + urllib.parse.quote(str(address))

def display_smart_table(data):
    if not data:
        print(f"\n{Fore.RED}🚫 [EMPTY RESPONSE] - No data found.")
        return

    icons = {
        "name": "👤",
        "fname": "👨‍👦",
        "address": "🏠",
        "city": "🏙️",
        "nic": "🆔",
        "number": "📞",
        "operator": "📡",
        "date": "📅",
        "location": "📍",
    }

    print(f"\n{Fore.YELLOW}╔═{'═' * 28}═╦═{'═' * 45}═╗")
    print(f"{Fore.YELLOW}║ {Fore.CYAN}{Style.BRIGHT}{'FIELD NAME':^28} {Fore.YELLOW}║ {Fore.CYAN}{Style.BRIGHT}{'EXTRAC>
    print(f"{Fore.YELLOW}╠═{'═' * 28}═╬═{'═' * 45}═╣")

    address_val = None

    if isinstance(data, list) and data:
        items = data[0].items()
    elif isinstance(data, dict):
        items = data.items()
    else:
        print(f"{Fore.RED}❌ Unknown data format")
        return

    for key, value in items:
        icon = icons.get(key.lower(), "🔹")
        key_label = f"{icon} {key.upper()}"

        if key.lower() in ["address", "location", "city"]:
            if value and value != "N/A":
                address_val = value

        print(
            f"{Fore.YELLOW}║ {Fore.GREEN}{key_label:<28} {Fore.YELLOW}║ {Fore.WHITE}{str(value)[:45]:<45} {Fore.YELLOW}>
        )

    if address_val:
        map_link = generate_map_link(address_val)
        print(f"{Fore.YELLOW}╠═{'═' * 28}═╬═{'═' * 45}═╣")
        print(
            f"{Fore.YELLOW}║ {Fore.RED}{'📍 MAP LINK':<28} {Fore.YELLOW}║ {Fore.BLUE}{map_link[:45]:<45} {Fore.YELLOW}║"
        )
        if len(map_link) > 45:
            print(
                f"{Fore.YELLOW}║ {'':<28} {Fore.YELLOW}║ {Fore.BLUE}{map_link[45:90]:<45} {Fore.YELLOW}║"
            )

    print(f"{Fore.YELLOW}╚═{'═' * 28}═╩═{'═' * 45}═╝")
    print(f"{Fore.GREEN}✅ RECON COMPLETE.")

def main():
    while True:
        print_banner()
        term, api_type, api_key, base_url = get_user_input()

        print(f"\n{Fore.CYAN}📡 Requesting Data...", end="\r")

        try:
            api_url = f"{base_url}?key={api_key}&type={api_type}&term={term}"
            response = requests.get(api_url, timeout=20)

            if response.status_code == 200:
                try:
                    result_data = response.json()
                    display_smart_table(result_data)
                except json.JSONDecodeError:
                    print(f"\n{Fore.YELLOW}📝 Raw Output: {Fore.WHITE}{response.text}")
            else:
                print(f"\n{Fore.RED}❌ Server Error: {response.status_code}")

        except Exception as e:
            print(f"\n{Fore.RED}🛑 Error: {e}")

        print(f"\n{Fore.YELLOW}Press Enter to go back to Menu...")
        input()

if __name__ == "__main__":
    main()
