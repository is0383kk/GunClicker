# GunClicker

**GunClicker** is a simple auto-clicker for Windows.
You can automate mouse clicks or keyboard key presses at a specified rate.
Features include a user-friendly GUI, F9 to start, F10 to stop, multiple key/click assignments, and bilingual UI (English/Japanese).

Use cases

- Idle Slayer
- Cookie Clicker
- Other games or tasks that involve clicking and leaving the screen idle

## 🖱️ How to use

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
$ pyinstaller --onefile --windowed gun_clicker.pyw --icon=gunclicker.ico
```

The built EXE will be at **dist/GunClicker.exe**

## 💾 About the icon

Include and specify gunclicker.ico for the application icon.

## 📝 License

This project is open-sourced under the MIT License.

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

同梱の「gun_clicker.exe」をダブルクリックで起動してください。
Python や追加のインストールは不要です。

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
pip install pyinstaller
pyinstaller --onefile --windowed gun_clicker.pyw --icon=gunclicker.ico
```

生成物は **dist/GunClicker.exe** になります

## 📝 ライセンス

This project is open-sourced under the MIT License.
