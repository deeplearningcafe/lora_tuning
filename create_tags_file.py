import pandas as pd
import os
import shutil

def parse_name(path):
    name = os.path.basename(path)
    return str(name)

def udpate_csv(new_path, source_path):
    df = pd.read_csv(source_path)
    
    for row in range(len(df)):
        original_path = df.iloc[row, 0]
        name = parse_name(original_path)

        df.iloc[row, 0] = name
    
    df.to_csv(new_path, index=False)

def remove_formats(new_path, source_path):
    # when resizing we removed some img formats, so update the csv

    remove_index = []
    df = pd.read_csv(source_path)
    
    for row in range(len(df)):
        filename = df.iloc[row, 0]
        if not filename.endswith((".jpg", ".jpeg", ".png")):
            # print(filename)
            remove_index.append(row)
    

    df = df.drop(remove_index)
    df.to_csv(new_path, index=False)
    print("dropped: ", len(remove_index))
    
def unify_formats(new_path, source_path):
    changed = 0
    df = pd.read_csv(source_path)
    
    for row in range(len(df)):
        filename = df.iloc[row, 0]
        if not filename.endswith((".jpg")):
            new_file_name = os.path.splitext(filename)[0] + '.jpg'
                      
            df.iloc[row, 0] = new_file_name
            changed += 1
    

    df.to_csv(new_path, index=False)
    print("changed: ", changed)
    
def check_df(df_path, img_dir, new_df=None):
    """
    Checks that the imgs included in the df are in the folder, if not they get removed from the df
    Args:
        df_path (str): path of the df we want to check
        img_dir (str): path of the image folder
    """
    
    # the tags df has 1 row more than the training so remove that row
    image_filenames = os.listdir(img_dir)
    df = pd.read_csv(df_path)
    print(len(df), len(image_filenames))
    remove_index = []
    
    for row in range(len(df)):
        filename = df.iloc[row, 0]
        if filename not in image_filenames:
            remove_index.append(row)

    df = df.drop(remove_index)

    if new_df is not None:
        df.to_csv(new_df, index=False)
    else:
        
        df.to_csv(df_path, index=False)
        
    print("removed: ", len(remove_index))
    
    
def parse_tag(text):
    """
    Replace spaces by , and _ by spaces

    Args:
        text (str): sentence to parse
    """
    word_list = text.split(",")
    word_list = [word.strip().lower() for word in word_list]
    # print(word_list)
    for i in range(len(word_list)):
        word = word_list[i]
        
        word_list[i] = word.replace('_', ' ')
        
    result = ', '.join(word_list)
    
    # print(result)
    return result
    
    
def danbooru_prompt_styling(df_path):
    df = pd.read_csv(df_path)
    
    for row in range(len(df)):
        original_tag = df.iloc[row, 1]
        new_tag = parse_tag(original_tag)


        df.iloc[row, 1] = new_tag
    
    df.to_csv(df_path, index=False)

def character_tags(new_path:str=None, source_path:str=None, character:str=None):
    """
    Returns a df only containing character imgs

    Args:
        new_path (str, optional): _description_. Defaults to None.
        source_path (str, optional): path of the df we want to check. Defaults to None.
    """
    df = pd.read_csv(source_path)
    remove_index = []

    for row in range(len(df)):
        tags = df.iloc[row, 1]
        if character not in tags:
            remove_index.append(row)

    df = df.drop(remove_index)
    df.to_csv(new_path, index=False)
    print("removed: ", len(remove_index))
    print("New len: ", len(df))
    
    
def create_character_folder(img_dir:str=None, df_path:str=None, destination:str=None):
    """
    reads the image names from a CSV file and copies the corresponding images to a new folder

    Args:
        img_dir (str, optional): /path/to/source/folder. Defaults to None.
        df_path (str, optional): /path/to/your/csvfile.csv. Defaults to None.
        destination (str, optional): path/to/destination/folder". Defaults to None.
    """
    if not os.path.exists(destination):
        os.makedirs(destination)

    df = pd.read_csv(df_path)
    filenames = df["image_filenames"]
    
    # Copy images to the destination folder
    for image_name in filenames:
        source_path = os.path.join(img_dir, image_name)
        destination_path = os.path.join(destination, image_name)

        # Check if the source file exists before copying
        if os.path.exists(source_path):
            shutil.copy2(source_path, destination_path)
            print(f"Copied: {image_name}")
        else:
            print(f"File not found: {image_name}")

    print("Copy process completed.")

        
if __name__ == "__main__":
    danbooru_prompt_styling("tags_clair_sama.csv")
