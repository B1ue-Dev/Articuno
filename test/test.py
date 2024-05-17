# import json

# db = json.loads(open("./test.json", "r", encoding="utf8").read())

# # Initialize an empty dictionary to store the exported species
# exported_species = {}

# generation_ranges = {
#     "1": [1, 151],
#     "2": [152, 251],
#     "3": [252, 386],
#     "4": [387, 493],
#     "5": [494, 649],
#     "6": [650, 721],
#     "7": [722, 809],
#     "8": [810, 905],
#     "9": [906, 1010]
# }

# # Iterate through each Pokémon entry
# for key, value in db.items():
#     if "name" in value and "Hisui" in value["name"]:
#         num = value["num"]
#         for gen, (start, end) in generation_ranges.items():
#             if start <= num <= end:
#                 exported_species[key] = {
#                     "num": value["num"],
#                     "name": f"""Hisuian {value["baseSpecies"]}""",
#                     "description": "If its rage peaks, it becomes so hot that anything that touches it will instantly go up in flames.",
#                     "generation": int(gen),
#                     "types": value["types"],
#                     "baseStats": {
#                         "hp": value["baseStats"]["hp"],
#                         "atk": value["baseStats"]["atk"],
#                         "def": value["baseStats"]["def"],
#                         "spa": value["baseStats"]["spa"],
#                         "spd": value["baseStats"]["spd"],
#                         "spe": value["baseStats"]["spe"]
#                     },
#                     "abilities": value["abilities"],
#                     "heightm": value["heightm"],
#                     "weightkg": value["weightkg"],
#                     "color": value["color"],
#                     "eggGroups": value["eggGroups"],
#                 }

# with open("test_export.json", "w") as outfile:
#     json.dump(exported_species, outfile, indent=4)

# print("Exported species saved to 'exported_species.json'")
# import json


# base: dict = json.loads(open("./src/db/pokemon.json", "r", encoding="utf8").read())
# hisui: dict = json.loads(open("./test_export.json", "r", encoding="utf8").read())
# merged_data = dict()

# # Loop through base data
# for base_key, base_value in base.items():

#     for hisui_key, hisui_value in hisui.items():

#         if base_key not in merged_data.keys():
#             merged_data[base_key] = base_value
#         # If the num in base and hisui match
#         if base_value["num"] == hisui_value["num"]:
#             print(base_key, base_value["evolutionLine"])
#             merged_data[hisui_key] = hisui_value
#             merged_data[hisui_key]["description"] = "Hisuian form. " +base_value["description"]

#             merged_data[hisui_key]["evolutionLine"] = (base_value["evolutionLine"].append(hisui_value["name"]))
#             print("done")

# with open("test.json", "w", encoding="utf8") as outfile:
#     json.dump(merged_data, outfile, indent=4, ensure_ascii=False)

# print("Exported!")
import json
import re
import requests
from time import sleep

# Load the JSON data
db: list[str] = json.loads(
    open("./test_base.json", "r", encoding="utf8").read()
)

generation_ranges = {
    "1": [1, 151],
    "2": [152, 251],
    "3": [252, 386],
    "4": [387, 493],
    "5": [494, 649],
    "6": [650, 721],
    "7": [722, 809],
    "8": [810, 905],
    "9": [906, 1025],
}
exported_species = {}

# Iterate through each Pokémon entry
for key, value in db.items():
    sleep(0.1)
    added: bool = False
    num = value["num"]
    for gen, (start, end) in generation_ranges.items():
        if start <= num <= end:
            if value.get("baseSpecies") is None:

                def returnkey(text):
                    # Remove non-alphabetic characters using regular expression
                    r = re.sub(r"[^a-zA-Z]", "", text)
                    return r.lower()

                prevo = value.get("prevo")
                evos = value.get("evos")
                evolution_chain = []

                if prevo:
                    evolution_chain.append(prevo)
                    _check = db[returnkey(prevo)].get("prevo")
                    if _check:
                        evolution_chain.insert(0, _check)

                evolution_chain.append(value["name"])

                if evos:
                    for evo in evos:
                        evolution_chain.append(evo)
                    for evo in evos[1:]:
                        _check = db[returnkey(evos[0])].get("evos")
                        if _check:
                            for _evo in _check:
                                evolution_chain.append(_evo)

                if len(evolution_chain) == 1:
                    evolution_chain = []

                description = None
                res = (
                    requests.get(
                        f"https://pokeapi.co/api/v2/pokemon-species/{int(num)}/"
                    )
                ).json()
                for entry in res["flavor_text_entries"]:
                    if entry["language"]["name"] == "en":
                        description = (
                            entry["flavor_text"]
                            .replace("\n", " ")
                            .replace("\f", " ")
                        )
                        break
                exported_species[key] = {
                    "num": value["num"],
                    "name": value["name"],
                    "description": description,
                    "generation": int(gen),
                    "types": value["types"],
                    "baseStats": {
                        "hp": value["baseStats"]["hp"],
                        "atk": value["baseStats"]["atk"],
                        "def": value["baseStats"]["def"],
                        "spa": value["baseStats"]["spa"],
                        "spd": value["baseStats"]["spd"],
                        "spe": value["baseStats"]["spe"],
                    },
                    "abilities": value["abilities"],
                    "heightm": value["heightm"],
                    "weightkg": value["weightkg"],
                    "color": value["color"],
                    "eggGroups": value["eggGroups"],
                    "evolutionLine": evolution_chain,
                }
                if value.get("otherFormes"):
                    other_formes = []
                    for forme in value["otherFormes"]:
                        if "-" not in forme:
                            other_formes.append(forme)
                    if other_formes:
                        exported_species[key]["otherFormes"] = other_formes
                added = True
            elif "Hisui" in value["name"]:
                description = None

                def returnkey(text):
                    # Remove non-alphabetic characters using regular expression
                    r = re.sub(r"[^a-zA-Z]", "", text)
                    return r.lower()

                prevo = value.get("prevo")
                evos = value.get("evos")
                evolution_chain = []

                if prevo:
                    evolution_chain.append(prevo)
                    _check = db[returnkey(prevo)].get("prevo")
                    if _check:
                        evolution_chain.insert(0, _check)

                evolution_chain.append(value["name"])

                if evos:
                    for evo in evos:
                        evolution_chain.append(evo)
                    for evo in evos[1:]:
                        _check = db[returnkey(evos[0])].get("evos")
                        if _check:
                            for _evo in _check:
                                evolution_chain.append(_evo)

                if len(evolution_chain) == 1:
                    evolution_chain = []

                res = (
                    requests.get(
                        f"https://pokeapi.co/api/v2/pokemon-species/{int(num)}/"
                    )
                ).json()
                for entry in res["flavor_text_entries"]:
                    if entry["version"]["name"] == "legends-arceus":
                        description = (
                            entry["flavor_text"]
                            .replace("\n", " ")
                            .replace("\f", " ")
                        )
                        break

                exported_species[key] = {
                    "num": value["num"],
                    "name": "Hisuian " + f"""{value["baseSpecies"]}""",
                    "description": description.replace("\n", " "),
                    "generation": int(8),
                    "types": value["types"],
                    "baseStats": {
                        "hp": value["baseStats"]["hp"],
                        "atk": value["baseStats"]["atk"],
                        "def": value["baseStats"]["def"],
                        "spa": value["baseStats"]["spa"],
                        "spd": value["baseStats"]["spd"],
                        "spe": value["baseStats"]["spe"],
                    },
                    "abilities": value["abilities"],
                    "heightm": value["heightm"],
                    "weightkg": value["weightkg"],
                    "color": value["color"],
                    "eggGroups": value["eggGroups"],
                    "evolutionLine": evolution_chain,
                }
                added = True

            if added:
                print(
                    f"""Exported: {key}\n{description}\n{num}/1025 {"{:.2f}%".format(round(int(num) / 1025 * 100, 2))}"""
                )

# Export the exported_species dictionary to a JSON file
with open("test.json", "w", encoding="utf-8") as outfile:
    json.dump(exported_species, outfile, indent=4, ensure_ascii=False)

print("Exported species saved to 'test.json'")
