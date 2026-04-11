import random


def draw_board(board, size):
    cell_width = len(str(size * size))
    border = "-" * (size * cell_width + size * 3 + 1)
    print(border)
    for i in range(size):
        row = board[i * size:(i + 1) * size]
        formatted_row = [f"{cell:>{cell_width}}" for cell in row]
        print(f"| {' | '.join(formatted_row)} |")
        print(border)


def take_input(board, player_token, size):
    while True:
        try:
            move = int(input(f"Куда поставим {player_token}? ")) - 1
            if 0 <= move < size * size and board[move] not in "XO":
                board[move] = player_token
                return
            print("Некорректный ход. Попробуйте снова.")
        except ValueError:
            print("Некорректный ввод. Введите число еще раз.")


def ai_move(board, size):
    available_moves = [i for i in range(size * size) if board[i] not in "XO"]
    if available_moves:
        move = random.choice(available_moves)
        board[move] = "O"


def check_win(board, size, win_length):
    def check_line(line):
        count = 1
        for i in range(len(line) - 1):
            if line[i] == line[i + 1] and line[i] in "XO":
                count += 1
                if count == win_length:
                    return line[i]
            else:
                count = 1
        return None

    for i in range(size):
        row_winner = check_line(board[i * size:(i + 1) * size])
        col_winner = check_line([board[j * size + i] for j in range(size)])
        if row_winner:
            return row_winner
        if col_winner:
            return col_winner

    # Проверяем все диагонали (включая смещенные), у которых длина не меньше win_length.
    for start_col in range(size):
        row = 0
        col = start_col
        main_diag = []
        while row < size and col < size:
            main_diag.append(board[row * size + col])
            row += 1
            col += 1
        if len(main_diag) >= win_length:
            winner = check_line(main_diag)
            if winner:
                return winner

    for start_row in range(1, size):
        row = start_row
        col = 0
        main_diag = []
        while row < size and col < size:
            main_diag.append(board[row * size + col])
            row += 1
            col += 1
        if len(main_diag) >= win_length:
            winner = check_line(main_diag)
            if winner:
                return winner

    for start_col in range(size):
        row = 0
        col = start_col
        anti_diag = []
        while row < size and col >= 0:
            anti_diag.append(board[row * size + col])
            row += 1
            col -= 1
        if len(anti_diag) >= win_length:
            winner = check_line(anti_diag)
            if winner:
                return winner

    for start_row in range(1, size):
        row = start_row
        col = size - 1
        anti_diag = []
        while row < size and col >= 0:
            anti_diag.append(board[row * size + col])
            row += 1
            col -= 1
        if len(anti_diag) >= win_length:
            winner = check_line(anti_diag)
            if winner:
                return winner

    return None


def play_game(size, win_length, is_pvp):
    board = [str(i + 1) for i in range(size * size)]
    counter = 0

    while True:
        draw_board(board, size)

        if counter % 2 == 0:
            take_input(board, "X", size)
        else:
            if is_pvp:
                take_input(board, "O", size)
            else:
                ai_move(board, size)

        counter += 1
        winner = check_win(board, size, win_length)

        if winner:
            draw_board(board, size)
            print(f"{winner} выиграл!")
            return

        if counter == size * size:
            draw_board(board, size)
            print("Ничья!")
            return


def main():
    print("#" * 5, " Крестики-нолики ", "#" * 5)
    mode = input("Выберите режим (1 - 5x5 PvP, 2 - 3x3 PvE): ")

    if mode == "1":
        play_game(size=5, win_length=4, is_pvp=True)
    else:
        play_game(size=3, win_length=3, is_pvp=False)


if __name__ == "__main__":
    main()
