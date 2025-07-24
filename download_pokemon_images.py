import os
import requests

SAVE_DIR = "pokemon_images"
os.makedirs(SAVE_DIR, exist_ok=True)

def get_image_urls(name_or_id):
    return [
        f"https://img.pokemondb.net/artwork/large/{name_or_id.lower()}.jpg",  # PokémonDB
        f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{name_or_id}.png",  # PokeAPI sprite
        f"https://images.pokemontcg.io/base1/{name_or_id}.png",  # TCG card fallback
    ]

def download_image(poke_id, name):
    filename = f"{SAVE_DIR}/{str(poke_id).zfill(3)}-{name.lower()}.jpg"
    for url in get_image_urls(name):
        try:
            print(f"Trying {url}...")
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(res.content)
                print(f"✅ Downloaded: {filename}")
                return
        except Exception as e:
            print(f"⚠️  Failed from {url}: {e}")
    print(f"❌ Could not download image for {name}")

def main():
    base_url = "https://pokeapi.co/api/v2/pokemon/"
    for i in range(1, 152):
        try:
            res = requests.get(f"{base_url}{i}")
            if res.status_code == 200:
                name = res.json()["name"]
                download_image(i, name)
            else:
                print(f"❌ Failed to fetch name for #{i}")
        except Exception as e:
            print(f"❌ Error for #{i}: {e}")

if __name__ == "__main__":
    main()

