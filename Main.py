import streamlit as st

# handle the session states use to processes comes in the main process
def handle_session_states():
    if "state" not in st.session_state:
        st.session_state.state = 0


if __name__ == "__main__":
    handle_session_states()

    if st.session_state.state == 0:
        ...