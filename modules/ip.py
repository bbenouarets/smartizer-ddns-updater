import requests
import json

RESOLVER = "https://api.ipify.org?format=json"

class PublicIPResolver:
    def __init__(self) -> None:
        pass

    def __call__(self) -> str:
        res = requests.get("https://api.ipify.org?format=json").json()
        return res["ip"]