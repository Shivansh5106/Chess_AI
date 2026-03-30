import pygame as p
import ChessEngine
from aibot import get_best_move

# ================= CONFIG =================
BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 300
WIDTH = BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH
HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 60
IMAGES = {}

AI_ENABLED = True

def loadImages():
    pieces = ['wP','wR','wN','wB','wK','wQ','bP','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"),
            (SQ_SIZE, SQ_SIZE)
        )

def main():
    global AI_ENABLED

    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    loadImages()

    font = p.font.SysFont("Arial", 18)
    bigFont = p.font.SysFont("Arial", 36)

    state = "MENU"
    selected_time = 300
    selected_diff = "Medium"

    gs = None
    validMoves = []

    sqSelected = ()
    playerClicks = []
    moveMade = False
    animate = False 

    gameOver = False

    whiteTime = 300
    blackTime = 300

    running = True

    while running:
        dt = clock.tick(MAX_FPS) / 1000

        # ================= MENU =================
        if state == "MENU":
            screen.fill((20, 20, 20))

            title = bigFont.render("CHESS GAME", True, p.Color("white"))
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

            start_x_3_btns = WIDTH // 2 - 170

            # --- Time Buttons ---
            times = [60, 300, 600]
            labels = ["1 min", "5 min", "10 min"]
            for i, t in enumerate(times):
                rect = p.Rect(start_x_3_btns + i*120, 130, 100, 50)
                color = p.Color("gold") if selected_time == t else p.Color("gray")
                p.draw.rect(screen, color, rect, border_radius=8)
                txt = font.render(labels[i], True, p.Color("black"))
                screen.blit(txt, (rect.x + rect.width//2 - txt.get_width()//2, rect.y + 14))

                if p.mouse.get_pressed()[0] and rect.collidepoint(p.mouse.get_pos()):
                    selected_time = t

            # --- Difficulty Buttons ---
            diffs = ["Easy", "Medium", "Hard"]
            for i, d in enumerate(diffs):
                rect = p.Rect(start_x_3_btns + i*120, 220, 100, 50)
                color = p.Color("green") if selected_diff == d else p.Color("gray")
                p.draw.rect(screen, color, rect, border_radius=8)
                txt = font.render(d, True, p.Color("black"))
                screen.blit(txt, (rect.x + rect.width//2 - txt.get_width()//2, rect.y + 14))

                if p.mouse.get_pressed()[0] and rect.collidepoint(p.mouse.get_pos()):
                    selected_diff = d

            # --- Mode Selection Buttons ---
            pvp_btn = p.Rect(WIDTH//2 - 160, 330, 150, 60)
            pvai_btn = p.Rect(WIDTH//2 + 10, 330, 150, 60)

            p.draw.rect(screen, p.Color("#2962ff"), pvp_btn, border_radius=10) 
            txt_pvp = font.render("Player vs Player", True, p.Color("white"))
            screen.blit(txt_pvp, (pvp_btn.x + pvp_btn.width//2 - txt_pvp.get_width()//2, pvp_btn.y + 19))

            p.draw.rect(screen, p.Color("#d50000"), pvai_btn, border_radius=10) 
            txt_pvai = font.render("Player vs AI", True, p.Color("white"))
            screen.blit(txt_pvai, (pvai_btn.x + pvai_btn.width//2 - txt_pvai.get_width()//2, pvai_btn.y + 19))

            if p.mouse.get_pressed()[0]:
                loc = p.mouse.get_pos()
                if pvp_btn.collidepoint(loc) or pvai_btn.collidepoint(loc):
                    AI_ENABLED = pvai_btn.collidepoint(loc) 
                    
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMove()
                    whiteTime = selected_time
                    blackTime = selected_time
                    state = "GAME"
                    p.time.delay(200) 

            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False

        # ================= GAME =================
        elif state == "GAME":

            # 🔥 Timer and Time-out Logic
            if not gameOver:
                if gs.whiteToMove:
                    whiteTime -= dt
                    if whiteTime <= 0:
                        whiteTime = 0
                        gameOver = True
                else:
                    blackTime -= dt
                    if blackTime <= 0:
                        blackTime = 0
                        gameOver = True

            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False

                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z: 
                        gs.undoMove()
                        if AI_ENABLED:
                            gs.undoMove() 
                        
                        validMoves = gs.getValidMove()
                        sqSelected = ()
                        playerClicks = []
                        gameOver = False

                    elif e.key == p.K_r: 
                        state = "MENU"  
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        gameOver = False

                elif e.type == p.MOUSEBUTTONDOWN and not gameOver:
                    location = p.mouse.get_pos()

                    if location[0] <= BOARD_WIDTH:
                        col = location[0] // SQ_SIZE
                        row = location[1] // SQ_SIZE

                        if sqSelected == (row, col):
                            sqSelected = ()
                            playerClicks = []
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)

                        if len(playerClicks) == 2:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)

                            for validMove in validMoves:
                                if move == validMove:
                                    if validMove.isPawnPromotion:
                                        color = 'w' if gs.whiteToMove else 'b'
                                        choice = getPromotionChoice(screen, color)
                                        validMove.promotionChoice = choice
                                        
                                    gs.makeMove(validMove)
                                    moveMade = True
                                    animate = True
                                    sqSelected = ()
                                    playerClicks = []
                                    break

                            if not moveMade:
                                playerClicks = [sqSelected]

            # 🤖 AI LOGIC
            if AI_ENABLED and not gameOver and not moveMade:
                if not gs.whiteToMove:
                    
                    if selected_diff == "Easy":
                        p.display.flip()   
                        p.time.delay(1500) 

                    fen = gs.getFEN()
                    ai_move = get_best_move(fen, selected_diff)

                    if ai_move:
                        startCol = ord(ai_move[0]) - ord('a')
                        startRow = 8 - int(ai_move[1])
                        endCol = ord(ai_move[2]) - ord('a')
                        endRow = 8 - int(ai_move[3])
                        
                        promo_char = ai_move[4].upper() if len(ai_move) == 5 else 'Q'

                        for move in validMoves:
                            if (move.startRow == startRow and
                                move.startCol == startCol and
                                move.endRow == endRow and
                                move.endCol == endCol):
                                
                                if move.isPawnPromotion:
                                    move.promotionChoice = promo_char

                                gs.makeMove(move)
                                moveMade = True
                                animate = True 
                                break

            # 🔥 Handle post-move logic and triggers
            if moveMade:
                if animate:
                    animateMove(gs.moveLog[-1], screen, gs.board, clock)
                validMoves = gs.getValidMove()
                moveMade = False
                animate = False

                if gs.checkmate or gs.stalemate:
                    gameOver = True

            # ================= UI =================
            screen.fill(p.Color(18,18,18))

            drawBoard(screen)
            highlightSquares(screen, gs, validMoves, sqSelected) 
            drawPieces(screen, gs.board)

            p.draw.rect(screen, p.Color(24,24,24),
                        (BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, HEIGHT))

            titleFont = p.font.SysFont("Arial", 22, True)
            textFont = p.font.SysFont("Consolas", 18)

            def formatTime(t):
                return f"{int(max(0, t)//60):02}:{int(max(0, t)%60):02}"

            screen.blit(titleFont.render("Black", True, p.Color("white")),
                        (BOARD_WIDTH+20, 20))
            screen.blit(textFont.render(formatTime(blackTime), True, p.Color("gold")),
                        (BOARD_WIDTH+150, 20))

            screen.blit(titleFont.render("White", True, p.Color("white")),
                        (BOARD_WIDTH+20, HEIGHT-50))
            screen.blit(textFont.render(formatTime(whiteTime), True, p.Color("gold")),
                        (BOARD_WIDTH+150, HEIGHT-50))

            screen.blit(titleFont.render("Moves", True, p.Color("white")),
                        (BOARD_WIDTH+20, 80))

            y = 110
            for i in range(0, len(gs.moveLog), 2):
                text = f"{i//2+1}. {gs.moveLog[i].getChessNotation()}"
                if i+1 < len(gs.moveLog):
                    text += f" {gs.moveLog[i+1].getChessNotation()}"

                screen.blit(textFont.render(text, True, p.Color("lightgray")),
                            (BOARD_WIDTH+20, y))
                y += 20

            # 🔥 Game Over Overlays
            if gameOver:
                if gs.checkmate:
                    text = "Checkmate! Black wins!" if gs.whiteToMove else "Checkmate! White wins!"
                elif gs.stalemate:
                    text = "Stalemate!"
                elif whiteTime <= 0:
                    text = "Time's up! Black wins!"
                elif blackTime <= 0:
                    text = "Time's up! White wins!"
                    
                overlay = p.Surface((BOARD_WIDTH, BOARD_HEIGHT))
                overlay.set_alpha(150)
                overlay.fill(p.Color("black"))
                screen.blit(overlay, (0, 0))
                
                endText = bigFont.render(text, True, p.Color("White"))
                textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(
                    BOARD_WIDTH / 2 - endText.get_width() / 2, 
                    BOARD_HEIGHT / 2 - endText.get_height() / 2
                )
                screen.blit(endText, textLocation)
                
            elif gs.inCheck():
                checkText = bigFont.render("CHECK!", True, p.Color("red"))
                textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(
                    BOARD_WIDTH / 2 - checkText.get_width() / 2, 
                    20 
                )
                
                bg_rect = p.Surface((checkText.get_width() + 20, checkText.get_height() + 10))
                bg_rect.set_alpha(150)
                bg_rect.fill(p.Color("black"))
                screen.blit(bg_rect, (textLocation.x - 10, textLocation.y - 5))
                screen.blit(checkText, textLocation)

        p.display.flip()

# --- HELPER FUNCTIONS ---

def getPromotionChoice(screen, color):
    pieces = ['Q', 'R', 'B', 'N']
    box_width = 4 * SQ_SIZE
    box_height = SQ_SIZE
    box_x = BOARD_WIDTH // 2 - box_width // 2
    box_y = BOARD_HEIGHT // 2 - box_height // 2

    overlay = p.Surface((BOARD_WIDTH, BOARD_HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(p.Color("black"))
    screen.blit(overlay, (0, 0))

    p.draw.rect(screen, p.Color("white"), p.Rect(box_x, box_y, box_width, box_height))
    p.draw.rect(screen, p.Color("black"), p.Rect(box_x, box_y, box_width, box_height), 2)

    for i, piece in enumerate(pieces):
        img = IMAGES[color + piece]
        p.draw.rect(screen, p.Color("black"), p.Rect(box_x + i * SQ_SIZE, box_y, SQ_SIZE, SQ_SIZE), 1)
        screen.blit(img, p.Rect(box_x + i * SQ_SIZE, box_y, SQ_SIZE, SQ_SIZE))

    p.display.flip()

    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.event.post(p.event.Event(p.QUIT))
                return 'Q'
            if e.type == p.MOUSEBUTTONDOWN:
                loc = p.mouse.get_pos()
                if box_y <= loc[1] <= box_y + box_height and box_x <= loc[0] <= box_x + box_width:
                    index = (loc[0] - box_x) // SQ_SIZE
                    return pieces[index]

def highlightSquares(screen, gs, validMoves, sqSelected):
    if len(gs.moveLog) > 0:
        lastMove = gs.moveLog[-1]
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('yellow'))
        screen.blit(s, (lastMove.endCol*SQ_SIZE, lastMove.endRow*SQ_SIZE))

    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): 
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) 
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    if gs.board[move.endRow][move.endCol] != "--":
                        s.fill(p.Color('red'))  
                    else:
                        s.fill(p.Color('purple')) 
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

def animateMove(move, screen, board, clock):
    colors = [p.Color(235,235,208), p.Color(181,136,99)]#light color & dark color
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    
    framesPerSquare = 15 
    frameCount = max(abs(dR), abs(dC)) * framesPerSquare 
    
    if frameCount == 0: 
        return
        
    is_castle = getattr(move, 'isCastleMove', False)
    if is_castle:
        if move.endCol - move.startCol == 2: 
            rookStartCol = move.startCol + 3
            rookEndCol = move.startCol + 1
        else: 
            rookStartCol = move.startCol - 4
            rookEndCol = move.startCol - 1
        rookRow = move.endRow
        rookPiece = board[rookRow][rookEndCol]
        
    for frame in range(frameCount + 1):
        r = move.startRow + dR * frame / frameCount
        c = move.startCol + dC * frame / frameCount
        
        for row in range(8):
            for col in range(8):
                color = colors[(row+col)%2]
                p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != "--":
                    if row == move.endRow and col == move.endCol:
                        continue
                    if is_castle and row == rookRow and col == rookEndCol:
                        continue
                    screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    
        if move.pieceCaptured != "--":
            if getattr(move, 'isEnpassantMove', False):
                enPassantRow = move.startRow 
                p.draw.rect(screen, p.Color(255, 50, 50), p.Rect(move.endCol*SQ_SIZE, enPassantRow*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                screen.blit(IMAGES[move.pieceCaptured], p.Rect(move.endCol*SQ_SIZE, enPassantRow*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            else:
                p.draw.rect(screen, p.Color(255, 50, 50), p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                screen.blit(IMAGES[move.pieceCaptured], p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        
        if is_castle:
            rook_dC = rookEndCol - rookStartCol
            rook_c = rookStartCol + rook_dC * frame / frameCount
            screen.blit(IMAGES[rookPiece], p.Rect(rook_c*SQ_SIZE, rookRow*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        
        p.display.update(p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT))
        clock.tick(60)

def drawBoard(screen):
    colors = [p.Color(235,235,208), p.Color(181,136,99)]#light color & dark color
    for r in range(8):
        for c in range(8):
            p.draw.rect(screen, colors[(r+c)%2], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(8):
        for c in range(8):
            if board[r][c] != "--":
                screen.blit(IMAGES[board[r][c]], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()