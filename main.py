import pyglet, classes

game = classes.Game()
print(f'{game}\n')

win = pyglet.window.Window(960, 540)
ARROW_KEYS = {pyglet.window.key.LEFT: game.left,
              pyglet.window.key.RIGHT: game.right,
              pyglet.window.key.UP: game.up,
              pyglet.window.key.DOWN: game.down}


@win.event()
def on_key_press(symbol, modifiers):
    """gives keyboard control of the game"""
    global game
    if symbol in ARROW_KEYS.keys():
        game.record()
        ARROW_KEYS[symbol]()
        # adding another tile after moving (if valid)
        if game.check_prev_valid():
            game.add_tile()
    elif symbol == pyglet.window.key.SPACE:
        game.back()
    print(f'{game}\n')

@win.event()
def on_draw():
    win.clear()


pyglet.app.run()
