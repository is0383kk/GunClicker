import platform
import threading
import time
import tkinter as tk
from tkinter import messagebox

import keyboard

IS_WINDOWS = platform.system() == "Windows"

# 言語リソース辞書
LANGS = {
    "ja": {
        "title": "GunClicker",
        "key_select": "キー選択：{label}",
        "key_select_base": "キー選択",
        "remove": "-",
        "add": "+",
        "rate_label1": "一秒間に",
        "rate_label2": "回キー処理をします",
        "start": "F9で開始",
        "stop": "F10で停止",
        "mouse_left": "マウス左クリック",
        "mouse_right": "マウス右クリック",
        "shift": "SHIFT",
        "ctrl": "CTRL",
        "alt": "ALT",
        "error": "エラーが発生しました",
        "lang_toggle": "ENGLISH",
        "input_error": "入力エラー",
        "input_error_msg1": "秒間クリック回数には数値を入力してください。",
        "input_error_msg2": "秒間クリック回数は1以上で指定してください。",
        "not_set": "「キー選択」を設定してください。",
        "not_supported": "このツールはWindows専用です。",
        "not_supported_title": "非対応",
        "not_set_title": "未設定",
        "key_input_title": "キーを入力してください",
        "key_input_msg": "キーを入力してください\n（マウス左/右クリック、またはキーボード）",
    },
    "en": {
        "title": "GunClicker",
        "key_select": "Key: {label}",
        "key_select_base": "Key",
        "remove": "-",
        "add": "+",
        "rate_label1": "Clicks per second:",
        "rate_label2": "times",
        "start": "Press F9 to Start",
        "stop": "Press F10 to Stop",
        "mouse_left": "Mouse Left Click",
        "mouse_right": "Mouse Right Click",
        "shift": "SHIFT",
        "ctrl": "CTRL",
        "alt": "ALT",
        "error": "An error has occurred",
        "lang_toggle": "日本語",
        "input_error": "Input Error",
        "input_error_msg1": "Please enter a number for clicks per second.",
        "input_error_msg2": "Clicks per second must be 1 or more.",
        "not_set": "Please set a key action.",
        "not_supported": "This tool is for Windows only.",
        "not_supported_title": "Not Supported",
        "not_set_title": "Not Set",
        "key_input_title": "Press a key",
        "key_input_msg": "Press a key\n(Mouse left/right click, or keyboard)",
    },
}

if IS_WINDOWS:
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32

    # INPUT types
    INPUT_MOUSE = 0
    INPUT_KEYBOARD = 1

    # MOUSEEVENTF flags
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010

    # KEYEVENTF flags
    KEYEVENTF_EXTENDEDKEY = 0x0001
    KEYEVENTF_KEYUP = 0x0002

    class MOUSEINPUT(ctypes.Structure):
        _fields_ = (
            ("dx", wintypes.LONG),
            ("dy", wintypes.LONG),
            ("mouseData", wintypes.DWORD),
            ("dwFlags", wintypes.DWORD),
            ("time", wintypes.DWORD),
            ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
        )

    class KEYBDINPUT(ctypes.Structure):
        _fields_ = (
            ("wVk", wintypes.WORD),
            ("wScan", wintypes.WORD),
            ("dwFlags", wintypes.DWORD),
            ("time", wintypes.DWORD),
            ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
        )

    class HARDWAREINPUT(ctypes.Structure):
        _fields_ = (
            ("uMsg", wintypes.DWORD),
            ("wParamL", wintypes.WORD),
            ("wParamH", wintypes.WORD),
        )

    class INPUT_union(ctypes.Union):
        _fields_ = (
            ("mi", MOUSEINPUT),
            ("ki", KEYBDINPUT),
            ("hi", HARDWAREINPUT),
        )

    class INPUT(ctypes.Structure):
        _fields_ = (
            ("type", wintypes.DWORD),
            ("union", INPUT_union),
        )

    SendInput = user32.SendInput
    SendInput.argtypes = (wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int)
    SendInput.restype = wintypes.UINT

    GetLastError = ctypes.windll.kernel32.GetLastError


def _get_zero_ptr():
    return ctypes.pointer(ctypes.c_ulong(0)) if IS_WINDOWS else None


class Action:
    def __init__(self, kind: str, value):
        self.kind = kind
        self.value = value

    def label(self, lang="ja"):
        l = LANGS[lang]
        if self.kind == "mouse":
            return l["mouse_left"] if self.value == "left" else l["mouse_right"]
        else:
            if self.value == 0x10:
                return l["shift"]
            if self.value == 0x11:
                return l["ctrl"]
            if self.value == 0x12:
                return l["alt"]
            return f"VK({self.value})"


def send_mouse_click(button: str):
    if not IS_WINDOWS:
        return
    if button == "left":
        down_flag, up_flag = MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
    else:
        down_flag, up_flag = MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP

    zero = _get_zero_ptr()
    inputs = (INPUT * 2)()
    mi_down = MOUSEINPUT(0, 0, 0, down_flag, 0, zero)
    mi_up = MOUSEINPUT(0, 0, 0, up_flag, 0, zero)
    inputs[0].type = INPUT_MOUSE
    inputs[0].union.mi = mi_down
    inputs[1].type = INPUT_MOUSE
    inputs[1].union.mi = mi_up

    print(f"[DEBUG] send_mouse_click: {button}")
    sent = SendInput(
        2, ctypes.cast(inputs, ctypes.POINTER(INPUT)), ctypes.sizeof(INPUT)
    )
    print(f"[DEBUG] SendInput sent={sent}, GetLastError={GetLastError()}")
    if sent != 2:
        print("[ERROR] SendInput failed for mouse!")


def send_key_press(vk_code: int):
    if not IS_WINDOWS:
        return
    zero = _get_zero_ptr()
    inputs = (INPUT * 2)()
    ki_down = KEYBDINPUT(vk_code, 0, 0, 0, zero)
    ki_up = KEYBDINPUT(vk_code, 0, KEYEVENTF_KEYUP, 0, zero)
    inputs[0].type = INPUT_KEYBOARD
    inputs[0].union.ki = ki_down
    inputs[1].type = INPUT_KEYBOARD
    inputs[1].union.ki = ki_up

    print(f"[DEBUG] send_key_press: vk_code={vk_code}")
    sent = SendInput(
        2, ctypes.cast(inputs, ctypes.POINTER(INPUT)), ctypes.sizeof(INPUT)
    )
    print(f"[DEBUG] SendInput sent={sent}, GetLastError={GetLastError()}")
    if sent != 2:
        print("[ERROR] SendInput failed for key!")


class ActionSelector:
    def __init__(self, parent, on_change, on_remove, lang="ja"):
        self.parent = parent
        self.on_change = on_change
        self.on_remove = on_remove
        self.lang = lang

        self.frame = tk.Frame(parent)
        self.frame.pack(fill="x", pady=2)

        self.button = tk.Button(
            self.frame, text=LANGS[lang]["key_select_base"], command=self.capture
        )
        self.button.pack(side="left", fill="x", expand=True)

        self.remove_btn = tk.Button(
            self.frame, text=LANGS[lang]["remove"], width=3, command=self.remove
        )
        self.remove_btn.pack(side="right", padx=(4, 0))

        self.action = None
        self.capturing = False

    def update_lang(self, lang):
        self.lang = lang
        if self.action:
            label = self.action.label(lang)
            self.button.config(text=LANGS[lang]["key_select"].format(label=label))
        else:
            self.button.config(text=LANGS[lang]["key_select_base"])
        self.remove_btn.config(text=LANGS[lang]["remove"])

    def set_action(self, action: Action):
        self.action = action
        label = action.label(self.lang)
        self.button.configure(text=LANGS[self.lang]["key_select"].format(label=label))
        self.button.config(state="normal")
        self.capturing = False
        if self.on_change:
            self.on_change()

    def capture(self):
        if self.capturing:
            # 2度押しで解除（キャンセル）
            self.button.config(text=LANGS[self.lang]["key_select_base"])
            self.button.config(state="normal")
            self.parent.unbind_all("<Key>")
            self.parent.unbind_all("<Button>")
            self.capturing = False
            return

        # キー待ち受け状態
        self.button.config(
            text="→ " + LANGS[self.lang]["key_input_msg"].replace("\n", " "),
            state="disabled",
        )
        self.capturing = True

        def finish_with_mouse(event):
            if not self.capturing:
                return
            button = "left" if event.num == 1 else "right" if event.num == 3 else None
            if button:
                self.set_action(Action("mouse", button))
                self.parent.unbind_all("<Key>")
                self.parent.unbind_all("<Button>")

        def finish_with_key(event):
            if not self.capturing:
                return
            vk = int(getattr(event, "keycode", 0))
            if vk:
                self.set_action(Action("key", vk))
                self.parent.unbind_all("<Key>")
                self.parent.unbind_all("<Button>")

        self.parent.bind_all("<Key>", finish_with_key)
        self.parent.bind_all("<Button>", finish_with_mouse)

    def remove(self):
        if self.on_remove:
            self.on_remove(self)
        self.frame.destroy()


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.lang = "ja"
        self.running = False
        self.worker = None
        self.selectors = []

        if not IS_WINDOWS:
            messagebox.showerror(
                LANGS[self.lang]["not_supported_title"],
                LANGS[self.lang]["not_supported"],
            )

        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        scale = 1 / (8**0.7)
        w = int(sw * scale)
        h = int(sh * scale)
        x = (sw - w) // 2
        y = (sh - h) // 3
        root.geometry(f"{w}x{h}+{x}+{y}")

        # 言語切り替えボタン（右上）
        header_frame = tk.Frame(root)
        header_frame.pack(fill="x", side="top", anchor="n")

        lang_btn = tk.Button(
            header_frame, text=LANGS[self.lang]["lang_toggle"], command=self.toggle_lang
        )
        lang_btn.pack(side="right", padx=4, pady=4)
        self.lang_btn = lang_btn

        root.title(LANGS[self.lang]["title"])

        top = tk.Frame(root)
        top.pack(fill="both", expand=True, padx=10, pady=10)

        self.selector_frame = tk.LabelFrame(
            top, text=LANGS[self.lang]["key_select_base"]
        )
        self.selector_frame.pack(fill="x", pady=(0, 8))

        first = ActionSelector(
            self.selector_frame,
            self._on_selector_change,
            self.remove_selector,
            lang=self.lang,
        )
        first.set_action(Action("mouse", "left"))
        self.selectors.append(first)

        add_btn = tk.Button(
            self.selector_frame,
            text=LANGS[self.lang]["add"],
            width=3,
            command=self.add_selector,
        )
        add_btn.pack(anchor="e", pady=2)
        self.add_btn = add_btn

        rate_frame = tk.Frame(top)
        rate_frame.pack(fill="x", pady=(0, 8))
        # ラベル変数にして切り替えやすく
        self.rate_label1 = tk.Label(rate_frame, text=LANGS[self.lang]["rate_label1"])
        self.rate_label1.pack(side="left")
        vcmd = (root.register(self._validate_int), "%P")
        self.rate_var = tk.StringVar(value="5")
        rate_entry = tk.Entry(
            rate_frame,
            textvariable=self.rate_var,
            validate="key",
            validatecommand=vcmd,
            width=6,
            justify="right",
        )
        rate_entry.pack(side="left", padx=6)
        self.rate_entry = rate_entry
        self.rate_label2 = tk.Label(rate_frame, text=LANGS[self.lang]["rate_label2"])
        self.rate_label2.pack(side="left")

        self.status_var = tk.StringVar(value=LANGS[self.lang]["start"])
        self.status_lbl = tk.Label(
            top, textvariable=self.status_var, anchor="w", font=("Meiryo", 13)
        )
        self.status_lbl.pack(fill="x", pady=(12, 0))

        root.protocol("WM_DELETE_WINDOW", self.on_close)
        root.bind("<F9>", self.on_f9)
        root.bind("<F10>", self.on_f10)
        print("[INFO] F9で開始、F10で停止できます")

    def _validate_int(self, proposed: str):
        if proposed == "":
            return True
        return proposed.isdigit()

    def _on_selector_change(self):
        pass

    def add_selector(self):
        sel = ActionSelector(
            self.selector_frame,
            self._on_selector_change,
            self.remove_selector,
            lang=self.lang,
        )
        self.selectors.append(sel)

    def remove_selector(self, selector):
        self.selectors.remove(selector)

    def on_f9(self, event=None):
        print("[DEBUG] F9 pressed → start")
        if not self.running:
            self.start()

    def on_f10(self, event=None):
        print("[DEBUG] F10 pressed → stop")
        if self.running:
            self.stop()

    def toggle_lang(self):
        self.lang = "en" if self.lang == "ja" else "ja"
        self._update_ui_lang()

    def _update_ui_lang(self):
        lang = LANGS[self.lang]
        self.root.title(lang["title"])
        self.selector_frame.config(text=lang["key_select_base"])
        self.add_btn.config(text=lang["add"])
        self.status_var.set(lang["start"] if not self.running else lang["stop"])
        self.lang_btn.config(text=lang["lang_toggle"])
        self.rate_label1.config(text=lang["rate_label1"])
        self.rate_label2.config(text=lang["rate_label2"])
        for sel in self.selectors:
            sel.update_lang(self.lang)

    def start(self):
        if not IS_WINDOWS:
            messagebox.showerror(
                LANGS[self.lang]["not_supported_title"],
                LANGS[self.lang]["not_supported"],
            )
            return
        rate_txt = self.rate_var.get().strip()
        if not rate_txt or not rate_txt.isdigit():
            messagebox.showwarning(
                LANGS[self.lang]["input_error"], LANGS[self.lang]["input_error_msg1"]
            )
            return
        rate = int(rate_txt)
        if rate <= 0:
            messagebox.showwarning(
                LANGS[self.lang]["input_error"], LANGS[self.lang]["input_error_msg2"]
            )
            return
        actions = [s.action for s in self.selectors if s.action is not None]
        if not actions:
            messagebox.showwarning(
                LANGS[self.lang]["not_set_title"], LANGS[self.lang]["not_set"]
            )
            return

        self._set_controls_enabled(False)
        self.running = True
        self.status_var.set(LANGS[self.lang]["stop"])
        self.worker = threading.Thread(
            target=self._run_worker, args=(actions, rate), daemon=True
        )
        self.worker.start()

    def stop(self):
        self.running = False
        self.status_var.set(LANGS[self.lang]["start"])
        self._set_controls_enabled(True)

    def _set_controls_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        for s in self.selectors:
            s.button.configure(state=state)
            s.remove_btn.configure(state=state)
        self.add_btn.configure(state=state)
        self.rate_entry.configure(state=state)

    def _run_worker(self, actions, rate):
        import traceback

        try:
            interval = 1.0 / float(rate)
            next_time = time.perf_counter()
            while self.running:
                for act in actions:
                    print(f"[DEBUG] Action: kind={act.kind}, value={act.value}")
                    if act.kind == "mouse":
                        send_mouse_click(act.value)
                    elif act.kind == "key":
                        send_key_press(int(act.value))
                next_time += interval
                sleep_for = max(0.0, next_time - time.perf_counter())
                if sleep_for > 0:
                    time.sleep(sleep_for)
                else:
                    next_time = time.perf_counter()
        except Exception:
            print("例外:", traceback.format_exc())
            self.running = False
            self.status_var.set(LANGS[self.lang]["error"])
            self._set_controls_enabled(True)

    def on_close(self):
        self.running = False
        self.root.destroy()


def main():
    root = tk.Tk()

    try:
        root.iconbitmap("gunclicker.ico")
    except Exception as e:
        print(f"アイコン設定エラー: {e}")

    app = App(root)

    # --- グローバルホットキー登録 ---
    def on_f9():
        if not app.running:
            app.start()

    def on_f10():
        if app.running:
            app.stop()

    # グローバルでF9/F10押下を検知
    keyboard.add_hotkey("F9", on_f9)
    keyboard.add_hotkey("F10", on_f10)

    root.mainloop()

    # 終了時ホットキー解除
    keyboard.unhook_all_hotkeys()


if __name__ == "__main__":
    main()
