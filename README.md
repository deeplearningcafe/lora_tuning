# LoRAチューニング
PytorchのDiffusersライブラリーを用いて、StableDiffusionとLoRAのファインチューニングを実行する。

## Requirements
pytorch==2.1.0
pytorch-cuda==12.1 
accelerate==0.26.1
diffusers==0.26.2
peft==0.8.2
bitsandbytes==0.42.0
transformers==4.35.2
safetensors==0.4.2


## Dataset
アニメや動画から画像を取得し、使いたいイラストを選択して画像の不要な部分を除去します。アノテーションを作成する際には、DeepDanbooruを利用できます。アニメ系以外の場合、BLIPが一般的に使用されています。最後に、LoRAチューニングを行うためにコラボを行います。


## Model description
今回使うモデルは二つあります、両方はStableDiffusion2系。ファインチューニングのために、*waifu-diffusion/wd-1-5-beta3*を使う。
推論の時には*gsdf/Replicant-V3.0*を使います。

## File description
    -screenshots.py　動画からフレームを保存する。
    -utils_lora.py データの処理。
    -create_tags_file.py　アノテーションデータの処理。
    -resize.py　画像を同じフォーマットと欲しい解像度を変わる。
    -Lora.ipynb LoRAチューニングのノートブック。
    -inference_clair_sama.ipynb LoRA推論のノートブック。

## 説明動画
[<img src="サムネイル.png" width="600" height="300"/>](https://www.youtube.com/watch?v=Fbpn3No0WXI)

## プレゼンテーション
[プレゼンテーション](LoRAの仕組み.pptx)



## Author
[aipracticecafe](https://github.com/deeplearningcafe)


## References
https://arxiv.org/abs/2112.10752

https://arxiv.org/pdf/2106.09685.pdf

https://deepsense.ai/diffusion-models-in-practice-part-1-the-tools-of-the-trade/

https://github.com/openai/CLIP

https://www.amazon.co.jp/%E5%A4%A7%E8%A6%8F%E6%A8%A1%E8%A8%80%E8%AA%9E%E3%83%A2%E3%83%87%E3%83%AB%E5%85%A5%E9%96%80-%E5%B1%B1%E7%94%B0-%E8%82%B2%E7%9F%A2/dp/4297136333

## LICENSE
このプロジェクトはMITライセンスの下でライセンスされています。詳細については[LICENSE](LICENSE.txt)ファイルを参照してください。
