from typing import Optional, TypedDict
from const import *

class QueueItem(TypedDict):
    pos: tuple[int, int]
    direction: int
    game_map: list[list[int]]
    path: list[int]

class MoveResult(TypedDict):
    pos: tuple[int, int]
    is_finished: bool


class Searcher:

    def __init__(self, game_map: list[list[int]]) -> None:
        for row in range(len(game_map)):
            for column in range(len(game_map[row])):
                if game_map[row][column] == START:
                    game_map[row][column] = NULL
                    self.queue = self.get_moveable_items(
                        {
                            "pos": (row, column),
                            "direction": UP,
                            "path": [],
                            "game_map": game_map
                        }
                    )
                    break

    def search(self, max_step: int = 12) -> list[int]:
        while True:
            item = self.queue.pop(0)
            result = self.move(item)
            if result["is_finished"]:
                return item["path"]
            item["pos"] = result["pos"]
            self.queue += self.get_moveable_items(item)
            if len(item["path"]) >= max_step:
                return []
    
    def move(self, queue_item: QueueItem) -> MoveResult:
        item = queue_item.copy()
        while True:
            moved_pos = self.get_moved_pos(item, item["direction"])
            moved_item = item["game_map"][moved_pos[0]][moved_pos[1]]
            if moved_item == WALL:
                return {
                    "is_finished": False,
                    "pos": item["pos"]
                }
            elif moved_item == SPECIAL:
                item["game_map"][moved_pos[0]][moved_pos[1]] = WALL
            elif moved_item == TERMINAL:
                return {
                    "is_finished": True,
                    "pos": moved_pos
                }
            item["pos"] = moved_pos



    def is_pos_moveable(self, game_map: list[list[int]], pos: tuple[int, int]) -> bool:
        return game_map[pos[0]][pos[1]] != WALL
    
    def get_moveable_items(self, parent_item: QueueItem) -> list[QueueItem]:
        items = []
        for d in [UP, DOWN, LEFT, RIGHT]:
            if item := self.get_queue_item(parent_item, d):
                items.append(item)
        return items

    def get_queue_item(self, parent_item: QueueItem, direction: int) -> Optional[QueueItem]:
        pos = self.get_moved_pos(parent_item, direction)
        if self.is_pos_moveable(parent_item["game_map"], pos):
            return {
                "pos": parent_item["pos"],
                "direction": direction,
                "game_map": parent_item["game_map"],
                "path": parent_item["path"] + [direction]
            }

    def get_moved_pos(self, queue_item: QueueItem, direction: int) -> tuple[int, int]:
        pos = list(queue_item["pos"])
        if direction == UP:
            pos[0] -= 1
        elif direction == DOWN:
            pos[0] += 1
        elif direction == RIGHT:
            pos[1] += 1
        elif direction == LEFT:
            pos[1] -= 1
        return pos[0], pos[1]
        

# class Searcher:

#     def __init__(self, game_map: list[list[int]]) -> None:
#         self.map = game_map
#         for row in range(len(self.map)):
#             for column in range(len(self.map[row])):
#                 if self.map[row][column] == START:
#                     self.queue = self.get_subnodes((row, column), [])
#                     self.map[row][column] = NULL
#                     break
        
#     def search(self, max_step: int = 12) -> list[int]:
#         while True:
#             item = self.queue.pop(0)
#             result = self.move(item["pos"], item["direction"])
#             if result["is_finished"]:
#                 return item["path"]
#             self.queue += self.get_subnodes(result["pos"], item["path"])
#             # print(len(item["path"]))
#             if len(item["path"]) >= max_step:
#                 return []

#     def get_subnodes(self, pos: tuple[int, int], path: list[int]) -> list[QueueItem]:
#         return [{
#             "pos": pos,
#             "direction": d,
#             "path": path + [d]
#         } for d in [UP, DOWN, LEFT, RIGHT] if self.map[(p := self.get_pos(pos, d))[0]][p[1]] != WALL]

#     def get_pos(self, pos: tuple[int, int], direction: int) -> tuple[int, int]:
#         player = list(pos)
#         if direction == UP:
#             player[0] -= 1
#         elif direction == DOWN:
#             player[0] += 1
#         elif direction == RIGHT:
#             player[1] += 1
#         elif direction == LEFT:
#             player[1] -= 1
#         return player[0], player[1]

#     def move(self, pos: tuple[int, int], direction: int) -> MoveResult:
#         original_pos = pos
#         while True:
#             pos = self.get_pos(original_pos, direction)
#             if self.map[pos[0]][pos[1]] == TERMINAL:
#                 original_pos = pos
#                 break
#             if self.map[pos[0]][pos[1]] not in [NULL, SPECIAL]:
#                 if self.map[pos[0]][pos[1]] == SPECIAL:
#                     self.map[pos[0]][pos[1]] = WALL
#                 break
#             original_pos = pos
#         return {
#             "pos": (original_pos[0], original_pos[1]),
#             "is_finished": self.map[original_pos[0]][original_pos[1]] == TERMINAL
#         }


if __name__ == "__main__":
    from map import generate
    game_map = generate()

    # game_map = [
    #     [1, 1, 1, 1, 3, 1, 1],
    #     [1, 0, 0, 2, 0, 0, 1],
    #     [1, 0, 0, 2, 0, 0, 1],
    #     [1, 0, 0, 2, 0, 0, 1],
    #     [1, 0, 4, 2, 0, 0, 1],
    #     [1, 1, 1, 1, 1, 1, 1]
    # ]
    print("\n".join(str(row) for row in game_map))
    searcher = Searcher(game_map)
    print(searcher.search())
