import json

with open("./test_base.json", "r", encoding="utf8") as file:
    all_pokemon = json.load(file)


class Pokemon:
    def __init__(self, data):
        self.num = data.get("num")
        self.name = data.get("name")
        self.evos = data.get("evos", [])
        self.prevo = data.get("prevo")


def get_evolution_chain(pokemon_data, all_pokemon):
    """
    This function builds the evolution chain for a Pokemon from the provided data.

    Args:
        pokemon_data: A dictionary containing data for the starting Pokemon.
        all_pokemon: A dictionary containing data for all Pokemon.

    Returns:
        A list of Pokemon objects representing the evolution chain.
    """
    chain = []
    current_pokemon = pokemon_data
    while current_pokemon:
        pokemon_obj = Pokemon(current_pokemon)
        chain.append(pokemon_obj)
        current_pokemon = all_pokemon.get(pokemon_obj.prevo)
    return chain


def print_evolution_chain(chain):
    """
    This function prints information about the evolution chain.

    Args:
        chain: A list of Pokemon objects representing the evolution chain.
    """
    print("Evolution Chain:")
    for i, pokemon in enumerate(chain):
        if i > 0:
            evo_level = all_pokemon.get(pokemon.prevo, {}).get("evoLevel")
            if evo_level:
                print(f"  - Evolves from: {chain[i-1].name} (Lv. {evo_level})")
            else:
                print(f"  - Evolves from: {chain[i-1].name}")
        print(f"  - {pokemon.name} (#{pokemon.num})")


# Example usage
pokemon_data = {
    "cyndaquil": {
        "num": 155,
        "name": "Cyndaquil",
        "types": ["Fire"],
        "genderRatio": {"M": 0.875, "F": 0.125},
        "baseStats": {
            "hp": 39,
            "atk": 52,
            "def": 43,
            "spa": 60,
            "spd": 50,
            "spe": 65,
        },
        "abilities": {"0": "Blaze", "H": "Flash Fire"},
        "heightm": 0.5,
        "weightkg": 7.9,
        "color": "Yellow",
        "evos": ["Quilava"],
        "eggGroups": ["Field"],
    },
    "quilava": {
        "num": 156,
        "name": "Quilava",
        "types": ["Fire"],
        "genderRatio": {"M": 0.875, "F": 0.125},
        "baseStats": {
            "hp": 58,
            "atk": 64,
            "def": 58,
            "spa": 80,
            "spd": 65,
            "spe": 80,
        },
        "abilities": {"0": "Blaze", "H": "Flash Fire"},
        "heightm": 0.9,
        "weightkg": 19,
        "color": "Yellow",
        "prevo": "Cyndaquil",
        "evoLevel": 14,
        "evos": ["Typhlosion", "Typhlosion-Hisui"],
        "eggGroups": ["Field"],
    },
    "typhlosion": {
        "num": 157,
        "name": "Typhlosion",
        "types": ["Fire"],
        "genderRatio": {"M": 0.875, "F": 0.125},
        "baseStats": {
            "hp": 78,
            "atk": 84,
            "def": 78,
            "spa": 109,
            "spd": 85,
            "spe": 100,
        },
        "abilities": {"0": "Blaze", "H": "Flash Fire"},
        "heightm": 1.7,
        "weightkg": 79.5,
        "color": "Yellow",
        "prevo": "Quilava",
        "evoLevel": 36,
        "eggGroups": ["Field"],
        "otherFormes": ["Typhlosion-Hisui"],
        "formeOrder": ["Typhlosion", "Typhlosion-Hisui"],
    },
    "typhlosionhisui": {
        "num": 157,
        "name": "Typhlosion-Hisui",
        "baseSpecies": "Typhlosion",
        "forme": "Hisui",
        "types": ["Fire", "Ghost"],
        "genderRatio": {"M": 0.875, "F": 0.125},
        "baseStats": {
            "hp": 73,
            "atk": 84,
            "def": 78,
            "spa": 119,
            "spd": 85,
            "spe": 95,
        },
        "abilities": {"0": "Blaze", "H": "Frisk"},
        "heightm": 1.6,
        "weightkg": 69.8,
        "color": "Yellow",
        "prevo": "Quilava",
        "evoLevel": 36,
        "eggGroups": ["Field"],
    },
}

# Assuming all_pokemon dictionary contains data for all Pokemon
chain = get_evolution_chain(pokemon_data["cyndaquil"], all_pokemon)
print_evolution_chain(chain)
