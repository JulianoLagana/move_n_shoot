from move_n_shoot import Game
from move_n_shoot import create_human_player_binding, create_not_so_simple_ai_binding

# Constants
teal_color = [0, 188, 212]
yellowish_color = [255, 235, 59]
max_score = 100

# Initializations
myGame = Game()
myGame.add_player(create_human_player_binding(), [100, 100], teal_color)
myGame.add_player(create_not_so_simple_ai_binding(), [myGame.screen_width, myGame.screen_height],
                  yellowish_color)

# Run the game until any of the players achieve the max_score
while (myGame.players[0].score < max_score) and (myGame.players[1].score < max_score):
    myGame.handle_events()
    myGame.update_physics()
    myGame.draw_frame()

# Print results
print('Final score')
print('Player 1:', myGame.players[0].score)
print('Player 2:', myGame.players[1].score)


