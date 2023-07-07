from typing import List, Dict, Any
from dataclasses import dataclass
import asyncio
import random
import time

MENU = [
    {"name": "fish",
     "cooking_time": 3},
    {"name": "beef",
     "cooking_time": 1},
    {"name": "pork",
     "cooking_time": 6},
    {"name": "vegetable",
     "cooking_time": 4},
    {"name": "rice",
     "cooking_time": 5},
    {"name": "pasta",
     "cooking_time": 2}
]


@dataclass
class Ingredient:
    name: str
    cooking_time: int


def load_menu(menu: List[Dict[str, Any]]) -> List[Ingredient]:
    return [Ingredient(**i) for i in menu]


def order_from_menu(ingredients_from_menu: List[Ingredient]) -> List[Ingredient]:
    return random.choices(ingredients_from_menu, k=random.randint(1, len(ingredients_from_menu)))


async def cook(ingredient: Ingredient):
    await asyncio.sleep(ingredient.cooking_time)


async def prepare_plate(cooked_ingredients: List[Ingredient]):
    await asyncio.sleep(len(cooked_ingredients))


async def serve_client(client_id: int, ordered_ingredients: List[Ingredient]):
    serve_start = time.perf_counter()
    print(f"Client {client_id} orders {[i.name for i in ordered_ingredients]}")
    await asyncio.gather(*[cook(i) for i in ordered_ingredients])
    await prepare_plate(ordered_ingredients)
    serve_end = time.perf_counter() - serve_start
    print(f"Meal for {client_id} done in {serve_end:0.2f}")


async def serve_group(nb_clients: int):
    ingredients = load_menu(MENU)
    await asyncio.gather(*[serve_client(i, order_from_menu(ingredients)) for i in range(nb_clients)])


start = time.perf_counter()
asyncio.run(serve_group(100))
end = time.perf_counter() - start
print(f"Order(s) prepared in {end:0.2f}")
