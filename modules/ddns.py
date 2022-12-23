import os
import sys
import json
import uuid

from .handler import Hetzner

from rich.table import Table
from rich.console import Console
from rich.text import Text

console = Console()

PROVIDER = ["hetzner"]

class DDNSUpdater:
    def __init__(self) -> None:
        pass

    def init(self, provider: str = "hetzner", key: str = None) -> None:
        print()
        self.provider = provider.lower()
        self.api_key = key
        if not self.provider in PROVIDER:
            console.print("Please choose a supported DNS provider!", style="bold red")
            sys.exit(1)
        match (self.provider):
            case "hetzner":
                self.HANDLER = Hetzner(key=key)
        self.zone_id, self.zone_name = self.zones()
        self.record_id, self.record_name = self.records()
        self.data = json.dumps({
            "provider": self.provider,
            "api_key": self.api_key,
            "zone": 
            {
                "id": self.zone_id,
                "name": self.zone_name,
            },
            "records": 
            [
                {
                    "id": self.record_id,
                    "name": self.record_name
                }
            ]
        })
        self.profile_id = uuid.uuid4()
        with open(f"profiles/{self.profile_id}.json", "w") as f:
            f.write(self.data)
            f.close()
        print(f"\nProfile was created! ID: {self.profile_id}")

    def update(self, profile: str = None) -> None:
        PROFILE_PATH = f"profiles/{profile}.json"
        if not os.path.exists(PROFILE_PATH):
            console.print("Profile not found!", style="bold red")
            sys.exit(1)
        with open(PROFILE_PATH, "r") as f:
            data = json.load(f)
        self.api_key = data["api_key"]
        if not data["provider"] in PROVIDER:
            console.print("Please choose a supported DNS provider!", style="bold red")
            sys.exit(1)
        match (data["provider"]):
            case "hetzner":
                self.HANDLER = Hetzner(key=self.api_key)
        zone_id = data["zone"]["id"]
        zone_name = data["zone"]["name"]
        for record in data["records"]:
            record_name = record["name"]
            res = self.HANDLER.update_records(zone=zone_id, record=record)
            if res["status"] == 200 or res["status"] == 201:
                console.print(f"Record {record_name} updated successfully!", style="bold green")
            else:
                console.print(f"Record {record_name} couldn't updated successfully!", style="bold red")
                sys.exit(1)

    def read_config(self, path: str = "profiles", name: str = None) -> None:
        if name is None:
            return None
        self.CONFIG_PATH = f"{path}/{name}.json"
        if os.path.exists(self.CONFIG_PATH):
            if os.path.isfile(self.CONFIG_PATH):
                try:
                    with open(self.CONFIG_PATH, "r") as f:
                        data = f.read()
                        return data
                except Exception as e:
                    console.print("Config file couldn't readed!", style="bold red")
                    sys.exit(1)
            else:
                return None
        else:
            return None

    def zones(self) -> str:
        print()
        zones = self.HANDLER.get_zones()
        zone_count = 0
        t = Table(title=self.HANDLER.NAME)
        t.add_column("ID")
        t.add_column("Name")
        t.add_column("Unqiue ID")
        for zone in zones:
            zone_count += 1
            ID = zone_count
            ZONE_ID = zone["id"]
            ZONE_NAME = zone["name"]
            t.add_row(str(ID), ZONE_NAME, ZONE_ID)
        console.print(t)
        choose = int(input("Please choose a zone: "))
        if choose < (zone_count + 1):
            console.print(zones[choose - 1]["name"], style="bold blue")
        else:
            console.print("Please choose a existing zone!", style="bold red")
            sys.exit()
        return zones[choose - 1]["id"], zones[choose - 1]["name"]

    def records(self) -> str:
        print()
        records = self.HANDLER.get_records(zone=self.zone_id)
        record_count = 0
        t = Table(title=self.HANDLER.NAME)
        t.add_column("ID")
        t.add_column("Name")
        t.add_column("Unqiue ID")
        for record in records:
            record_count += 1
            ID = record_count
            ZONE_ID = record["id"]
            ZONE_NAME = record["name"]
            t.add_row(str(ID), ZONE_NAME, ZONE_ID)
        console.print(t)
        choose = int(input("Please choose a zone: "))
        if choose < (record_count + 1):
            console.print(records[choose - 1]["name"], style="bold blue")
        else:
            console.print("Please choose a existing zone!", style="bold red")
            sys.exit()
        return records[choose - 1]["id"], records[choose - 1]["name"]