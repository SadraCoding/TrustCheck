import requests
import re

def is_valid_eth_address(address):
    """Validate Ethereum address."""
    if not isinstance(address, str):
        return False
    if len(address) != 42:
        return False
    if not address.startswith("0x"):
        return False
    return bool(re.fullmatch(r'[0-9a-fA-F]{40}', address[2:]))

def check_token(token_address):
    """Check if the token is a honeypot using honeypot.is API."""
    api_url = f"https://api.honeypot.is/v2/IsHoneypot?address={token_address}"
    try:
        resp = requests.get(api_url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        is_honeypot = data.get("honeypotResult", {}).get("isHoneypot", False)
        message = "This token appears to be a honeypot! Exercise caution." if is_honeypot else "This token appears to be safe."
        return {
            "address": token_address,
            "isHoneypot": is_honeypot,
            "message": message
        }
    except requests.RequestException as e:
        return {"error": f"Error retrieving data: {e}"}

def main():
    print("Ethereum Honeypot Checker")
    print("Type 'exit' to quit.\n")

    while True:
        token_address = input("Enter Ethereum token address: ").strip()
        if token_address.lower() == 'exit':
            print("Goodbye!")
            break

        if not is_valid_eth_address(token_address):
            print("Invalid Ethereum address\n")
            continue

        result = check_token(token_address)
        if "error" in result:
            print(result["error"])
        else:
            print(f"Address: {result['address']}")
            print(f"Is Honeypot: {result['isHoneypot']}")
            print(f"Message: {result['message']}\n")

if __name__ == "__main__":
    main()
