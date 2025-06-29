import streamlit as st
from utils.saveDocument import save_document

# handle the session states use to processes comes in the main process
def handle_session_states():
    if "state" not in st.session_state:
        st.session_state.state = 0


def UserFileUploadUI():
    """
    File upload interface

    does:
        This funciton provide user interface for user interaction. upload the file and  save it in the selected document
    """

    st.title("Upload you file.")
    st.text("Upload file what you need to chat with the knowledge.")

    with st.container():
        upload_file = st.file_uploader("Uplad file:")
        is_submited = st.button("Let's chat")

        if is_submited:
            if not upload_file:
                st.error("Please select the file.")
            else:
                save_document(upload_file, "documents")
            
if __name__ == "__main__":
    handle_session_states()

    if st.session_state.state == 0:
        UserFileUploadUI()