import random

class Connect4:
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.board = [[' ' for _ in range(columns)] for _ in range(rows)]  # Játéktábla inicializálása
        self.current_player = 'Y'  # Jelenlegi játékos (Y: Sárga - Ember)
        self.players = {'Y': 'Játékos 1', 'R': 'AI (Piros)'}  # Játékosok nevei
        self.game_over = False  # Játék vége állapot

    def print_board(self):
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')  # Tábla kiírása
        print('  ' + '   '.join([str(i) for i in range(self.columns)]))  # Osztályok számozása (0-6)

    def is_valid_location(self, col):
        return self.board[self.rows - 1][col] == ' '  # Ellenőrzi, hogy az oszlop érvényes-e

    def get_next_open_row(self, col):
        for r in range(self.rows):
            if self.board[r][col] == ' ':
                return r  # Visszaadja a következő üres sort az oszlopban

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece  # Korong elhelyezése a táblán

    def winning_move(self, piece):
        # Ellenőrzi a nyerő kombinációkat vízszintesen
        for c in range(self.columns - 3):
            for r in range(self.rows):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and \
                   self.board[r][c + 2] == piece and self.board[r][c + 3] == piece:
                    return True

        # Ellenőrzi a nyerő kombinációkat függőlegesen
        for c in range(self.columns):
            for r in range(self.rows - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and \
                   self.board[r + 2][c] == piece and self.board[r + 3][c] == piece:
                    return True

        # Ellenőrzi a nyerő kombinációkat átlósan felfelé
        for c in range(self.columns - 3):
            for r in range(self.rows - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and \
                   self.board[r + 2][c + 2] == piece and self.board[r + 3][c + 3] == piece:
                    return True

        # Ellenőrzi a nyerő kombinációkat átlósan lefelé
        for c in range(self.columns - 3):
            for r in range(3, self.rows):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and \
                   self.board[r - 2][c + 2] == piece and self.board[r - 3][c + 3] == piece:
                    return True

    def save_game(self):
        with open("game_state.txt", "w") as f:
            for row in self.board:
                f.write(''.join(row) + '\n')  # Tábla állapotának mentése
            f.write(self.current_player + '\n')  # Játékos mentése

    def load_game(self):
        try:
            with open("game_state.txt", "r") as f:
                self.board = [list(line.strip()) for line in f.readlines()[:-1]]  # Tábla betöltése
                self.current_player = f.readlines()[-1].strip()  # Játékos betöltése
        except FileNotFoundError:
            print("Nincs mentett játék.")

    def play_game(self):
        self.load_game()  # Játékállás betöltése, ha elérhető
        while not self.game_over:
            self.print_board()  # Tábla kiírása
            if self.current_player == 'Y':
                col = self.get_valid_column()  # Játékos választ egy oszlopot
                row = self.get_next_open_row(col)  # Keresd meg a következő üres sort
                self.drop_piece(row, col, self.current_player)  # Korong elhelyezése
                if self.winning_move(self.current_player):  # Ellenőrzi, hogy nyert-e
                    self.print_board()
                    print(f"{self.players[self.current_player]} nyert!")
                    self.game_over = True
            else:
                col = random.randint(0, self.columns - 1)  # AI véletlenszerű oszlopválasztása
                if self.is_valid_location(col):
                    row = self.get_next_open_row(col)
                    self.drop_piece(row, col, self.current_player)
                    if self.winning_move(self.current_player):
                        self.print_board()
                        print(f"{self.players[self.current_player]} nyert!")
                        self.game_over = True

            # Játékosok váltása
            self.current_player = 'R' if self.current_player == 'Y' else 'Y'

        if input("Szeretnéd elmenteni a játékot? (i/n): ").lower() == 'i':
            self.save_game()  # Játék mentése
            print("Játék elmentve.")

    def get_valid_column(self):
        while True:
            try:
                col = int(input(f"{self.players[self.current_player]}, válassz egy oszlopot (0-{self.columns - 1}): "))
                if col >= 0 and col < self.columns and self.is_valid_location(col):
                    return col  # Visszaadja az érvényes oszlopot
                else:
                    print("Érvénytelen oszlop. Próbáld újra.")
            except ValueError:
                print("Érvénytelen bemenet. Kérlek, adj meg egy számot.")

if __name__ == "__main__":
    game = Connect4()
    game.play_game()
