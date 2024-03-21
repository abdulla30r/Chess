"""
This class is responsible for storing all the information about current state of the chess game. It will also be
responsible for determining valid moves at the current state. It will also keep a move log.
"""


class GameState():
    def __init__(self):
        # board is an 8*8 2d list . each element has 2 character.
        # first character means color. 2nd character piece name.
        # for example: bQ = black Queen
        # "--" represents empty space with no piece

        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--", ],
            ["--", "--", "--", "--", "--", "--", "--", "--", ],
            ["--", "--", "--", "--", "--", "--", "--", "--", ],
            ["--", "--", "--", "--", "--", "--", "--", "--", ],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.moveFunction = {'p': self.getPawnMoves, 'R': self.getRookeMoves, 'N': self.getKnightMoves,
                             'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves, }

        self.whiteToMove = True
        self.moveLog = []

    '''
    move a piece using move parameter. this will not work for pawn promotion, castling, en-passant
    '''

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"  # make blank in source
        self.board[move.endRow][move.endCol] = move.pieceMoved  # put piece in destination
        self.moveLog.append(move)  # log the move, so we can see history or undo move
        self.whiteToMove = not self.whiteToMove  # swap players

    '''
      undo the last move
    '''

    def undoMove(self):
        if len(self.moveLog) > 0:  # make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # swap players

    def getValidMoves(self):
        return self.getAllPossibleMoves()  # for now, we will not worry about checks

    '''
    All moves without considering check
    '''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of cols
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunction[piece](r, c, moves)   # calls the appropriate move function based on piece
        return moves

    '''
    Get all the pawn moves at row,col and add these moves to the list
    '''

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn moves

            # 1 square pawn advance
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))

                # 2 square pawn advance
                if (self.board[r - 2][c] == "--") and (r == 6):
                    moves.append(Move((r, c), (r - 2, c), self.board))

            # capture left corner
            if (c > 0) and (self.board[r - 1][c - 1][0] == "b"):
                moves.append(Move((r, c), (r - 1, c - 1), self.board))

            # capture right corner
            if (c < 7) and (self.board[r - 1][c + 1][0] == "b"):
                moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # black pawn moves
            # 1 square pawn advance
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))

                # 2 square pawn advance
                if (self.board[r + 2][c] == "--") and (r == 1):
                    moves.append(Move((r, c), (r + 2, c), self.board))

            # capture left corner
            if (c > 0) and (self.board[r + 1][c - 1][0] == "w"):
                moves.append(Move((r, c), (r + 1, c - 1), self.board))

            # capture right corner
            if (c < 7) and (self.board[r + 1][c + 1][0] == "w"):
                moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookeMoves(self, r, c, moves):
        pass

    def getBishopMoves(self, r, c, moves):
        pass

    def getKnightMoves(self, r, c, moves):
        pass

    def getKingMoves(self, r, c, moves):
        pass

    def getQueenMoves(self, r, c, moves):
        pass


class Move():
    # maps keys to value
    # key : value
    # normally chess e vertical e 0-7 numbering kora. starting from white.
    # horizontal e a-h. called files. our board orders are not same. hence, mapping.
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}  # mapping dictionary
    rowsToRanks = {v: k for k, v in ranksToRows.items()}  # reverse a dictionary

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}  # mapping dictionary
    colsToFiles = {v: k for k, v in filesToCols.items()}  # reverse a dictionary

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    '''
    Overriding the equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    # source Destination of current move. example : d2d4
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
