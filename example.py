from move_n_shoot import Game
from move_n_shoot import get_human_player_action
from move_n_shoot import create_not_so_simple_ai_action_generator

# Constants
teal_color = [0, 188, 212]
yellowish_color = [255, 235, 59]
max_score = 100

# Initializations
myGame = Game()
myGame.add_player([100, 100], teal_color)
myGame.add_player([myGame.screen_width, myGame.screen_height], yellowish_color)

# Create the random action generator functions
get_not_so_simple_ai_action = create_not_so_simple_ai_action_generator()

# Run the game until any of the players achieve the max_score
while (myGame.players[0].score < max_score) and (myGame.players[1].score < max_score):

    myGame.handle_events()

    a1 = get_human_player_action(myGame)
    a2 = get_not_so_simple_ai_action(1, myGame)

    myGame.update_physics([a1, a2])
    myGame.draw_frame()

# Print results
print('Final score')
print('Player 1:', myGame.players[0].score)
print('Player 2:', myGame.players[1].score)


