import turtle
import copy


screen = turtle.Screen()
screen.title("Wooden Chess ♟️")
screen.bgcolor("#CFB595")
screen.tracer(0)

S = 75
LIGHT = "#f0d9b5"
DARK = "#b58863"
start_x, start_y = -300, 300

board_t = turtle.Turtle(visible=False)
piece_t = turtle.Turtle(visible=False)
highlighter = turtle.Turtle(visible=False)
status = turtle.Turtle(visible=False)
capture_t = turtle.Turtle(visible=False)

for t in [piece_t, highlighter, status, capture_t]:
    t.penup()

symbols = {"P":"♟","R":"♜","N":"♞","B":"♝","Q":"♛","K":"♚"}


board_state = {}
turn = "white"
selected = None
captured_white = []
captured_black = []


def init_board():
    pieces = ["R","N","B","Q","K","B","N","R"]
    for i in range(8):
        board_state[(0,i)] = ("black",pieces[i])
        board_state[(1,i)] = ("black","P")
        board_state[(6,i)] = ("white","P")
        board_state[(7,i)] = ("white",pieces[i])


def draw_square(x,y,color):
    board_t.goto(x,y)
    board_t.pendown()
    board_t.fillcolor(color)
    board_t.begin_fill()
    for _ in range(4):
        board_t.forward(S); board_t.right(90)
    board_t.end_fill()
    board_t.penup()

def draw_board():
    board_t.clear()
    for r in range(8):
        for c in range(8):
            x = start_x + c*S
            y = start_y - r*S
            color = LIGHT if (r+c)%2==0 else DARK
            draw_square(x,y,color)

def draw_pieces():
    piece_t.clear()
    for (r,c),(clr,p) in board_state.items():
        x = start_x + c*S + S/2
        y = start_y - r*S - S/2 - 12
        piece_t.goto(x,y)
        piece_t.color("white" if clr=="white" else "black")
        piece_t.write(symbols[p], align="center",
                      font=("Times New Roman",30,"bold"))

def draw_captured():
    capture_t.clear()
    x,y = start_x, start_y+40
    for clr,p in captured_white:
        capture_t.goto(x,y); capture_t.color("white")
        capture_t.write(symbols[p], font=("Times New Roman",18,"bold")); x+=30
    x,y = start_x, start_y-8*S-40
    for clr,p in captured_black:
        capture_t.goto(x,y); capture_t.color("black")
        capture_t.write(symbols[p], font=("Times New Roman",18,"bold")); x+=30

def redraw():
    draw_board()
    draw_pieces()
    draw_captured()
    screen.update()


def show_status(msg):
    status.clear()
    status.goto(0,360)
    status.color("black")
    status.write(msg, align="center",
                 font=("Times New Roman",28,"bold"))


def get_square(x, y):
    col = int((x - start_x) // S)
    row = int((start_y - y) // S)
    if 0 <= row < 8 and 0 <= col < 8:
        return (row, col)

def find_king(color, state):
    for pos,(clr,p) in state.items():
        if clr==color and p=="K":
            return pos


def raw_moves(pos, state):
    r,c = pos
    color,piece = state[pos]
    moves=[]
    def empty(x): return x not in state
    def enemy(x): return x in state and state[x][0]!=color

    if piece=="P":
        d=-1 if color=="white" else 1
        if empty((r+d,c)):
            moves.append((r+d,c))
            if (color=="white" and r==6) or (color=="black" and r==1):
                if empty((r+2*d,c)):
                    moves.append((r+2*d,c))
        for dc in [-1,1]:
            if enemy((r+d,c+dc)):
                moves.append((r+d,c+dc))

    if piece in ["R","Q"]:
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            while 0<=nr<8 and 0<=nc<8:
                if (nr,nc) in state:
                    if enemy((nr,nc)): moves.append((nr,nc))
                    break
                moves.append((nr,nc))
                nr+=dr; nc+=dc

    if piece in ["B","Q"]:
        for dr,dc in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            nr,nc=r+dr,c+dc
            while 0<=nr<8 and 0<=nc<8:
                if (nr,nc) in state:
                    if enemy((nr,nc)): moves.append((nr,nc))
                    break
                moves.append((nr,nc))
                nr+=dr; nc+=dc

    if piece=="N":
        for dr,dc in [(2,1),(1,2),(-1,2),(-2,1),(2,-1),(1,-2),(-1,-2),(-2,-1)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<8 and 0<=nc<8:
                if empty((nr,nc)) or enemy((nr,nc)):
                    moves.append((nr,nc))

    if piece=="K":
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr or dc:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<8 and 0<=nc<8:
                        if empty((nr,nc)) or enemy((nr,nc)):
                            moves.append((nr,nc))
    return moves

def in_check(color, state):
    king = find_king(color, state)
    enemy = "black" if color=="white" else "white"
    for pos,(clr,p) in state.items():
        if clr==enemy and king in raw_moves(pos,state):
            return True
    return False

def safe_moves(pos):
    moves=[]
    for m in raw_moves(pos, board_state):
        temp=copy.deepcopy(board_state)
        temp[m]=temp[pos]; del temp[pos]
        if not in_check(board_state[pos][0], temp):
            moves.append(m)
    return moves

def checkmate(color):
    if not in_check(color, board_state): return False
    for pos,(clr,p) in board_state.items():
        if clr==color and safe_moves(pos):
            return False
    return True


def promote_pawn(pos):
    color,_ = board_state[pos]
    choice = screen.textinput("Promotion","Promote to (Q, R, B, N):")
    if choice:
        choice = choice.upper()
        if choice in ["Q","R","B","N"]:
            board_state[pos] = (color,choice)


def click(x,y):
    global selected, turn
    pos=get_square(x,y)
    if not pos: return

    if selected is None:
        if pos in board_state and board_state[pos][0]==turn:
            selected=pos
            highlighter.clear()
            for r,c in safe_moves(pos):
                hx=start_x+c*S+S/2
                hy=start_y-r*S-S/2
                highlighter.goto(hx,hy)
                highlighter.dot(15,"green")
    else:
        if pos in safe_moves(selected):
            piece = board_state[selected]
            if pos in board_state:
                if board_state[pos][0]=="white":
                    captured_white.append(board_state[pos])
                else:
                    captured_black.append(board_state[pos])

            board_state[pos]=piece
            del board_state[selected]

            r,_ = pos
            if piece[1]=="P" and (r==0 or r==7):
                promote_pawn(pos)

            enemy="black" if turn=="white" else "white"

            if checkmate(enemy):
                show_status(f"CHECKMATE! {turn.upper()} WON")
            elif in_check(enemy, board_state):
                show_status(f"{enemy.upper()} IN CHECK")
            else:
                show_status(f"{enemy.capitalize()} Move")

            turn=enemy

        selected=None
        highlighter.clear()
        redraw()


init_board()
redraw()
show_status("White Move")
screen.onclick(click)
screen.mainloop()
