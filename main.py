from map import generate
from search import Searcher

game_map = generate()
print("Map:")
print("\n".join(str(row) for row in game_map))

print("\nSteps (MIN):")
print(Searcher(game_map).search())


