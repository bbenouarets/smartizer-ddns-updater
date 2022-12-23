import requests
import json

from ..ip import PublicIPResolver

ENDPOINT = "https://dns.hetzner.com/api/v1"

ip = PublicIPResolver()

class Hetzner:
    def __init__(self, key: str = None) -> None:
        if key is None:
            raise ValueError("API Key must specifed!")
        self.API_KEY = key
        self.HEADERS = {
            "Auth-API-Token": self.API_KEY
        }
        self.NAME = "Hetzner"

    def get_zones(self) -> None:
        URL = f"{ENDPOINT}/zones"
        res = requests.get(url=URL, headers=self.HEADERS)
        if res.status_code == 404:
            return {
                "status": 404
            }
        return res.json()["zones"]

    def get_records(self, zone: str = None) -> None:
        URL = f"{ENDPOINT}/records?zone_id={zone}"
        res = requests.get(url=URL, headers=self.HEADERS)
        if res.status_code == 404:
            return {
                "status": 404
            }
        return res.json()["records"]

    def update_records(self, zone: str = None, record: dict = None) -> None:
        RECORD_ID = record["id"]
        URL = f"{ENDPOINT}/records/{RECORD_ID}"
        PUBLIC_IP = ip()
        res = requests.put(url=URL, headers=self.HEADERS, data=json.dumps({
            "zone_id": zone,
            "type": "A",
            "name": record["name"],
            "value": PUBLIC_IP,
            "ttl": 86400
        }))
        print(res.status_code)
        if res.status_code == 404:
            return {
                "status": 404
            }
        if res.status_code == 200 or res.status_code == 201:
            return {
                "status": res.status_code
            }
