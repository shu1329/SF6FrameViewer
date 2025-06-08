import flet as ft

class Character:
    def __init__(self, moves: list):
        self.moves = moves

    def advantage(self, is_rush: bool, is_bo: bool):
        nomal, spetial = [], []
        for x in self.moves:
            if x[2] is not None:
                if is_bo:
                    if x[2] + 4 >= 0:
                        if x[4]:
                            nomal.append(ft.Text(f'{x[0]} - 硬直差: {x[2]+4}'))
                        else:
                            spetial.append(ft.Text(f'{x[0]} - 硬直差: {x[2]+4}'))
                    if is_rush and x[4] and x[2] + 8 >= 0:
                        nomal.append(ft.Text(f'[ラッシュ]{x[0]} - 硬直差: {x[2]+8}'))
                else:
                    if x[2] >= 0:
                        if x[4]:
                            nomal.append(ft.Text(f'{x[0]} - 硬直差: {x[2]}'))
                        else:
                            spetial.append(ft.Text(f'{x[0]} - 硬直差: {x[2]}'))
                    if is_rush and x[4] and x[2] + 4 >= 0:
                        nomal.append(ft.Text(f'[ラッシュ]{x[0]} - 硬直差: {x[2]+4}'))
    
        return nomal, spetial

    def counterable(self, is_bo: bool, is_all: bool) -> list:
        counterable_move = []
        for x in self.moves:
            if x[2] is not None:
                if is_all:
                    if not is_bo:
                        counterable_move.append(x)
                    else:
                        counterable_move.append(x)
                else:
                    if not is_bo and x[2] <= -4:
                        counterable_move.append(x)
                    elif is_bo and x[2] <= -8:
                        counterable_move.append(x)
        
        self.counterable_move = counterable_move
        return counterable_move
    
    def search_counters(self, frame: int, n: int):
        if frame < 0:
            frame = -frame

        if n == 1:
            move = []
            for x in self.moves:
                if None not in (x[1], x[3]):
                    if x[1] - frame <= 0:
                        move.append(x)
            return move
        
        elif n == 2:
            nomal, spetial = [], []
            for x in self.moves:
                if None not in (x[1], x[3]):
                    if x[1] - frame <= 0:
                        if x[4]:
                            nomal.append(ft.Text(f'{x[0]}({x[1]}) - ダメージ: {x[3]}'))
                        else:
                            spetial.append(ft.Text(f'{x[0]}({x[1]}) - ダメージ: {x[3]}'))
                    if x[1] - frame + 11 <= 0:
                        if x[4]:
                            nomal.append(ft.Text(f'[ラッシュ]{x[0]}({x[1]+11}) - ダメージ: {x[3]}'))
                        else:
                            spetial.append(ft.Text(f'[ラッシュ]{x[0]}({x[1]+11}) - ダメージ: {x[3]}'))

            return nomal, spetial


class Process:
    def __init__(self, my: Character, op: Character):
        self.my = my
        self.op = op
    
    def show_counters(self, is_bo: bool, selected_index: int):
        op_move = self.op.counterable_move[selected_index]
        pc = self.my.search_counters(op_move[2], 1)
        nomal = []
        spetial = []

        pc.sort(key=lambda x: x[3], reverse=True)

        for counter in pc:
            if counter[4]:
                nomal.append(ft.Text(f'{counter[0]}({counter[1]}) - ダメージ: {counter[3]}'))
            else:
                spetial.append(ft.Text(f'{counter[0]}({counter[1]}) - ダメージ: {counter[3]}'))

            if not is_bo and op_move[2] + counter[1] + 11 <= 0:
                if counter[4]:
                    nomal.append(ft.Text(f'[ラッシュ]{counter[0]}({counter[1]+11}) - ダメージ: {counter[3]}'))
                else:
                    spetial.append(ft.Text(f'[ラッシュ]{counter[0]}({counter[1]+11}) - ダメージ: {counter[3]}'))

        return nomal, spetial