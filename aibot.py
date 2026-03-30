import chess
import chess.engine
import random  # 🔥 NEW: Import random to simulate beginner mistakes
import atexit

engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish")
atexit.register(engine.quit)

def get_best_move(fen, difficulty="Medium"):
    board = chess.Board(fen)
    
    if difficulty == "Easy":
        # 🔥 THE FIX: 50% chance to make a completely random, terrible move
        if random.random() < 0.5: 
            legal_moves = list(board.legal_moves)
            return random.choice(legal_moves).uci()
            
        # The other 50% of the time, it makes a weak Stockfish move
        engine.configure({"Skill Level": 0})
        limit = chess.engine.Limit(time=0.1, depth=1) 
        
    elif difficulty == "Medium":
        engine.configure({"Skill Level": 5})
        limit = chess.engine.Limit(time=0.2, depth=5) 
        
    else: # Hard
        engine.configure({"Skill Level": 20}) 
        limit = chess.engine.Limit(time=0.5, depth=15) 

    result = engine.play(board, limit)
    return result.move.uci()