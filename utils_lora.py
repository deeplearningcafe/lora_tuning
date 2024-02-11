import os
import pandas as pd
from collections import Counter

def create_tags_files(df_path:str=None, img_dir:str=None):
    """
    Creates captions files given the tags and the img_dir
    """
    df = pd.read_csv(df_path)

    img_files = os.listdir(img_dir)

    for i in range(len(df)):
        file_name, tags = df.iloc[i]
        
        if file_name in img_files:
            file_name = os.path.splitext(os.path.basename(file_name))[0]
            
            file_name = file_name + ".txt"
            file_path = os.path.join(img_dir, file_name)

            with open(file_path, 'w') as file:
                file.write(tags)
        else:
            continue

    print("Text files created successfully.")

def process_text(file_path):
    
    # return result_dict
    with open(file_path, 'r', encoding='utf-8') as file:
        # ファイルの中身を読み取る
        content = file.read()

        # 単語ごとに分割
        words = content.split(",")

        # 空白を取り除き、小文字に変換
        words = [word.strip().lower() for word in words]

        # 単語の使用回数を数える
        word_counts = Counter(words)

        return {
            'total_words': len(words),
            'word_counts': dict(word_counts)
        }


def process_all_text_files(folder_path:str=None):
    """Count words from txt files

    Args:
        folder_path (str, optional): folder where the txt files are stored. Defaults to None.

    Returns:
        Dict: dict with the total number of words and a dict with the words sorted by count
    """

    # フォルダ内の全てのtxtファイルを取得
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]


    combined_content = ""
    for txt_file in txt_files:
        file_path = os.path.join(folder_path, txt_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            combined_content += content + ', '

    # 全体の文書を単語ごとに分割
    words = combined_content.split(",")

    # 空白を取り除き、小文字に変換
    words = [word.strip().lower() for word in words]

    # 単語の使用回数を数える
    word_counts = Counter(words)

    # 使用回数が多い順にソート
    sorted_word_counts = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True))


    return {
        'total_words': len(words),
        'word_counts': sorted_word_counts
    }
    
def process_all_df_files(df_path:str=None):
    """
    Same as process_all_text_files but from a csv instead of from txt files
    """


    combined_content = ""
    df = pd.read_csv(df_path)

    for row in range(len(df)):
        tags = df.iloc[row, 1]
        # words = tags.split(",")
        
        
        combined_content += tags + ', '
    
    # 全体の文書を単語ごとに分割、各単語はリストの要素
    words = combined_content.split(",")
    
    # 空白を取り除き、小文字に変換
    words = [word.strip().lower() for word in words]


    # 単語の使用回数を数える
    word_counts = Counter(words)
    # 使用回数が多い順にソート
    sorted_word_counts = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True))


    return {
        'total_words': len(words),
        'word_counts': sorted_word_counts
    }


def delete_unique_tags(img_dir:str=None, unique_words:list=None, implicit_words:list=None):
    """ Given a txt file with the words to remove, any other word in the txt files is keep

    Args:
        img_dir (str, optional): folder with the txt files. Defaults to None.
        unique_words (list, optional): txt file with the words to remove. Defaults to None.
        implicit_words (list, optional): txt file with the words to remove. Defaults to None.
    """
    txt_files = [f for f in os.listdir(img_dir) if f.endswith('.txt')]

    for txt_file in txt_files:
        file_path = os.path.join(img_dir, txt_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            words = content.split(", ")
            words = [word.strip().lower() for word in words]

            new_content= "Asuka"
            for word in words:
                if word not in unique_words:
                    if word not in implicit_words:
                        new_content += ", " + word

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)


def create_tags_csv(df_path:str=None, img_dir:str=None, output_file:str=None):
    """
    Creates captions files given the tags and the img_dir
    """
    df = pd.read_csv(df_path)

    img_files = os.listdir(img_dir)
    drop_index = []
    for i in range(len(df)):
        file_name, tags = df.iloc[i]
        
        if file_name in img_files:
            file_name = os.path.splitext(os.path.basename(file_name))[0]
            
            file_name = file_name + ".txt"
            file_path = os.path.join(img_dir, file_name)

            with open(file_path, 'r') as file:
                content = file.read()

                df.iloc[i, 1] = content        
        else:
            drop_index.append(i)

    df = df.drop(drop_index)
    df.to_csv(output_file, index=False)

    print("Text files created successfully.", len(df))


def create_txt_from_dict(dictionary: dict=None, file_name:str=None, unique_words:list=None):
    """Creates a txt file with the words included in the unique_words list.
    Can be done only with the list but we lose the order

    Args:
        dictionary (dict, optional): containing another dict with words ordered by count. Defaults to None.
        file_name (str, optional): txt file to save. Defaults to None.
        unique_words (list, optional): txt file with words to not include. Defaults to None.
    """
    words = ""
    for word, _ in dictionary['word_counts'].items():
        if word not in unique_words:
            words += word + ", "
        
    file_name = file_name + ".txt"

    with open(file_name, 'w') as file:
        file.write(words)
    
    print("Saved")
    
def update_txt(img_dir:str=None, use_words:list=None):
    img_files = os.listdir(img_dir)
    txt_files = [f for f in os.listdir(img_dir) if f.endswith('.txt')]
    img_files = [f for f in os.listdir(img_dir) if f.endswith('.jpg')]

    
    
    for file_path in txt_files:        
        with open(file_path, 'r') as file:
            # Read the content
            content = file.read()
            
        words = ""
        content = content.split(",")
        # 空白を取り除き、小文字に変換
        content = [word.strip().lower() for word in content]
        
        for word in content:
            if word in use_words:
                words += word + ", "
        
        with open(file_path, 'w') as file:

            # Write the modified content back to the file
            file.write(words)

            print("Text files created successfully.")

def keep_unique_tags(img_dir:str=None, use_words_path:str=None, first_word:str=None):
    """ Given a txt files, keep all the words from that file and add the first word to all txt files in img_dir folder

    """
    txt_files = [f for f in os.listdir(img_dir) if f.endswith('.txt')]

    with open(use_words_path, 'r', encoding='utf-8') as file:
        content = file.read()

        use_words = content.split(", ")
        use_words = [word.strip().lower() for word in use_words]
    
    print(use_words)
    for txt_file in txt_files:
        file_path = os.path.join(img_dir, txt_file)
        new_content = first_word
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            words = content.split(", ")
            words = [word.strip().lower() for word in words]

            # new_content= "Asuka"
            for word in words:
                if word in use_words:
                    new_content += ", " + word


        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        file.close()

def keep_unique_tags_csv(df_path:str=None, use_words_path:str=None, first_word:str=None):
    """ Same as keep_unique_tags but updating a csv file instead of txt files
    """
    df = pd.read_csv(df_path)
    
    with open(use_words_path, 'r', encoding='utf-8') as file:
        content = file.read()

        use_words = content.split(", ")
        use_words = [word.strip().lower() for word in use_words]
    
    print(use_words)
    
            
    for row in range(len(df)):
        if first_word is not None:
            new_content = first_word
        else:
            new_content = ""
            
        tags = df.iloc[row, 1]
        
        words = tags.split(", ")
        words = [word.strip().lower() for word in words]

            
        for word in words:
            if word in use_words:
                new_content += ", " + word
        
        if first_word is None:
            # delete the first , 
            new_content = new_content[1:]
            
        df.iloc[row, 1] = new_content
        
    
    df.to_csv(df_path, index=False)
    

def create_csv(img_dir:str=None, output_file:str=None):
    """ Create a csv file with path and txt from txt files

    """
    img_files = os.listdir(img_dir)
    txt_files = [f for f in os.listdir(img_dir) if f.endswith('.txt')]
    img_files = [f for f in os.listdir(img_dir) if f.endswith('.jpg')]

    file_names = []
    captions = []

    for file_name, txt_name in zip(img_files, txt_files):
        file_path = os.path.join(img_dir, txt_name)
     
        with open(file_path, 'r') as file:
            # Read the content
            content = file.read()
            
        words = ""
        content = content.split(",")
        # 空白を取り除き、小文字に変換
        # content = [word.strip().lower() for word in content]
        
        for word in content:
            word.strip().lower()
            words += word + ","
            

        file_names.append(file_name)
        captions.append(words)    

    pd.DataFrame(
      {"image_filenames": file_names, "captions": captions}
    ).to_csv(output_file, index=False)
    
if __name__ == '__main__':
    img_dir = r"YOUR-INPUT-FOLDER"
    df_path = r"YOUR-OUTPUT-PATH"

    result = process_all_text_files(img_dir)

    # 結果の表示
    print("単語の数:", result['total_words'])
    print("単語の使用回数:")
    for word, count in result['word_counts'].items():
        if count > 5:
            print(f"{word}: {count}回")
    
    
    
    unique_words = [word for word, count in result['word_counts'].items() if count < 4]


    
    # create txt file to prune tags
    # create_txt_from_dict(result, "unique_words_clair_sama", unique_words)
    
    
    # from the file keep those tags and add the LoRa word
    # keep_unique_tags(img_dir=img_dir, use_words_path="unique_words_clair_sama.txt", first_word="ClairSama")
    # create_csv(img_dir, "tags_clair_sama.csv")