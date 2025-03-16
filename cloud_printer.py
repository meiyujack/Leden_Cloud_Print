import socket, time
import subprocess

from tkinter import Tk, ttk
import tkinter
from tkinter import messagebox


class App(Tk):

    def __init__(self):
        super().__init__()
        self.iconbitmap("favicon.ico")
        self.title("LEDEN云打印0.2")
        self.geometry("300x200+650+207")
        self.resizable(0, 0)
        frm = ttk.Frame(self)
        self.titleVar = tkinter.StringVar()
        self.textVar = tkinter.StringVar()
        self.qrVar = tkinter.StringVar()
        frm.grid()
        tlbl = ttk.Label(self, text="电子标签标题：", style="myMiddle.TLabel")
        tlbl.grid(column=0, row=0, sticky="W", padx=20, pady=(10, 0))
        ttext = ttk.Entry(self, width=12, textvariable=self.titleVar)
        ttext.grid(column=1, row=0, sticky="W", pady=(6, 0))

        clbl = ttk.Label(self, text="内容：", style="myMiddle.TLabel")
        clbl.grid(column=0, row=1, sticky="E", padx=20, pady=(10, 0))
        text = ttk.Entry(self, width=16, textvariable=self.textVar)
        text.grid(column=1, row=1, sticky="W", pady=(6, 0))

        qr = ttk.Label(self, text="二维码：", style="myMiddle.TLabel")
        qr.grid(column=0, row=2, sticky="E", padx=20, pady=(10, 0))
        qrValue = ttk.Entry(self, width=12, textvariable=self.qrVar)
        qrValue.grid(column=1, row=2, sticky="W", pady=(6, 0))

        button = ttk.Button(self,
                            text="云打印",
                            width=7,
                            padding=2,
                            command=self.cloud_print,
                            style="TButton")
        button.grid(column=1, row=3, sticky="NW", pady=25)

        style = ttk.Style()
        style.configure("myMiddle.TLabel", font=("微软雅黑", 13))
        style.configure("TButton",
                        font=("微软雅黑", 18, "bold"),
                        foreground="orange",
                        background="blue")

        ttext.focus_set()
        qrValue.bind("<Return>", lambda x: self.cloud_print())

        self.process = subprocess.Popen(
            ["frp/frpc.exe", '-c', 'frp/frpc.toml'])

    def send_print_job(self, cmd, printer_ip="40.90.232.31", port=6000):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((printer_ip, port))
                s.sendall(cmd.encode("ansi"))
                print(
                    f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {self.titleVar.get()}打印任务已发送"
                )
            except Exception as e:
                print(f"发送打印任务失败：{e}")

    @staticmethod
    def generate_cmd(title="", content="", qr=""):
        return f"JOB\nDEF MD=5,TR=1,DR=1,DK=10,SP=3,MO=0,PW=840,PH=360,MK=2,PG=32,DR=1,LM=0,RM=0,TM=0,BM=0,GM=1\nSTART\n\nFONT TP=103,WD=40,LG=40,LS=5,BO=0\nTEXT X=200,Y=10,L=1\n{title}\n\nFONT TP=103,WD=30,LG=30,LS=5,BO=0\nTEXT X=120,Y=60,L=1\n{content}\n\nRFID MD=2,L=1,LEN=10\n43413132303036383230\n\nQR X=460,Y=120,CV=9,CS=8\n{qr}\n\nQTY P=1\nEND\nJOBE\n"

    def cloud_print(self):
        self.send_print_job(
            App.generate_cmd(self.titleVar.get(), self.textVar.get(),
                             self.qrVar.get()))

    def on_closing(self):
        if messagebox.askokcancel("退出", "你确定要退出吗？"):
            self.quit()
            self.process.terminate()
            self.destroy()


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
