import streamlit as streamlit

streamlit.title('Hello World!')

# Text Input
name = streamlit.text_input('Enter your name')
streamlit.write('Hello', name)

# Number Input
option = streamlit.selectbox('Which Number do you like best?', [1, 2, 3, 4, 5])
streamlit.write('Your selected number is:', option)

# Radio Button
option = streamlit.radio('Which Number do you like best?', [1, 2, 3, 4, 5])
streamlit.write('Your selected number is:', option)

# Checkbox
if streamlit.checkbox('Show/Hide'):
    streamlit.write('This is a secret message.')

# Slider
age = streamlit.slider('How old are you?', 0, 130, 25)
streamlit.write('I am', age, 'years old.')

# Button
if streamlit.button('Say Hello'):
    streamlit.write('Hello')

# Text Area
message  = streamlit.text_area('Enter your message')
streamlit.write('You entered: ',message)

# Calender
import datetime
today = streamlit.date_input('Today is', datetime.datetime.now())
streamlit.write('Today is: ', today)

# Time
time  = streamlit.time_input('Current Time', datetime.datetime.now())
streamlit.write('Current Time is: ', time)

# File Upload
import pandas as pd
Upload = streamlit.file_uploader('Choose a file', type=['csv'])
if  Upload is not None:
    Data = pd.read_csv(Upload)
    streamlit.write(Data)

# Progress Bar
import time
my_bar = streamlit.progress(0)
for per in range(100):
    time.sleep(0.01)
    my_bar.progress(per + 1)

# Sidebar
streamlit.sidebar.write('This is a Sidebar')
streamlit.sidebar.button('Press Me')

# Expander
with streamlit.expander('See more'):
    streamlit.write('This is hidden by default')

# Columns

col1, col2, col3 = streamlit.columns(3)
col1.header('Column 1')
col1.write('This is column 1')
col2.header('Column 2')
col2.write('This is column 2')
col3.header('Column 3')
col3.write('This is column 3')

# Plot
import plotly.express as px
import numpy as np

x = np.random.randn(100)
fig = px.histogram(x, nbins=20)
streamlit.plotly_chart(fig)

# Image
from PIL import Image

Image_St = streamlit.file_uploader('Choose a file', type=['jpg'])
if  Image_St is not None:
    image = Image.open(Image_St)
    streamlit.image(image, use_column_width=True, caption='Image on Streamlit')

#Video
URL = streamlit.text_input('Paste URL')
if URL is not None:
    streamlit.video(URL)

# import streamlit as st
# import streamlit.components.v1 as components
# import numpy as np
# import random

# class TicTacToe:
#     def __init__(self):
#         self.board = [' '] * 9
#         self.current_player = 'X'
#         self.winning_combo = [
#             (0, 1, 2), (3, 4, 5), (6, 7, 8),
#             (0, 3, 6), (1, 4, 7), (2, 5, 8),
#             (0, 4, 8), (2, 4, 6)
#         ]
    
#     def make_move(self, position):
#         if self.board[position] ==' ':
#             self.board[position] = self.current_player
#             self.current_player = 'O' if self.current_player == 'X' else 'X'
#             return True
#         return False
    
#     def check_winner(self):
#         for combo in self.winning_combo:
#             if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
#                 return self.board[combo[0]]
#         if ' ' not in self.board:
#             return 'Tie'
#         return None

#     def get_winning_combo(self):
#         for combo in self.winning_combo:
#             if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
#                 return combo
#         return None

#     def reset_board(self):
#         self.board = [' '] * 9

# game = TicTacToe()

# st.title('Tic Tac Toe')

# def display_board():
#     st.text('Player 1 (X) - You, Player 2 (O)')
#     st.text('Current Player:'+ game.current_player)


# display_board()

# # Create a TicTacToe instance
# game = TicTacToe()

# # Streamlit App
# st.title("Tic Tac Toe")

# # Initialize the session state for the game board and player
# if 'board' not in st.session_state:
#     st.session_state.board = [' '] * 9
#     st.session_state.current_player = 'X'
#     st.session_state.winner = None

# # Reset the game board
# def reset_game():
#     st.session_state.board = [' '] * 9
#     st.session_state.current_player = 'X'
#     st.session_state.winner = None
#     game.reset_board()

# # Display the Tic Tac Toe board
# def display_board():
#     board = np.array(st.session_state.board).reshape(3, 3)
#     for i in range(3):
#         cols = st.columns(3)
#         for j in range(3):
#             idx = i * 3 + j
#             if cols[j].button(board[i, j], key=idx):
#                 if st.session_state.winner is None and game.make_move(idx):
#                     st.session_state.board[idx] = st.session_state.current_player
#                     st.session_state.winner = game.check_winner()
#                     st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'
#                     if st.session_state.winner:
#                         time.sleep(0.5)
#                         if st.session_state.winner == 'Tie':
#                             st.success("It's a tie!")
#                         else:
#                             st.success(f"Player {st.session_state.winner} wins!")
#                         st.balloons()

# # Display the board
# display_board()

# # Reset button
# if st.button('Reset Game'):
#     reset_game()