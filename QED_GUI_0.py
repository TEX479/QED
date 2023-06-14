import tkinter
from tkinter import scrolledtext
from tkinter.filedialog import askopenfilename, asksaveasfilename
import time
import math
from PIL import Image as PILImage
from PIL import ImageTk as PILImageTk


def save_file(text):
    """Save the 'text' as a new file."""

    filepath = asksaveasfilename(
        defaultextension=".dat",
        filetypes=[("normal Files", "*.dat"), ("All Files", "*.*")],
        )
    if not filepath:
        return
    with open(filepath, mode="wb") as f:
        print(type(text))
        #pickle.dump(obj = text, file=f)
        f.write(bytes(str(text)))

def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("normal Files", "*.dat"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, mode="r") as f:
        #text = pickle.load(file=f)
        text = ""
        fr = f.read()
        lengths = []
        for i in fr:
            lengths.append(math.ceil((len(bin(ord(i)))-2)/8)*8)
            text += "0"*((math.ceil((len(bin(ord(i)))-2)/8)*8+2)-len(bin(ord(i)))) + bin(ord(i))[2:]
        return text, filepath, lengths


class GUI():
    def __init__(self, texts = {"o": "", "p": "", "l": "", "v": "", "e": ""}, chunk = 16, KEY = ["","",""]) -> None:
        self.texts = texts
        self.KEY = KEY
        self.chunk = chunk

        self.create_gui()
        #way : True -> Ent; False -> Ver

    def create_gui(self):
        self.main_window = tkinter.Tk()
        self.main_window.title("\"QED\" : version: 4.1")
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

        self.o_btns = tkinter.Frame(master=self.main_window)
        self.o_btns.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

        self.not_btns = tkinter.Frame(master=self.main_window)
        self.not_btns.grid(row=2, column=1, padx=5, pady=5, sticky="nw")

        """CONTROL"""
        self.ver_btn = tkinter.Button(master=self.top_btns, background = "#ffffff", fg = "#000000", text="Verarbeiten", command=self.start)
        self.ver_btn.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.swap_image = PILImageTk.PhotoImage(PILImage.open("C:\\Users\\Butzel2020\\Documents\\Ich\\keep out\\do not enter\\fertig\\QED\\25274.png").resize((30,30),PILImage.Resampling.LANCZOS))
        self.swap_btn = tkinter.Button(master=self.top_btns, background = "#ffffff", fg = "#000000",image = self.swap_image, command=self.swap_bin_chr)
        self.swap_btn.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.swap_lbl_b = True
        self.swap_lbl = tkinter.Label(master=self.top_btns, background = "#ffffff", fg = "#000000", text="Anzeige: Bits")
        self.swap_lbl.grid(row=0, column=3, padx=5, pady=5, sticky="nw")

        """KEY"""
        self.key_lbl = tkinter.Label(master=self.key_btns, background = "#ffffff", fg = "#000000", text="Schlüssel: ")
        self.key_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.key_btn = tkinter.Button(master=self.key_btns, background = "#ffffff", fg = "#000000", text="Schlüssel-Datei öffnen", command=lambda: self.open_file_f("k"))
        self.key_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        self.key_lbl = tkinter.Label(master=self.key_btns, background = "#ffffff", fg = "#000000", text=self.KEY[1])
        self.key_lbl.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.key_btn = tkinter.Button(master=self.key_btns, background = "#ffffff", fg = "#000000", text="X", command=lambda: self.delete_file_f("k"))
        self.key_btn.grid(row=0, column=3, padx=5, pady=5, sticky="nw")
        self.key_sct = scrolledtext.ScrolledText(master=self.not_btns, wrap="word", background = "#ffffff", fg = "#000000", height=12)
        self.key_sct.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        """ORIGINAL"""
        self.TEXT_o_lbl = tkinter.Label(master=self.o_btns, background = "#ffffff", fg = "#000000", text="Bitte Text eingeben:")
        self.TEXT_o_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.TEXT_o_btn_o = tkinter.Button(master=self.o_btns, background = "#ffffff", fg = "#000000", text="Textdatei öffnen", command=lambda: self.open_file_f("o"))
        self.TEXT_o_btn_o.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        self.TEXT_o_lbl_p = tkinter.Label(master=self.o_btns, background = "#ffffff", fg = "#000000", text=self.texts["l"])
        self.TEXT_o_lbl_p.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.TEXT_o_btn_x = tkinter.Button(master=self.o_btns, background = "#ffffff", fg = "#000000", text="X", command=lambda: self.delete_file_f("o"))
        self.TEXT_o_btn_x.grid(row=0, column=3, padx=5, pady=5, sticky="nw")
        self.TEXT_o_sct = scrolledtext.ScrolledText(master=self.main_window, wrap="word", background = "#ffffff", fg = "#000000")
        self.TEXT_o_sct.grid(row=2, column=0, padx=5, pady=5, sticky="nw", columnspan=2)

        """INFO"""
        self.info_lbl = tkinter.Label(master=self.not_btns, background = "#ffffff", fg = "#000000", text="Infos:")
        self.info_lbl.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.info_sct = scrolledtext.ScrolledText(master=self.not_btns, wrap="word", background = "#ffffff", fg = "#000000", state="disabled", height=8)
        self.info_sct.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        """ENT"""
        self.TEXT_e_lbl = tkinter.Label(master=self.ent_btns, background = "#ffffff", fg = "#000000", text="Entschlüsselter Text:")
        self.TEXT_e_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.use_as_input_e_btn = tkinter.Button(master=self.ent_btns, background = "#ffffff", fg = "#000000", text="<als Eingabe verwenden>", command=lambda:self.use_as_input("e"))
        self.use_as_input_e_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        self.save_e_btn = tkinter.Button(master=self.ent_btns, background = "#ffffff", fg = "#000000", text="in Datei speichern", command=lambda:save_file(BitToStr(self.texts["e"])))
        self.save_e_btn.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.TEXT_e_sct = scrolledtext.ScrolledText(master=self.main_window, wrap="word", background = "#ffffff", fg = "#000000", state="disabled")
        self.TEXT_e_sct.grid(row=4, column=0, padx=5, pady=5, sticky="nw")

        """VER"""
        self.TEXT_v_lbl = tkinter.Label(master=self.ver_btns, background = "#ffffff", fg = "#000000", text="Verschlüsselter Text:")
        self.TEXT_v_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.use_as_input_v_btn = tkinter.Button(master=self.ver_btns, background = "#ffffff", fg = "#000000", text="<als Eingabe verwenden>", command=lambda:self.use_as_input("v"))
        self.use_as_input_v_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        self.save_v_btn = tkinter.Button(master=self.ver_btns, background = "#ffffff", fg = "#000000", text="in Datei speichern", command=lambda:save_file(BitToStr(self.texts["v"])))
        self.save_v_btn.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.TEXT_v_sct = scrolledtext.ScrolledText(master=self.main_window, wrap="word", background = "#ffffff", fg = "#000000", state="disabled")
        self.TEXT_v_sct.grid(row=4, column=1, padx=5, pady=5, sticky="ne")


        self.main_window.mainloop()

    def swap_bin_chr(self):
        if self.swap_lbl_b:
            self.swap_lbl.destroy()
            self.swap_lbl = tkinter.Label(master=self.top_btns, background = "#ffffff", fg = "#000000", text="Anzeige: Zeichen")
            self.swap_lbl.grid(row=0, column=3, padx=5, pady=5, sticky="nw")
            self.swap_lbl_b = False
            try:
                self.TEXT_o_sct.configure(state="normal")
                self.TEXT_o_sct.delete("1.0", tkinter.END)
                self.TEXT_o_sct.insert(tkinter.INSERT, BitToStr(self.texts["o"], self.texts["l"]))

                self.TEXT_v_sct.delete("1.0", tkinter.END)
                self.TEXT_v_sct.insert(tkinter.INSERT, BitToStr(self.texts["v"], self.texts["l"]))

                self.TEXT_e_sct.delete("1.0", tkinter.END)
                self.TEXT_e_sct.insert(tkinter.INSERT, BitToStr(self.texts["e"], self.texts["l"]))
            except Exception as e:
                print(e)
        else:
            self.swap_lbl.destroy()
            self.swap_lbl = tkinter.Label(master=self.top_btns, background = "#ffffff", fg = "#000000", text="Anzeige: Bits")
            self.swap_lbl.grid(row=0, column=3, padx=5, pady=5, sticky="nw")
            self.swap_lbl_b = True

            try:
                self.TEXT_o_sct.delete("1.0", tkinter.END)
                self.TEXT_o_sct.insert(tkinter.INSERT, self.texts["o"])
                self.TEXT_o_sct.configure(state="disabled")

                self.TEXT_v_sct.delete("1.0", tkinter.END)
                self.TEXT_v_sct.insert(tkinter.INSERT, self.texts["v"])

                self.TEXT_e_sct.delete("1.0", tkinter.END)
                self.TEXT_e_sct.insert(tkinter.INSERT, self.texts["e"])
            except Exception as e:
                print(e)

    def start(self):
        if not(self.swap_lbl_b):
            self.texts["o"], self.texts["l"] = StrToBit((self.TEXT_o_sct.get("1.0", tkinter.END))[:-1])
        else:
            self.texts["o"] = (self.TEXT_o_sct.get("1.0", tkinter.END))[:-1]
        self.texts["v"] = self.texts["o"]
        self.texts["e"] = self.texts["o"]




    def open_file_f(self, w=None):
        if w == "k":
            self.KEY[0], self.KEY[1], self.KEY[2] = open_file()
            self.key_sct.configure(state="normal")
            self.key_sct.delete("1.0", tkinter.END)
            self.key_sct.insert(tkinter.INSERT, str(self.KEY[0]))
            self.key_lbl.configure(text=str(self.KEY[1]))
            self.key_sct.configure(state="disabled")
        else:
            self.texts["o"], self.texts["p"], self.texts["l"] = open_file()
            self.TEXT_o_sct.configure(state="normal")
            self.TEXT_o_sct.delete("1.0", tkinter.END)
            self.TEXT_o_sct.insert(tkinter.INSERT, str(self.texts["o"]))
            self.TEXT_o_sct.configure(state="disabled")
            self.TEXT_o_lbl_p.configure(text=str(self.texts["p"]))

    def delete_file_f(self, w=None):
        if w == "k":
            self.KEY[0], self.KEY[1], self.KEY[2] = "", "", ""
            self.key_sct.configure(state="normal")
            self.key_sct.delete("1.0",tkinter.END)
            self.key_lbl.configure(text=str(self.KEY[1]))
        else:
            self.texts["o"], self.texts["p"], self.texts["l"] = "", "", ""
            self.TEXT_o_sct.delete("1.0",tkinter.END)
            self.TEXT_o_lbl_p.configure(text=str(self.texts["p"]))


    def use_as_input(self, what):
        if what == "v":
            self.TEXT_o_sct.delete("1.0", tkinter.END)
            if self.swap_bin_chr: self.TEXT_o_sct.insert(tkinter.INSERT, self.TEXT_v_sct.get("1.0", tkinter.END))
            else: self.TEXT_o_sct.insert(tkinter.INSERT, self.StrToBit(self.TEXT_v_sct.get("1.0", tkinter.END)))
            self.start()
        elif what == "e":
            self.TEXT_o_sct.delete("1.0", tkinter.END)
            if self.swap_bin_chr: self.TEXT_o_sct.insert(tkinter.INSERT, self.TEXT_e_sct.get("1.0", tkinter.END))
            else: self.TEXT_o_sct.insert(tkinter.INSERT, self.StrToBit(self.TEXT_e_sct.get("1.0", tkinter.END)))
            self.start()
        else:
            self.info_log += f"code: use_as_input; with: {what}; at: {time.asctime()}\n"

    def print_info(self,text,info):
        self.info_sct.configure(state="normal")
        self.info_sct.insert(tkinter.INSERT, str(text))
        self.info_sct.configure(state="disabled")
        print(str(text),"\nINFO CODE:", info)


"""
xor bit:

x = "10101010"
y = "01010101"
z = bin(int(x,2)^int(y,2))[2:]


with open(<name>, "rb") as f:
    test_content = f.read()

test_content_arr = []
for i in test_content:
    test_content_arr.append(i)
print(test_content_arr)

test2_content = bytes(test_content_arr)
with open(<name>, "wb") as f:
    f.write(test2_content)
"""
class fehler(ValueError): ...