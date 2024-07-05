#!/usr/bin/env python3

""""Script to generate weapon / plug CSVs from the Bungie API"""
import json
import csv
import enum
import types


class ItemType(enum.IntEnum):
    """DestinyItemType"""

    WEAPON = 3
    MOD = 19
    PATTERN = 30


class ItemCategory(enum.IntEnum):
    """DestinyInventoryCategoryDefinition"""

    WEAPON_MODS = 610365472


class SocketCategory(enum.IntEnum):
    """DestinySocketCategoryDefinition"""

    INTRINSIC = 3956125808
    WEAPON_PERK = 4241085061


def write_csv(filename, fields, rows):
    """Write fieldnames and rows to filename.csv"""
    with open(f"{filename}.csv", "w+", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fields)
        writer.writeheader()
        writer.writerows(rows)


def get_damage_type(json, item):
    return json[str(item.crafting["outputItemhash"]["defaultDamageType"])]


PATTERN_FIELDS = [
    "hash",
    "name",
    "itemTypeDisplayName",
    "defaultDamageType",
    "icon path",
]
MOD_FIELDS = ["hash", "itemTypeDisplayName", "name", "icon path"]
TRAIT_FIELDS = ["hash", "name", "icon path"]

patterns = []
with open("DestinyInventoryItemDefinition.json", "r", encoding="utf-8") as inventory_file:
    json = json.load(inventory_file)  # , object_hook=lambda d: types.SimpleNamespace(**d))

for key in json:
    item = types.SimpleNamespace(**json[key])
    display = types.SimpleNamespace(**item.displayProperties)
    # We only care about patterns and non-adept items.
    if item.itemType != ItemType.PATTERN or display.name[-1:] == ")":
        continue
    patterns.append(
        {
            PATTERN_FIELDS[0]: item.hash,
            PATTERN_FIELDS[1]: display.name,
            PATTERN_FIELDS[2]: item.itemTypeDisplayName,
            PATTERN_FIELDS[3]: get_damage_type(json, item),
            PATTERN_FIELDS[4]: display.icon,
        }
    )

write_csv("patterns", PATTERN_FIELDS, patterns)
# write_csv("mods", MOD_FIELDS, mods)
