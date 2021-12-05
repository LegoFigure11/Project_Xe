# Instructions
1. Obtain a copy of this repository, either by cloning or downloading and extracting the zip
<img width="678" alt="downloadzip" src="https://user-images.githubusercontent.com/24732684/144750768-e00b6fc1-3f99-44ce-8b2a-3d82bbc0a2b0.png">
2. Install <a href="https://www.python.org/">python</a>. Make sure you tick the "Add to PATH" option during the installation!

3. Open a command prompt (`Windows Key` + `r` -> `cmd.exe`) or terminal window.

4. Navigate to the folder containing the scripts with the `cd` command.
    
    4a. e.g. `cd C:\Users\Lego\Downloads\Project_Xe-main\Project_Xe-main\src`
    
5. Run `pip install numpy` (you only need to do this once!)

6. Run the script with the command `python main.py`


See <a href="https://youtu.be/brzi2HhFTaQ">this handy video</a> to see how to apply this tool.

# Original README:

# Project Xe

xoroshiro128+が連続して出力する128個の乱数列(64bit)の下位1bitから内部状態(128bit=64bit+64bit)を逆算するプログラムです.

src/test.pyが逆算が成功しているproofになっています. たぶん色々書き換えれば逆算ツールになるはずです.

# Reference
### xoroshiro128+の状態遷移の逆算の考察
https://hackmd.io/@yatsuna827/r1ez2-n3S

### 【TinyMT】なぜ乱数値の最下位bit列から元の内部状態を復元できるのか考えてみた。
https://ameblo.jp/yatsuna/entry-12337825820.html
