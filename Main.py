import os
import streamlit as st
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate


# handle the session states use to processes comes in the main process
def handle_session_states():
    if "state" not in st.session_state:
        st.session_state.state = 0

    if "messages" not in st.session_state:
        st.session_state.messages = []

        st.session_state.messages.append({
            'role' : 'Assistant',
            'message' : 'Hello, what are the things you need to know from the document ?'
        })


def save_document(file, file_dir):
    """
    Save document in the selected path

    does:
        This function is responsible for save the document in selected file.
    
    args:
        file -> file need to save
        file_path -> path to save the file
    """

    try:
        file_path = os.path.join(file_dir, file.name)
        
        # check path is already exists or not
        os.makedirs(file_dir, exist_ok= True)

        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        
        return file_path
    except Exception as e:
        print(f"Something went wrong in document saving process.... {e}")
        return None


def extract_content(file_path):
    """
    Document content extractor

    does:
        This function is responsible for extract data from the uploaded document

    args:
        file_path -> where the responsible document is saved.
    
    return:
        extracted content        
    """
    
    try:
        document_reader_object = PdfReader(file_path)
        document_page_count = len(document_reader_object.pages)
        document_content = ""

        for i in range(0, document_page_count):
            current_page = document_reader_object.pages[i]
            page_content = current_page.extract_text()

            if page_content:
                document_content += page_content.strip().replace("\t","").replace("\n","")
        
        return document_content
    except Exception as e:
        print(f"Something went wrong in text extraction process... {e}")
        return None


def document_text_splitter(content):
    """
    Split text into chunks

    does:
        This function is responsible for split text into small chunks
    
    args:
        content -> what is the content need to split into chunks

    return:
        splitted_document
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 2000,
            chunk_overlap = 400
        )

        splitted_documents = text_splitter.create_documents([content])
        return splitted_documents
    except Exception as e:
        print(f"Something went wrong in text splitting process.. {e}")
        return None
    


def embedding_function():
    """
    Text embedding function

    does:
        this function is responsible for create the embeddings
    """

    try:
        model_name = "sentence-transformers/all-mpnet-base-v2"
        model_kwargs = {'device' : 'cpu'}
        
        embedder = HuggingFaceEmbeddings(
            model_name = model_name,
            model_kwargs = model_kwargs
        )

        return embedder
    except Exception as e:
        print(f"Something went wrongi in text embedding function... {e}")


def create_vectore_store(chunks,embedding_function,file_path):
    """
    Craete vectore database to store vectors

    does:
        This function is responsible for create vectore database for upcomming operations
    """ 
    try:
        if not os.path.exists(file_path):
            vector_store = Chroma.from_documents(
                documents= chunks,
                embedding= embedding_function,
                persist_directory= file_path
            )
    except Exception as e:
        print(f"Something went wrong in vectore store creation process... {e}")


def access_vector_database_retriever(embedding_func, path):
    """
    Access the specific vectore store and make it with similarity searchs

    does:
        this function is responsible for access the vectore database and create reciever for similarity search
    
    args:
        embedding function
        path -> responsible vector store path

    return:
        similarity search reciever
    """
    
    try:
        vector_store = Chroma(
            embedding_function= embedding_func(),
            persist_directory= path
        )

        retriever = vector_store.as_retriever(search_type = "similarity")
        
        return retriever
    except Exception as e:
        print(f"Something went wrong in vector database accessing process.. {e}")
        return None

def prompt_maker(question, documents):
    template = """
    You is a assistant for provide simple and relvent answers for the question using the provided contents. You need to use simple english and relevent answers to easy understanding.

    question : {question}
    related documents : {documents}
    """

    try:
        prompt_template = ChatPromptTemplate.from_template(template)
        prompt = prompt_template.invoke({
            "question" : question,
            "documents" : documents
        })

        return prompt
    except Exception as e:
        print(f"Something went wrong in promt making process.. {e}")


def ollama_connection():
    """
    Create connection with the ollama llm model

    does:
        this funciton is responsible for create connection with the ollama model store in the local pc
    """

    try:
        model_name = "gemma3:1b"
        temp = 0.7
        base_url = "127.0.0.1:11435"

        llm = ChatOllama(
            model= model_name,
            temperature= temp,
            base_url= base_url
        )

        return llm
        
    except Exception as e:
        print(f"Something went wrong in llm connection process.. {e}")
        return None


def generate_response(question, documents):

    try:
        prompt = prompt_maker(question, documents)
        llm = ollama_connection()

        response = llm.invoke(prompt)
        return response 
    except Exception as e:
        print(f"Something went wrong in response generation process.. {e}")

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
                saved_path = save_document(upload_file, "documents")

                if saved_path:
                    document_content = extract_content(saved_path)
                    splitted_documents = document_text_splitter(document_content)

                    vector_database = create_vectore_store(
                        chunks= splitted_documents,
                        embedding_function= embedding_function(),
                        file_path= "document_vector"
                    )
                    
                    st.session_state.state = 1
                    st.rerun()
            


def chat_interface():
    st.title("Lets collect knowledge")

    # show previos message
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['message'])
    

    user_message = st.chat_input("What you need to ask")

    if user_message:
        st.session_state.messages.append({
            'role' : 'human',
            'message' : user_message
        })

        vectore_store = access_vector_database_retriever(
            embedding_func= embedding_function,
            path= "document_vector"
        )

        documents = vectore_store.invoke(user_message)
        print(documents)

        response = generate_response(user_message, documents)

        st.session_state.messages.append({
            'role' : 'assistant',
            'message' : response.content
        })
        
        st.rerun()
    
            
if __name__ == "__main__":
    handle_session_states()

    if st.session_state.state == 0:
        UserFileUploadUI()
    elif st.session_state.state == 1:
        chat_interface()