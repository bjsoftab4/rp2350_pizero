# micropython for rp2350_pizero
- RP2350-PiZERO 用のボード設定ファイル
- GamePi13 と組み合わせた際の設定ファイル
- GamePi13 と組み合わせて使う動画プレイヤー, MP3 プレイヤー

GamePi13 関連が前提としているドライバは st7789_mpy リポジトリにあります。

## build の前提

st7789_mpy を以下の構成に合わせて clone します

```
  rp2350_pizero/	this repository
      boards		micropython board configuration
      RP2350player	movie/MP3 player
      sound			micropython sound driver
  st7789_mpy/		russhughes/st7789_mpy + bitbank2/JPEGDEC
```


### ビルド手順

rp2350_pizero/boards のRP2350_PIZEROをフォルダごとmicropython ビルド環境にコピー（micropython/ports/rp2/boards）

以下のコマンドでビルド
```sh
cd micropython/ports/rp2
make USER_C_MODULES="Path/To/rp2350_pizero/micropython.cmake" BOARD=RP2350_PIZERO
```


## 配布ファイル説明
- RP2350player
  - main.py\
プレイヤー本体\
起動時にSDカードをマウントし、SDカードの中の tar ファイルを再生します。\
Selectボタン(左の十字ボタンの上にあるボタン）で再生モードを切り替えます。（音声なし動画、音声あり動画、MP3プレイヤー）\
左の十字ボタン前記の tar ファイルを /sd から読み込む設定にしています。\
左の十字ボタン　左右で前、次のファイル再生、下で1分スキップ。右の十字ボタン　上下で音量調整。\
プリズムで画面を上下反転して使う場合は main.py のinit.startLCD(0) を 2 に変更します。

  - hw_wrapper.py\
ハードウェア構成の変更用。ほかのHWに流用する場合に修正。

- RP2350player
  - hw
    - tft_config.py\
LCDの設定ファイル。st7789 ドライバが利用する。ほかのHWに流用する場合に修正。
    - init.py\
初期化用ファイル。SDカードのポート変更時に修正。
  - lib
動画や音声の再生用プログラム

- tools
  - maketar_gp.py\
指定した *.mp4 ファイルをA/V 分離し、JPEG変換、mp3変換し、 *.tar にまとめるプログラム\
GamePi13 を前提にした画質で設定。

  - setTimePC.py\
USBポートを検索しシリアルポートを見つければ、RP2350の時刻を設定するための文字列を送信するプログラム。\
Thonnyから起動すればRP2350に自動で時刻を設定するが、Thonnyを使用しない場合に使う。\
linux, windows で確認済み。

- boards\
  RP2350向けボード設定ファイル。micropython 用。

- sound\
  サウンドドライバ。micropython 用。

