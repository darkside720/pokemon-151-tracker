import os
import requests

# Top 20 most sought-after Gen 1 Pokémon
chase_pokemon = [
    "Charizard", "Blastoise", "Venusaur", "Pikachu", "Mewtwo", "Mew",
    "Gyarados", "Zapdos", "Moltres", "Articuno", "Dragonite", "Alakazam",
    "Snorlax", "Gengar", "Machamp", "Raichu", "Nidoking", "Clefairy",
    "Hitmonchan", "Chansey"
]

# API settings
API_URL = "https://api.pokemontcg.io/v2/cards"
HEADERS = {"X-Api-Key": "YOUR_API_KEY"}  # Replace with real key or remove if not needed

# Output directory
output_dir = "images/chase"
os.makedirs(output_dir, exist_ok=True)

for name in chase_pokemon:
    params = {
        "q": f'name:"{name}" supertype:"Pokémon"',
        "orderBy": "-set.releaseDate",
        "pageSize": 1
    }

    try:
        res = requests.get(API_URL, headers=HEADERS, params=params)
        res.raise_for_status()
        card = res.json()["data"][0]
        image_url = card["images"]["large"]
        file_name = f"{name}.jpg"
        img_data = requests.get(image_url).content

        with open(os.path.join(output_dir, file_name), "wb") as f:
            f.write(img_data)
        print(f"Downloaded: {name}")
    except Exception as e:
        print(f"Failed to get {name}: {e}")

