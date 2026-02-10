import itertools
import socket
import requests
import csv
import time


def check_domain(domain):
    """Check if domain resolves or responds to HTTP."""
    try:
        # Try DNS resolution
        socket.gethostbyname(domain)
        return "REGISTERED (resolves)"
    except socket.gaierror:
        # DNS failed, try HTTP anyway
        try:
            r = requests.get("http://" + domain, timeout=3)
            if r.status_code < 500:
                return "REGISTERED (http response)"
        except Exception:
            return "NO RESPONSE"
    return "NO RESPONSE"


def generate_domains():
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    # 1-char domains
    for c in chars:
        yield f"{c}.hk"
    # 2-char domains
    for c1, c2 in itertools.product(chars, repeat=2):
        yield f"{c1}{c2}.hk"


if __name__ == "__main__":
    with open("hk_domains.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["domain", "status"])  # header row

        for domain in generate_domains():
            status = check_domain(domain)
            writer.writerow([domain, status])
            print(f"{domain}: {status}")
            time.sleep(0.5)  # polite delay to avoid hammering servers
