import tkinter
from tkinter import scrolledtext
from tkinter.filedialog import askopenfilename, asksaveasfilename
import time
from QED_system import Verschlüsselung
import QED_hilfsfunktionen as hilfsfunktionen
from random import randint


def save_file(text, return_path:bool= False) -> None | str:
    """Save the 'text' as a new file."""

    filepath = asksaveasfilename(
        defaultextension=".qed.dat",
        filetypes=[("QED-Files", ".qed.dat"), ("Textfiles", "*.txt"), ("All Files", "*")],
        )
    if not filepath:
        return
    content = bytes(hilfsfunktionen.BitToInt(text))
    with open(filepath, "wb") as f:
        f.write(content)
    if return_path: return filepath

def open_file() -> tuple[str, str]:
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("QED-Files", ".qed.dat"), ("Textfiles", "*.txt"), ("All Files", "*")],
    )
    if not filepath:
        raise FileNotFoundError("No file was selected or no file could be parsed")
    with open(filepath, mode="rb") as f:
        content = f.read()
        content_arr:list[int] = []
        for i in content:
            content_arr.append(i)
        #print(content_arr)
        text = "".join(hilfsfunktionen.IntToBit(i) for i in content_arr)
        return text, filepath


class GUI():
    def __init__(self, texts:dict= {"o":"", "p":"", "v":"", "e":""}, chunk:int= 16, KEY:list= ["",""], debug:bool= False) -> None:
        self.texts = texts
        self.KEY = KEY
        self.chunk = chunk
        self.debug = debug
        
        self.create_gui(version_index="die funktionierende Version™", gui_version="nicht schön aber hässlich")

    def create_gui(self, version_index:str, gui_version:str) -> None:
        self.main_window = tkinter.Tk()
        self.main_window.title(f"\"QED_GUI\" - version: {gui_version} // \"QED_system\" - version: {version_index}")
        #main_window.geometry("1920x1080")
        self.main_window.columnconfigure(index=1, minsize=20, weight=1)
        self.main_window.rowconfigure(index=1, minsize=20,weight=1)


        self.top_btns = tkinter.Frame(master=self.main_window)
        self.top_btns.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        self.ver_btns = tkinter.Frame(master=self.main_window)
        self.ver_btns.grid(row=3, column=1, padx=5, pady=5, sticky="nw")

        self.ent_btns = tkinter.Frame(master=self.main_window)
        self.ent_btns.grid(row=3, column=0, padx=5, pady=5, sticky="nw")

        self.key_btns = tkinter.Frame(master=self.main_window)
        self.key_btns.grid(row=1, column=1, padx=5, pady=5, sticky="nw")

        self.keygen_btns = tkinter.Frame(self.main_window)
        self.keygen_btns.grid(row=2, column=1, padx=5, pady=5, sticky="nw")

        self.o_btns = tkinter.Frame(master=self.main_window)
        self.o_btns.grid(row=1, column=0, padx=5, pady=5, sticky="nw")


        """CONTROL"""
        self.ver_btn = tkinter.Button(master=self.top_btns, background = "#ffffff", fg = "#000000", text="Verschlüsseln", command=lambda: self.crypt(encrypt=True))
        self.ver_btn.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.ver_btn = tkinter.Button(master=self.top_btns, background = "#ffffff", fg = "#000000", text="Entschlüsseln", command=lambda: self.crypt(encrypt=False))
        self.ver_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

        """KEY"""
        self.key_lbl = tkinter.Label(master=self.key_btns, background = "#ffffff", fg = "#000000", text="Schlüssel: ")
        self.key_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.key_btn = tkinter.Button(master=self.key_btns, background = "#ffffff", fg = "#000000", text="Schlüssel-Datei öffnen", command=lambda: self.open_file_f("k"))
        self.key_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        self.key_lbl = tkinter.Label(master=self.key_btns, background = "#ffffff", fg = "#000000", text=self.KEY[1])
        self.key_lbl.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.key_btn_X = tkinter.Button(master=self.key_btns, background = "#ffffff", fg = "#000000", text="X", command=lambda: self.delete_file_f("k"))
        self.key_btn_X.grid(row=0, column=3, padx=5, pady=5, sticky="nw")

        '''KEY-GEN'''
        #len
        self.keygen_len_lbl = tkinter.Label(master=self.keygen_btns, background = "#ffffff", fg="#000000", text="KEY-gen-length:")
        self.keygen_len_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.keygen_len_entry = tkinter.Entry(self.keygen_btns, background = "#ffffff", fg="#000000")
        self.keygen_len_entry.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        #generate & output
        self.keygen_output_btn = tkinter.Button(master=self.keygen_btns, background="#ffffff", fg="#000000", text="Schlüssel-Datei generieren und speichern", command=self.save_key)
        self.keygen_output_btn.grid(row=1, column=1, padx=5, pady=5, sticky="nw")

        """ORIGINAL"""
        self.TEXT_o_lbl = tkinter.Label(master=self.o_btns, background = "#ffffff", fg = "#000000", text="Bitte Text eingeben:")
        self.TEXT_o_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.TEXT_o_btn_o = tkinter.Button(master=self.o_btns, background = "#ffffff", fg = "#000000", text="Textdatei öffnen", command=lambda: self.open_file_f("o"))
        self.TEXT_o_btn_o.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        self.TEXT_o_lbl_p = tkinter.Label(master=self.o_btns, background = "#ffffff", fg = "#000000", text=self.texts["p"])
        self.TEXT_o_lbl_p.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.TEXT_o_btn_x = tkinter.Button(master=self.o_btns, background = "#ffffff", fg = "#000000", text="X", command=lambda: self.delete_file_f("o"))
        self.TEXT_o_btn_x.grid(row=0, column=3, padx=5, pady=5, sticky="nw")
        self.TEXT_o_sct = scrolledtext.ScrolledText(master=self.main_window, wrap="word", background = "#ffffff", fg = "#000000")
        self.TEXT_o_sct.grid(row=2, column=0, padx=5, pady=5, sticky="nw", columnspan=2)

        """ENT"""
        self.TEXT_e_lbl = tkinter.Label(master=self.ent_btns, background = "#ffffff", fg = "#000000", text="Entschlüsselter Text:")
        self.TEXT_e_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.use_as_input_e_btn = tkinter.Button(master=self.ent_btns, background = "#ffffff", fg = "#000000", text="<als Eingabe verwenden>", command=lambda:self.use_as_input("e"))
        self.use_as_input_e_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        self.save_e_btn = tkinter.Button(master=self.ent_btns, background = "#ffffff", fg = "#000000", text="in Datei speichern", command=lambda:save_file(self.texts["e"]))
        self.save_e_btn.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.TEXT_e_sct = scrolledtext.ScrolledText(master=self.main_window, wrap="word", background = "#ffffff", fg = "#000000", state="disabled")
        self.TEXT_e_sct.grid(row=4, column=0, padx=5, pady=5, sticky="nw")

        """VER"""
        self.TEXT_v_lbl = tkinter.Label(master=self.ver_btns, background = "#ffffff", fg = "#000000", text="Verschlüsselter Text:")
        self.TEXT_v_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.use_as_input_v_btn = tkinter.Button(master=self.ver_btns, background = "#ffffff", fg = "#000000", text="<als Eingabe verwenden>", command=lambda:self.use_as_input("v"))
        self.use_as_input_v_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        self.save_v_btn = tkinter.Button(master=self.ver_btns, background = "#ffffff", fg = "#000000", text="in Datei speichern", command=lambda:save_file(self.texts["v"]))
        self.save_v_btn.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.TEXT_v_sct = scrolledtext.ScrolledText(master=self.main_window, wrap="word", background = "#ffffff", fg = "#000000", state="disabled")
        self.TEXT_v_sct.grid(row=4, column=1, padx=5, pady=5, sticky="ne")


        self.main_window.mainloop()

    def start(self) -> None:
        if (self.texts["o"] != "") and (self.KEY[0] != ""):
            if self.debug: print("Verarbeiten...")
            duration = time.time()
            v = Verschlüsselung(chunk = self.chunk, debug = False)
            self.texts["v"] = v.verschlüsseln(text = self.texts["o"], KEY = self.KEY[0])
            self.texts["e"] = v.entschlüsseln(text = self.texts["o"], KEY = self.KEY[0])
            duration = time.time() - duration
            if self.debug: print("duration: ", duration)
            if self.debug: print("V: ", bytes(hilfsfunktionen.BitToInt(self.texts["v"])), "\n\nE: ", bytes(hilfsfunktionen.BitToInt(self.texts["e"])))
            if self.debug: print(f"len(V): {len(bytes(hilfsfunktionen.BitToInt(self.texts['v'])))}\nlen(E): {len(bytes(hilfsfunktionen.BitToInt(self.texts['e'])))}")

            self.TEXT_v_sct.configure(state="normal")
            self.TEXT_v_sct.delete("1.0", tkinter.END)
            self.TEXT_v_sct.insert(tkinter.INSERT, "".join([chr(i) for i in hilfsfunktionen.BitToInt(self.texts["v"])]))
            self.TEXT_v_sct.configure(state="disabled")

            self.TEXT_e_sct.configure(state="normal")
            self.TEXT_e_sct.delete("1.0", tkinter.END)
            self.TEXT_e_sct.insert(tkinter.INSERT, "".join([chr(i) for i in hilfsfunktionen.BitToInt(self.texts["e"])]))
            self.TEXT_e_sct.configure(state="disabled")
            if self.debug: print("fertig")

    def crypt(self, encrypt:bool):
        if (self.texts["o"] == "") or (self.KEY[0] == ""):
            if self.debug: print("Text oder Key nicht festgelegt...")
            return
        if self.debug: print("Verarbeiten...")
        duration = time.time()
        v = Verschlüsselung(chunk=self.chunk, debug=False)
        if encrypt:
            self.texts["v"] = v.verschlüsseln(text = self.texts["o"], KEY = self.KEY[0])
            #self.texts["v"] = bytes(hilfsfunktionen.BitToInt(v.verschlüsseln(self.texts["o"], self.KEY[0])))
            #v.verschlüsseln(self.texts["input"], self.KEY[0])
            #bytes(hilfsfunktionen.BitToInt(v.verschlüsseln(self.texts["input"], self.KEY[0])))

            self.TEXT_v_sct.configure(state="normal")
            self.TEXT_v_sct.delete("1.0", tkinter.END)
            self.TEXT_v_sct.insert(tkinter.INSERT, "".join([chr(i) for i in hilfsfunktionen.BitToInt(self.texts["v"])]))
            self.TEXT_v_sct.configure(state="disabled")
        else:
            self.texts["e"] = v.entschlüsseln(text = self.texts["o"], KEY = self.KEY[0])
            #self.texts["e"] = bytes(hilfsfunktionen.BitToInt(v.entschlüsseln(self.texts["o"], self.KEY[0])))

            self.TEXT_e_sct.configure(state="normal")
            self.TEXT_e_sct.delete("1.0", tkinter.END)
            self.TEXT_e_sct.insert(tkinter.INSERT, "".join([chr(i) for i in hilfsfunktionen.BitToInt(self.texts["e"])]))
            self.TEXT_e_sct.configure(state="disabled")

        duration = time.time() - duration
        if self.debug: print("duration: ", duration)
        if self.debug: print("output: ", self.texts["v"] if encrypt else self.texts["e"])
        if self.debug: print("fertig")

    def open_file_f(self, w:str|None= None) -> None:
        if w == "k":
            self.KEY[0], self.KEY[1] = open_file()
            if self.debug: print("Schlüssel: ", self.KEY[0])
            self.key_lbl.configure(text=str(self.KEY[1]))
        elif w == "kg":
            pass
        else:
            self.texts["o"], self.texts["p"] = open_file()
            if self.debug: print("Original Text:",self.texts["o"])
            self.TEXT_o_sct.configure(state="normal")
            self.TEXT_o_sct.delete("1.0", tkinter.END)
            self.TEXT_o_sct.insert(tkinter.INSERT, "".join([chr(i) for i in hilfsfunktionen.BitToInt(self.texts["o"])]))
            self.TEXT_o_sct.configure(state="disabled")
            self.TEXT_o_lbl_p.configure(text=str(self.texts["p"]))

    def save_key(self) -> None:
        key = hilfsfunktionen.IntToBit(randint(1,2**(8*int(self.keygen_len_entry.get()))))
        filepath = save_file(key, return_path=True)
        self.KEY[0] = key
        self.KEY[1] = filepath

    def delete_file_f(self, w:str|None= None) -> None:
        if w == "k":
            self.KEY[0], self.KEY[1] = "", ""
            self.key_lbl.configure(text="")
        else:
            self.texts["o"], self.texts["p"] = "", ""
            self.TEXT_o_sct.configure(state="normal")
            self.TEXT_o_sct.delete("1.0",tkinter.END)
            self.TEXT_o_sct.configure(state="disabled")
            self.TEXT_o_lbl_p.configure(text="")

    def use_as_input(self, what:str) -> None:
        if what == "v":
            self.texts["o"] = self.texts["v"]
            self.TEXT_o_sct.configure(state="normal")
            self.TEXT_o_sct.delete("1.0", tkinter.END)
            self.TEXT_o_sct.insert(tkinter.INSERT, "".join([chr(i) for i in hilfsfunktionen.BitToInt(self.texts["o"])]))
            self.TEXT_o_sct.configure(state="disabled")
        elif what == "e":
            self.texts["o"] = self.texts["e"]
            self.TEXT_o_sct.configure(state="normal")
            self.TEXT_o_sct.delete("1.0", tkinter.END)
            self.TEXT_o_sct.insert(tkinter.INSERT, "".join([chr(i) for i in hilfsfunktionen.BitToInt(self.texts["o"])]))
            self.TEXT_o_sct.configure(state="disabled")

if __name__ == "__main__":
    g = GUI(debug=False)
