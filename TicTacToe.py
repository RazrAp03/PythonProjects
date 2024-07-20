class TicTacToe:
    def __init__(self):             # Initialisation
        self.board=[[' ']*3 for i in range(3)]
        self.player='X'             # Player => 'X' by default
    def fill(self,i,j):
        if not (0<=i<=2 and 0<=j<=2):
            raise ValueError("INVALID BOARD POSITION")
        if self.board[i][j]!=' ':
            raise ValueError("BOARD POSITION ALREADY FILLED")
        if self.winner() is not None:
            raise ValueError("THE GAME IS ALREADY FINISHED")
        self.board[i][j]=self.player
        if self.player=='X':
            self.player='O'
        else:
            self.player='X'
    def for_win(self,fill):         # CHECK THE CONDITIONS REQUIRED TO WIN
        board=self.board
        return (fill==board[0][0]==board[0][1]==board[0][2]
                or fill==board[1][0]==board[1][1]==board[1][2]
                or fill==board[2][0]==board[2][1]==board[2][2]
                or fill==board[0][0]==board[1][0]==board[2][0]
                or fill==board[0][1]==board[1][1]==board[2][1]
                or fill==board[0][2]==board[1][2]==board[2][2]
                or fill==board[0][0]==board[1][1]==board[2][2]
                or fill==board[0][2]==board[1][1]==board[2][0])
    def winner(self):
        for fill in 'XO':
            if self.for_win(fill):
                return fill
        return None
    def __str__(self) -> str:
        rows=[' | '.join(self.board[k]) for k in range(3)]
        return '\n----------\n'.join(rows)
    
game=TicTacToe()
print(game)
for i in range(9):
    a=int(input("Enter row (0-2): "))
    b=int(input("Enter column (0-2): "))
    game.fill(a,b)
    print(game)
    winner=game.winner()
    if winner is not None:
        print("\n",winner, "WINS !!")
        break
if winner is None:
    print("\nIT's A DRAW !!")

