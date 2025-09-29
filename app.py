import streamlit as st
import joblib
from game_logic import play_round

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

st.title("Slot Machine")
state = load_state()
if 'last_spin' not in st.session_state:
    st.session_state.last_spin = ["❓", "❓", "❓"]
if 'message' not in st.session_state:
    st.session_state.message = "Place your bet to start!"

if state['coins'] <= 0 or state['game_over']:
    st.header("Game Over!")

    st.metric(label="Your Final Score", value=f"{state['coins']}")
    st.metric(label="You could have got", value=f"{state['high_score']}")

    if state['coins'] <= 0:
        st.error("You've run out of coins!")
    else:
        st.success("You stopped the game. Thanks for playing!")

    if st.button("Start a New Game"):
        new_state = get_initial_state()
        save_state(new_state)
        st.rerun()
else:
    st.header(f"Your Balance: {state['coins']}")
    bet = st.number_input("Place your bet:", min_value=1, max_value=state['coins'], step=1)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Spin!", use_container_width=True, type="primary"):
            new_coins, spin_result, message = play_round(bet, state['coins'])
            state['coins'] = new_coins
            state['high_score'] = max(state['high_score'], new_coins)
            save_state(state)
            st.session_state.last_spin = spin_result
            st.session_state.message = message
            st.rerun()
    with col2:
        if st.button("Stop Playing", use_container_width=True):
            state['game_over'] = True
            save_state(state)
            st.rerun()

if not state['game_over'] and state['coins'] > 0:
    st.divider()
    reel1, reel2, reel3 = st.columns(3)
    reel1.markdown(f"<h1 style='text-align: center;'>{st.session_state.last_spin[0]}</h1>", unsafe_allow_html=True)
    reel2.markdown(f"<h1 style='text-align: center;'>{st.session_state.last_spin[1]}</h1>", unsafe_allow_html=True)
    reel3.markdown(f"<h1 style='text-align: center;'>{st.session_state.last_spin[2]}</h1>", unsafe_allow_html=True)
    st.info(st.session_state.message)
