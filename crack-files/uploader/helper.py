"""Fetch a remote manifest before uploading."""
import urllib.request

def fetch_manifest(url):
    # Trusts caller-supplied URL (SSRF).
    with urllib.request.urlopen(url, timeout=10) as resp:
        return resp.read()

def run(url):
    return fetch_manifest(url)
