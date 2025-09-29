import streamlit as st
import random
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Slot Machine Game",
    page_icon="🎰",
    layout="centered"
)

# --- Game Assets and Variables ---
SYMBOLS = ["🍒", "🍋", "🔔", "💎", "7️⃣", "🍀"]

# --- Initialize Session State ---
# This is crucial for Streamlit apps to remember variables across reruns.
if 'coins' not in st.session_state:
    st.session_state.coins = 100
if 'last_spin' not in st.session_state:
    st.session_state.last_spin = ["❓", "❓", "❓"]
if 'message' not in st.session_state:
    st.session_state.message = "Place your bet and click 'Spin' to start!"

# --- Game Logic Function ---
def spin_reels():
    """Handles the logic of a single spin."""
    bet = st.session_state.bet_amount
    
    # Validate the bet
    if bet <= 0:
        st.session_state.message = "Bet must be greater than 0. 😕"
        return
    if bet > st.session_state.coins:
        st.session_state.message = "You don't have enough coins for that bet. 😢"
        return

    # Proceed with the spin
    st.session_state.coins -= bet
    spin = random.choices(SYMBOLS, k=3)
    st.session_state.last_spin = spin

    # Check for winnings
    if spin[0] == spin[1] == spin[2]:
        winnings = bet * 10
        st.session_state.coins += winnings
        st.session_state.message = f"🎉 JACKPOT! All three match! You won {winnings} coins! 🎉"
    elif spin[0] == spin[1] or spin[0] == spin[2] or spin[1] == spin[2]:
        winnings = bet * 2
        st.session_state.coins += winnings
        st.session_state.message = f"✨ Two symbols match! You won {winnings} coins! ✨"
    else:
        st.session_state.message = "🙁 No match. Better luck next time!"

# --- UI Layout ---
st.title("🎰 Welcome to the Slot Machine! 🎰")

# Display Rules in an expander
with st.expander("📖 Click to see the rules"):
    st.markdown("""
    - You start with **100 coins**.
    - Place a bet and spin the reels.
    - **Three matching symbols**: Win 10x your bet!
    - **Two matching symbols**: Win 2x your bet!
    - **No match**: You lose your bet.
    - The game ends when you run out of coins.
    """)

st.divider()

# --- Main Game Interface ---
if st.session_state.coins > 0:
    st.header(f"Your Balance: {st.session_state.coins} 🪙")
    
    # Bet input
    bet_amount = st.number_input(
        "Place your bet:",
        min_value=1,
        max_value=st.session_state.coins,
        step=1,
        key='bet_amount' # Use a key to access the value in session_state
    )

    # Spin button
    if st.button("Spin!", use_container_width=True):
        spin_reels()

    # Display the reels
    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{st.session_state.last_spin[0]}</h1>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{st.session_state.last_spin[1]}</h1>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{st.session_state.last_spin[2]}</h1>", unsafe_allow_html=True)
    
    # Display the result message
    st.info(st.session_state.message)

else:
    # Game Over screen
    st.error("💔 Game Over! You've run out of coins. 💔")
    st.balloons()
    if st.button("Start a New Game"):
        # Reset the game state
        st.session_state.coins = 100
        st.session_state.last_spin = ["❓", "❓", "❓"]
        st.session_state.message = "Place your bet and click 'Spin' to start!"
        st.rerun() # Rerun the script to reflect the new game state