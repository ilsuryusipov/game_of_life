#!/usr/bin/python3

import copy
import time
from random import randint

class Life:
    ## Public
    def __init__(self, rows_count: int = randint(5,10), columns_count: int = randint(5,10)) -> None:
        self.game_over_flag = False
        self.rows_count = rows_count
        self.columns_count = columns_count
        self.previous_state: list = None
        self.current_state: list
        self.__generate_current_state()


    def run(self) -> None:
        try:
            while not self.game_over_flag:
                self.__visualize()
                self.__update_states()
                time.sleep(0.1)
            self.__visualize_finish()
        except KeyboardInterrupt:
            print('UNEXPECTED STOP!')


    ## Private
    def __generate_current_state(self) -> None:
        self.current_state = [[1 if randint(0,1) == 0 else 0 for j in range(self.columns_count)] for i in range(self.rows_count)]


    def __visualize(self) -> None:
        import os
        os.system('clear')
        for r in range(len(self.current_state)):
            for c in range(len(self.current_state[r])):
                symbol = 'X' if self.current_state[r][c] is 1 else ' '
                print(symbol, end = '')
            print()


    def __update_states(self) -> None:
        _next_state = self.__calculate_next_state()
        if _next_state == self.current_state or _next_state == self.previous_state:
            self.game_over_flag = True
        else:
            self.previous_state = copy.deepcopy(self.current_state)
            self.current_state = copy.deepcopy(_next_state)


    def __calculate_next_state(self) -> list:
        _next_state = [[0] * self.columns_count for _ in range(self.rows_count)]

        for r in range(self.rows_count):
            for c in range(self.columns_count):
                _alive_neighbors_count = self.__calculate_alive_neighbors_count(r, c)

                if ((
                    _alive_neighbors_count == 3 and
                    self.current_state[r][c] == 0
                )
                or
                (
                    (_alive_neighbors_count == 2 or _alive_neighbors_count == 3) and
                    self.current_state[r][c] == 1
                )):
                    _next_state[r][c] = 1

        return _next_state


    def __calculate_alive_neighbors_count(self, r: int, c: int) -> int:
        _neighbors_coordinates = [
            [r-1, c-1], [r-1, c], [r-1, c+1],
            [r, c-1], [r, c+1],
            [r+1, c-1], [r+1, c], [r+1, c+1]
        ]

        _existing_neighbors_coordinates = list(filter(self.__border_crossing_filter, _neighbors_coordinates))

        _alive_neighbors_count = 0
        for neighbor_cord in _existing_neighbors_coordinates:
            if self.current_state[neighbor_cord[0]][neighbor_cord[1]] == 1:
                _alive_neighbors_count += 1

        return _alive_neighbors_count


    def __border_crossing_filter(self, cell_coordinates: list) -> bool:
        if (cell_coordinates[0] == -1 or
            cell_coordinates[0] == self.rows_count or
            cell_coordinates[1] == -1 or
            cell_coordinates[1] == self.columns_count):
            return False
        return True


    def __visualize_finish(self) -> None:
        print('GAME OVER')


def main():
    gl = Life(20, 60)
    # gl = Life()
    gl.run()


if __name__ == '__main__':
    main()
