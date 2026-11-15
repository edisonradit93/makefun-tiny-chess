import json
import os
import sys
import urllib.error
import urllib.request

ENV_URL = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")

VAL = {"p": 100, "n": 320, "b": 330, "r": 500, "q": 900, "k": 20000}
PST = {
    "p": [0,0,0,0,0,0,0,0, 5,10,10,-20,-20,10,10,5, 5,-5,-10,0,0,-10,-5,5, 0,0,0,20,20,0,0,0, 5,5,10,25,25,10,5,5, 10,10,20,30,30,20,10,10, 50,50,50,50,50,50,50,50, 0,0,0,0,0,0,0,0],
    "n": [-50,-40,-30,-30,-30,-30,-40,-50, -40,-20,0,5,5,0,-20,-40, -30,5,10,15,15,10,5,-30, -30,0,15,20,20,15,0,-30, -30,5,15,20,20,15,5,-30, -30,0,10,15,15,10,0,-30, -40,-20,0,0,0,0,-20,-40, -50,-40,-30,-30,-30,-30,-40,-50],
    "b": [-20,-10,-10,-10,-10,-10,-10,-20, -10,5,0,0,0,0,5,-10, -10,10,10,10,10,10,10,-10, -10,0,10,10,10,10,0,-10, -10,5,5,10,10,5,5,-10, -10,0,5,10,10,5,0,-10, -10,0,0,0,0,0,0,-10, -20,-10,-10,-10,-10,-10,-10,-20],
    "r": [0,0,0,5,5,0,0,0, -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5, -5,0,0,0,0,0,0,-5, 5,10,10,10,10,10,10,5, 0,0,0,0,0,0,0,0],
    "q": [-20,-10,-10,-5,-5,-10,-10,-20, -10,0,0,0,0,5,0,-10, -10,0,5,5,5,5,5,-10, -5,0,5,5,5,5,0,-5, 0,0,5,5,5,5,0,-5, -10,5,5,5,5,5,0,-10, -10,0,5,0,0,0,0,-10, -20,-10,-10,-5,-5,-10,-10,-20],
    "k": [20,30,10,0,0,10,30,20, 20,20,0,0,0,0,20,20, -10,-20,-20,-20,-20,-20,-20,-10, -20,-30,-30,-40,-40,-30,-30,-20, -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30]
}

def post(path, body):
    req = urllib.request.Request(
        ENV_URL + path,
        data=json.dumps(body).encode(),
        headers={"content-type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as res:
            return json.load(res)
    except urllib.error.HTTPError as e:
        sys.exit(f"{path}: HTTP {e.code} {e.read().decode(errors='replace')}")

def parse_board(fen):
    board = {}
    rows = fen.split()[0].split("/")
    for r, row in enumerate(rows):
        f = 0
        for c in row:
            if c.isdigit():
                f += int(c)
            else:
                sq = "abcdefgh"[f] + str(8 - r)
                board[sq] = c
                f += 1
    return board

def sq_idx(sq):
    return (int(sq[1]) - 1) * 8 + ("abcdefgh".index(sq[0]))

def eval_board(board, is_white):
    score = 0
    for sq, p in board.items():
        low = p.lower()
        v = VAL.get(low, 0)
        idx = sq_idx(sq)
        pst_val = PST.get(low, [0]*64)[idx if p.isupper() else (63 - idx)]
        tot = v + pst_val
        score += tot if p.isupper() else -tot
    return score if is_white else -score

def choose_move(fen, legal, is_white):
    board = parse_board(fen)
    best_score = -1e9
    best_move = legal[0]

    for m in legal:
        frm, to = m[:2], m[2:4]
        promo = m[4] if len(m) == 5 else None
        p = board.get(frm)
        if not p:
            continue
        
        # Apply move
        nb = dict(board)
        del nb[frm]
        nb[to] = promo.upper() if (promo and is_white) else (promo.lower() if promo else p)
        
        # Immediate static eval
        sc = eval_board(nb, is_white)
        
        # MVV-LVA bonus for captures and center advance
        captured = board.get(to)
        if captured:
            sc += VAL.get(captured.lower(), 0) * 12 - VAL.get(p.lower(), 0)
        if to in ("d4", "d5", "e4", "e5"):
            sc += 15
        
        if sc > best_score:
            best_score = sc
            best_move = m

    return best_move

while True:
    g = post("/game", {})
    if g.get("status") == "done":
        break
    while g.get("status") == "your_move":
        turn_white = g["fen"].split()[1] == "w"
        mv = choose_move(g["fen"], g["legal_moves"], turn_white)
        g = post("/move", {"game": g["game"], "move": mv})
    print(f"game {g.get('game')}: {g.get('outcome')} by {g.get('reason')}", file=sys.stderr)
print(f"done: {g.get('wins', 0)} won, {g.get('draws', 0)} drawn, {g.get('losses', 0)} lost", file=sys.stderr)
