import streamlit as st
import joblib
import time
import random
from game_logic import play_round, SYMBOLS

STATE_FILE = 'game_state.joblib'

def get_initial_state():
    return {'coins': 100, 'high_score': 100, 'game_over': False}

def load_state():
    try:
        return joblib.load(STATE_FILE)
    except FileNotFoundError:
        return get_initial_state()

def save_state(state):
    joblib.dump(state, STATE_FILE)

# --- UI Layout ---
st.set_page_config(page_title="Slot Machine", page_icon="🎰")
st.title("🎰 Slot Machine 🎰")

# Load game state
state = load_state()

# --- Main Game Logic ---

if state.get('game_over', False) or state['coins'] <= 0:
    # --- Game Over Screen ---
    st.header("Game Over!")
    final_coins = 0 if state['coins'] < 0 else state['coins']
    st.metric(label="Your Final Score", value=f"{final_coins}")
    st.metric(label="Highest Score Achieved", value=f"{state['high_score']}")

    if state['coins'] <= 0:
        st.error("You've run out of coins!")
    else:
        st.success("You stopped the game. Thanks for playing!")

    if st.button("Start a New Game"):
        new_state = get_initial_state()
        save_state(new_state)
        st.rerun()
else:
    # --- Active Game Interface ---
    st.header(f"Your Balance: {state['coins']}")

    bet = st.number_input("Place your bet:", min_value=1, max_value=state['coins'], step=1)

    reel_placeholders = st.columns(3)
    message_placeholder = st.empty()

    last_spin = st.session_state.get('last_spin', ["❓", "❓", "❓"])
    last_message = st.session_state.get('last_message', "Place your bet and click 'Spin'!")

    for i, reel in enumerate(reel_placeholders):
        reel.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{last_spin[i]}</h1>", unsafe_allow_html=True)
    message_placeholder.info(last_message)

    spin_col, stop_col = st.columns(2)

    if spin_col.button("Spin!", use_container_width=True, type="primary"):
        # Step 1: Determine the final, random outcome *before* the animation
        new_coins, final_spin, message = play_round(bet, state['coins'])

        # Step 2: Create long, shuffled "reel strips" for the animation
        reel_strips = []
        for _ in range(3):
            strip = (SYMBOLS * 5)  # Create a long strip
            random.shuffle(strip)
            reel_strips.append(strip)

        # --- The New Animation Logic ---
        STOP_FRAME_1 = 15  # When the first reel stops
        STOP_FRAME_2 = 25  # When the second reel stops
        TOTAL_FRAMES = 30  # Total animation frames
        
        # Start spinning from a random position
        start_indices = [random.randint(0, len(s) - 1) for s in reel_strips]

        for i in range(1, TOTAL_FRAMES + 1):
            spin_display = ["", "", ""]
            
            # Reel 1
            if i < STOP_FRAME_1:
                idx = (start_indices[0] + i) % len(reel_strips[0])
                spin_display[0] = reel_strips[0][idx]
            else:
                spin_display[0] = final_spin[0]

            # Reel 2
            if i < STOP_FRAME_2:
                idx = (start_indices[1] + i) % len(reel_strips[1])
                spin_display[1] = reel_strips[1][idx]
            else:
                spin_display[1] = final_spin[1]
            
            # Reel 3
            if i < TOTAL_FRAMES:
                idx = (start_indices[2] + i) % len(reel_strips[2])
                spin_display[2] = reel_strips[2][idx]
            else:
                spin_display[2] = final_spin[2]

            # Update UI placeholders
            for j, reel in enumerate(reel_placeholders):
                reel.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{spin_display[j]}</h1>", unsafe_allow_html=True)
            
            time.sleep(0.05 + i * 0.002) # Sleep longer as it slows down

        # Finalize the game state
        st.session_state.last_message = message
        st.session_state.last_spin = final_spin
        
        state['coins'] = new_coins
        state['high_score'] = max(state['high_score'], new_coins)
        save_state(state)
        
        st.rerun()

    if stop_col.button("Stop Playing", use_container_width=True):
        state['game_over'] = True
        save_state(state)
        st.rerun()
