import streamlit as st

#FIX: Refactored low and high values for difficulty level logic into get_range_for_difficulty in 
# logic_utils.py using Claude Code agent
#FIX: Implemented changes in range logic into new_secret in logic_utils.py using Claude Code agent
#FIX: Refactored check_guess into logic_utils.py and corrected the hint direction using Claude Code agent
#FIX: Refactored parse_guess into logic_utils.py and added difficulty-range validation using Claude Code agent
#FIX: Refactored update_score into logic_utils.py and fixed the win formula and the Too High guess adding
# points glitch using Claude Code agent
from logic_utils import (
    get_range_for_difficulty,
    new_secret,
    check_guess,
    parse_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

#FIX: Made attempts actually decrease as difficulty rises using Claude Code agent
attempt_limit_map = {
    "Easy": 8,
    "Normal": 6,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

#FIX: Showed changes in range logic into UI sidebar using Claude Code agent
st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

#FIX: Treat first load and any difficulty change as a fresh game. Besides a new
# secret for the new range, reset attempts/score/status/history too — otherwise a
# finished game's "won"/"lost" status carries over and the status check locks the
# player out, and the old score/history bleed into the new game (Claude Code agent).
# attempts starts at 0 so attempt_number is a consistent 1-based count.
if "secret" not in st.session_state or st.session_state.get("active_difficulty") != difficulty:
    st.session_state.secret = new_secret(difficulty)
    st.session_state.active_difficulty = difficulty
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []

st.subheader("Make a guess")

#FIX: Reserve these spots now but fill them at the end so they reflect the state
# *after* this turn's guess is processed, not the stale pre-guess value (Claude Code agent)
info_box = st.empty()
debug_box = st.empty()


def render_status():
    info_box.info(
        #FIX: Showed changes in range logic into UI sidebar using Claude Code agent
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {max(0, attempt_limit - st.session_state.attempts)}"
    )
    with debug_box.expander("Developer Debug Info"):
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Score:", st.session_state.score)
        st.write("Difficulty:", difficulty)
        st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    #FIX: Matched the range secret is in to match the difficulty in new games using Claude Code agent
    st.session_state.secret = new_secret(difficulty)
    st.session_state.active_difficulty = difficulty
    #FIX: Reset status/score/history so New Game is actually playable after a
    # win or loss (status stayed "won"/"lost" and st.stop() blocked play) using Claude Code agent
    st.session_state.status = "playing"
    st.session_state.score = 0
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    render_status()
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        # FIX: An invalid or out-of-range guess no longer burns an attempt so
        # the attempt counter only increases for a valid guess (used Claude Code agent)
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        #FIX: Claude Code pointed out that previous code stringified the secret
        # on even attempts for no reason, so now check_guess always compares the guess against the int secret
        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

#FIX: Render banner + debug after the guess is processed so they aren't a turn stale (Claude Code agent)
render_status()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
