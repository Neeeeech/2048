import pyglet, classes
from math import log2

game = classes.Game()
print(f'{game}\n')

win = pyglet.window.Window(540, 540)
batch = pyglet.graphics.Batch()
ARROW_KEYS = {pyglet.window.key.LEFT: game.left,
              pyglet.window.key.RIGHT: game.right,
              pyglet.window.key.UP: game.up,
              pyglet.window.key.DOWN: game.down}
BACKGROUND = [pyglet.shapes.Rectangle(0, 0, 540, 540, color=(245, 245, 245), batch=batch)]
tiles = []
# setting up BACKGROUND, with 5 horizontal & vertical lines each
for i in [20, 145, 270, 395, 520]:
    BACKGROUND.append(pyglet.shapes.Line(i, 20, i, 520, width=2, color=(0, 0, 0), batch=batch))
    BACKGROUND.append(pyglet.shapes.Line(20, i, 520, i, width=2, color=(0, 0, 0), batch=batch))

def color_gen(num):
    seed = int(log2(num))
    return (seed * 20 + 10) % 128 + 128, (seed * 40 + 100) % 128 + 128, (seed * 50 + 196) % 128 + 128

def give_tiles():
    """gives list of tile Labels"""
    global game
    text, rectangles = [], []
    for i in range(4):
        for j in range(4):
            if game.current_state.board[i][j]:
                length = len(str(game.current_state.board[i][j]))
                rectangles.append(pyglet.shapes.Rectangle(30+125*j, 405-125*i, 105, 105,
                                                          color=color_gen(game.current_state.board[i][j]),
                                                          batch=batch))
                text.append(pyglet.text.Label(str(game.current_state.board[i][j]),
                                              font_name='Andale Mono',
                                              font_size=40 if length <= 3 else 30,
                                              x=80+125*j-(11 if length > 3 else 15)*length,
                                              y=440-125*i + (5 if length > 3 else 0),
                                              align='center',
                                              color=(0,0,0,255)))
    return text, rectangles

@win.event()
def on_key_press(symbol, modifiers):
    """gives keyboard control of the game"""
    global game, ARROW_KEYS
    if symbol in ARROW_KEYS.keys():
        ARROW_KEYS[symbol]()
    elif symbol == pyglet.window.key.SPACE:
        game.back()
    elif symbol == pyglet.window.key.R:
        game.reset()
    print(f'{game}\n')

@win.event()
def on_draw():
    win.clear()
    text, rectangles = give_tiles()
    batch.draw()
    list(map(pyglet.text.Label.draw, text))


pyglet.app.run()
