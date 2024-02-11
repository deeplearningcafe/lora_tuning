from PIL import Image
import os
from tqdm import tqdm

# リサイズ後のサイズを指定
target_size = (512, 768)

# 画像があるフォルダのパスを指定
folder_path = r"YOUR-FOLDER-WITH-IMAGES"
target_path = r"THE-FOLDER-TO-SAVE-RESIZED-IMAGES"
if not os.path.exists(target_path):
    os.mkdir(target_path)

# フォルダ内の全ての画像ファイルに対して処理
for filename in tqdm(os.listdir(folder_path)):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        # 画像のフルパス
        full_path = os.path.join(folder_path, filename)

        # 画像を開いてリサイズ
        image = Image.open(full_path)
        # RGBAモードの画像をRGBモードに変換
        rgb_image = image.convert('RGB')
        
        resized_image = rgb_image.resize(target_size)

        # リサイズ後の画像をJPEG形式で保存（元の拡張子はjpgに変更）
        # resized_image.save(full_path.replace(os.path.splitext(filename)[1], ".jpg"))
        # リサイズ後の画像を保存（上書き注意）
        save_path = os.path.join(target_path, filename)
        
        # print(save_path.replace(os.path.splitext(filename)[1], ".jpg"))
        resized_image.save(save_path.replace(os.path.splitext(filename)[1], ".jpg"))
        
print("リサイズと保存が完了しました。")
