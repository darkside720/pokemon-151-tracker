import os
import requests

SAVE_DIR = "pokemon_images"
os.makedirs(SAVE_DIR, exist_ok=True)

TCG_SEARCH_URL = "https://api.pokemontcg.io/v2/cards"
HEADERS = {"X-Api-Key": ""}  # Optional: add your TCG API key here

pokemon_list = [
    "bulbasaur", "ivysaur", "venusaur", "charmander", "charmeleon", "charizard", "squirtle", "wartortle", "blastoise", "caterpie",
    "metapod", "butterfree", "weedle", "kakuna", "beedrill", "pidgey", "pidgeotto", "pidgeot", "rattata", "raticate",
    "spearow", "fearow", "ekans", "arbok", "pikachu", "raichu", "sandshrew", "sandslash", "nidoran♀", "nidorina",
    "nidoqueen", "nidoran♂", "nidorino", "nidoking", "clefairy", "clefable", "vulpix", "ninetales", "jigglypuff", "wigglytuff",
    "zubat", "golbat", "oddish", "gloom", "vileplume", "paras", "parasect", "venonat", "venomoth", "diglett",
    "dugtrio", "meowth", "persian", "psyduck", "golduck", "mankey", "primeape", "growlithe", "arcanine", "poliwag",
    "poliwhirl", "poliwrath", "abra", "kadabra", "alakazam", "machop", "machoke", "machamp", "bellsprout", "weepinbell",
    "victreebel", "tentacool", "tentacruel", "geodude", "graveler", "golem", "ponyta", "rapidash", "slowpoke", "slowbro",
    "magnemite", "magneton", "farfetch’d", "doduo", "dodrio", "seel", "dewgong", "grimer", "muk", "shellder",
    "cloyster", "gastly", "haunter", "gengar", "onix", "drowzee", "hypno", "krabby", "kingler", "voltorb",
    "electrode", "exeggcute", "exeggutor", "cubone", "marowak", "hitmonlee", "hitmonchan", "lickitung", "koffing", "weezing",
    "rhyhorn", "rhydon", "chansey", "tangela", "kangaskhan", "horsea", "seadra", "goldeen", "seaking", "staryu",
    "starmie", "mr. mime", "scyther", "jynx", "electabuzz", "magmar", "pinsir", "tauros", "magikarp", "gyarados",
    "lapras", "ditto", "eevee", "vaporeon", "jolteon", "flareon", "porygon", "omanyte", "omastar", "kabuto",
    "kabutops", "aerodactyl", "snorlax", "articuno", "zapdos", "moltres", "dratini", "dragonair", "dragonite", "mewtwo",
    "mew"
]

def sanitize(name):
    return name.lower().replace('♀', 'f').replace('♂', 'm').replace('.', '').replace('’', '').replace(' ', '-')

def download_tcg_image(pokedex_num, padded_num, name):
    query_url = f"{TCG_SEARCH_URL}?q=nationalPokedexNumbers:{pokedex_num}"
    try:
        r = requests.get(query_url, headers=HEADERS)
        r.raise_for_status()
        cards = r.json().get("data", [])
        if not cards:
            return False

        # Prefer Base Set card
        base_card = next((card for card in cards if "Base" in card.get("set", {}).get("name", "")), cards[0])
        image_url = base_card["images"]["large"]
        img_data = requests.get(image_url).content
        filename = f"{SAVE_DIR}/{padded_num}-{sanitize(name)}.jpg"
        with open(filename, "wb") as f:
            f.write(img_data)
        print(f"✅ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"⚠️  Error getting TCG card for #{pokedex_num} {name}: {e}")
        return False

def download_fallback(padded_num, name):
    fallback_url = f"https://img.pokemondb.net/artwork/large/{sanitize(name)}.jpg"
    try:
        img_data = requests.get(fallback_url).content
        filename = f"{SAVE_DIR}/{padded_num}-{sanitize(name)}.jpg"
        with open(filename, "wb") as f:
            f.write(img_data)
        print(f"🔁 Fallback downloaded: {filename}")
    except Exception as e:
        print(f"❌ Failed fallback for {name}: {e}")

def main():
    for i, name in enumerate(pokemon_list):
        padded_num = str(i + 1).zfill(3)
        success = download_tcg_image(i + 1, padded_num, name)
        if not success:
            download_fallback(padded_num, name)

if __name__ == "__main__":
    main()

