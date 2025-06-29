import os

def save_document(file, file_dir):
    """
    Save document in the selected path

    does:
        This function is responsible for save the document in selected file.
    
    args:
        file -> file need to save
        file_path -> path to save the file
    """

    file_path = os.path.join(file_dir, file.name)
    
    # check path is already exists or not
    os.makedirs(file_dir, exist_ok= True)

    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    
    return file_path