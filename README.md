# GunClicker

**GunClicker** is a simple auto-clicker for Windows.
You can automate mouse clicks or keyboard key presses at a specified rate.
Features include a user-friendly GUI, F9 to start, F10 to stop, multiple key/click assignments, and bilingual UI (English/Japanese).

Use cases

- Idle Slayer
- Cookie Clicker
- Other games or tasks that involve clicking and leaving the screen idle

![](https://github.com/is0383kk/GunClicker/blob/main/img/gunclicker.gif)

## 🖱️ How to use

Download the compressed file from the [release](https://github.com/is0383kk/GunClicker/releases/tag/20250818_v1.0.0) page.  
Double-click “gun_clicker.exe” included in the package to launch the program.  
![](https://github.com/is0383kk/GunClicker/blob/main/img/gunclicker.png)

1. Select Key/Click Actions

- Click the "Key" button to register a key or mouse action.
- The button text will prompt you to press a key or mouse button (left/right click) to set the action.
- You can register multiple actions by pressing the "+" button.
- Remove actions with the "-" button.

2. Set Clicks per Second

- Enter the number of clicks or key actions per second in the input field next to "Clicks per second:".
- For example, entering "5" will perform the action 5 times per second.

3. Start / Stop

- At the top right, the message shows "Press F9 to Start / F10 to Stop".
- Press F9 to start, and F10 to stop the action.
- These hotkeys work even when the app window is not in focus or you are using other apps.
- The status at the bottom shows the current state ("Press F9 to Start" / "Press F10 to Stop" etc.).

4. Other

- Press the "日本語" button to switch the UI to Japanese.
- Any errors during setup or operation will be shown as dialog messages.

## 🧑‍💻 For Developers

### 💻 Environment

- Supported OS: Windows (10 or later recommended)
- Python: 3.8+
- No additional dependencies (standard library only)

## 🖱️ How to use（For Developers）

- Run gun_clicker.pyw (double-click or python gun_clicker.pyw)

- Add/select the key or mouse action you want to automate

- Set the clicks per second (e.g., 10)

- Press F9 to start, F10 to stop

- Use the language button (top right) to toggle English/Japanese

- Note: Windows only. Does not run on Mac/Linux.

## 📦 Build (Create Standalone EXE)

- Build with pyinstaller:

```sh
$ pip install pyinstaller
$ pip install keyboard
$ pyinstaller --onefile --windowed gun_clicker.pyw --icon=gunclicker.ico
```

The built EXE will be at **dist/GunClicker.exe**

---

## 🪄 概要

**GunClicker** は、Windows 用に設計されたシンプルな自動クリックツールです。  
指定したレートでマウスクリックやキーボードのキー入力を自動化できます。  
F9 キーで開始、F10 キーで停止、複数のキー/クリックの割り当てが可能です。  

ユースケース

- Idle Slayer
- CookieClicker
- その他、クリック操作で放置するゲームや作業

---

## 🖱️ 使い方

[リリースページ](https://github.com/is0383kk/GunClicker/releases/tag/20250818_v1.0.0)から圧縮ファイルをダウンロードしてください。  
同梱の「gun_clicker.exe」をダブルクリックで起動してください。  
![](https://github.com/is0383kk/GunClicker/blob/main/img/gunclicker_ja.png)

1. キー/クリックアクションの選択

- 「キー選択」ボタンを押すと、設定したいキーやマウスクリックを登録できます。
- ボタンを押すと「キーを入力してください」という表示になり、登録したいキーやマウスクリック（左クリック or 右クリック）を押してください。
- 複数のキー/クリックを登録したい場合は「+」ボタンで追加できます。
- 「-」ボタンでアクションの削除もできます。

2. 秒間クリック数の設定

- 「一秒間に ◯ 回キー処理をします」欄で、実行したいクリック/キー入力の回数を数字で入力します。
- 例：5 を入力すると 1 秒に 5 回実行されます。

3. 開始／停止

- 画面右上に**「F9 で開始／F10 で停止」**のガイダンスが表示されます。
- F9 キーを押すと開始、F10 キーで停止します。
- このホットキーはアプリ画面の外、他のアプリ操作中でも有効です。
- 画面下のステータス表示（「F9 で開始」「F10 で停止」等）が現在の状態を示します。

4. その他

- 「ENGLISH」ボタンを押すと英語表示に切り替えできます。
- 設定・操作中にエラーが出た場合はダイアログで案内されます。
- Python や追加のインストールは不要です。

## 🧑‍💻 開発者向け

### 💻 動作環境

- **動作環境**: Windows（10 以降推奨）
- **Python**: 3.8 以降
- **追加ライブラリ不要（標準ライブラリのみ）**

### 🖱️ 使い方（開発者向け）

1. `gun_clicker.pyw` をダブルクリック、または `python gun_clicker.pyw` で実行
2. クリックまたはキー入力動作を追加・選択
3. 秒間回数を指定（例: 10）
4. **F9**キーで自動クリック開始、**F10**キーで停止
5. UI 右上のボタンで「日本語/ENGLISH」切り替え

> ※ Windows 専用です。Mac や Linux では動作しません。

---

### 📦 ビルド（EXE 作成）

`pyinstaller`で単体実行ファイル化できます：

```sh
$ pip install pyinstaller
$ pip install keyboard
$ pyinstaller --onefile --windowed gun_clicker.pyw --icon=gunclicker.ico
```

生成物は **dist/GunClicker.exe** になります
