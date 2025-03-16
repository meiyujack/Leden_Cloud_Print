import socket, time
import uuid, random
import subprocess

from tkinter import Tk, ttk
import tkinter
from tkinter import messagebox

from template import Template


class App(Tk):

    def __init__(self):
        super().__init__()
        self.iconbitmap("favicon.ico")
        self.title("LEDEN云打印0.6")
        self.geometry("500x300+650+207")
        self.resizable(0, 0)
        frm = ttk.Frame(self)
        self.titleVar = tkinter.StringVar()
        self.textVar = tkinter.StringVar()
        self.text2Var = tkinter.StringVar()
        self.text3Var = tkinter.StringVar()
        self.text4Var = tkinter.StringVar()
        self.comboVar = tkinter.StringVar()
        self.combo2Var = tkinter.IntVar()
        self.rfidVar = tkinter.StringVar()
        self.qrVar = tkinter.StringVar()
        frm.grid()
        title = ttk.Label(self, text="电子标签", style="myLarge.TLabel")
        title.grid(column=0,
                   row=0,
                   sticky="W",
                   pady=(10, 0),
                   padx=190,
                   columnspan=4)

        tlbl = ttk.Label(self, text="标题：", style="myMiddle.TLabel")
        tlbl.grid(column=0, row=1, sticky="E", pady=(10, 0))
        ttext = ttk.Entry(self, width=12, textvariable=self.titleVar)
        ttext.grid(column=1, row=1, sticky="W", pady=(10, 0))

        clbl = ttk.Label(self, text="内容1：", style="myMiddle.TLabel")
        clbl.grid(column=2, row=1, sticky="W", pady=(10, 0), padx=20)
        text = ttk.Entry(self, width=16, textvariable=self.textVar)
        text.grid(column=2, row=1, sticky="E", pady=(10, 0), padx=86)

        clbl2 = ttk.Label(self, text="内容2：", style="myMiddle.TLabel")
        clbl2.grid(column=0, row=2, sticky="E", pady=(10, 0))
        text2 = ttk.Entry(self, width=16, textvariable=self.text2Var)
        text2.grid(column=1, row=2, sticky="W", pady=(10, 0))

        clbl3 = ttk.Label(self, text="内容3：", style="myMiddle.TLabel")
        clbl3.grid(column=2, row=2, sticky="W", pady=(10, 0), padx=20)
        text3 = ttk.Entry(self, width=16, textvariable=self.text3Var)
        text3.grid(column=2, row=2, sticky="E", pady=(10, 0), padx=86)

        clbl4 = ttk.Label(self, text="内容4：", style="myMiddle.TLabel")
        clbl4.grid(column=0, row=3, sticky="E", pady=(10, 0))
        text4 = ttk.Entry(self, width=46, textvariable=self.text4Var)
        text4.grid(column=1, row=3, sticky="W", pady=(10, 0), columnspan=3)

        tlbl = ttk.Label(self, text="RFID类型：", style="myMiddle.TLabel")
        tlbl.grid(column=0, row=4, sticky="E", pady=(10, 0), padx=(52, 0))
        combo = ttk.Combobox(self, width=4, textvariable=self.comboVar)
        combo['values'] = ('数字', '字母', '混合')
        combo.grid(column=1, row=4, sticky="W", pady=(10, 0))
        combo.current(0)

        tlbl = ttk.Label(self, text="RFID位数：", style="myMiddle.TLabel")
        tlbl.grid(column=2, row=4, sticky="W", pady=(10, 0))
        combo2 = ttk.Combobox(self, width=2, textvariable=self.combo2Var)
        combo2['values'] = (8, 12, 16, 20, 24)
        combo2.grid(column=2,
                    row=4,
                    sticky="W",
                    padx=88,
                    pady=(10, 0),
                    columnspan=2)
        combo2.current(0)

        qr = ttk.Label(self, text="二维码：", style="myMiddle.TLabel")
        qr.grid(column=0, row=5, sticky="E", pady=(10, 0))
        qrValue = ttk.Entry(self, width=12, textvariable=self.qrVar)
        qrValue.grid(column=1, row=5, sticky="W", pady=(10, 0))

        button = ttk.Button(self,
                            text="云打印",
                            width=7,
                            padding=2,
                            command=self.cloud_print,
                            style="TButton")
        button.grid(row=6, sticky="ES", columnspan=3, padx=70)

        style = ttk.Style()
        style.configure("myMiddle.TLabel", font=("微软雅黑", 13))
        style.configure("myLarge.TLabel", font=("微软雅黑", 18))
        style.configure("TButton",
                        font=("微软雅黑", 16, "bold"),
                        foreground="orange",
                        background="blue")

        ttext.focus_set()
        qrValue.bind("<Return>", lambda x: self.cloud_print())

        self.process = subprocess.Popen(
            ["frp/frpc.exe", '-c', 'frp/frpc.toml'])

    @staticmethod
    def generate_unique(type: str, num: int):
        answer = ''
        uid = str(uuid.uuid4())
        while len(answer) != num:
            r = random.choice(uid)
            match type:
                case "混合":
                    if r.isalnum():
                        answer += r
            match type:
                case "数字":
                    if r.isdigit():
                        answer += r
            match type:
                case "字母":
                    if r.isalpha():
                        answer += r
        return answer

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

    def generate_cmd(self, title: str, content: list, rfid_type_num: tuple,
                     qr: str):
        my = Template()
        title = my.get_content(X=200, Y=10, WD=40, LG=40, text=title)
        text, text2, text3, text4 = content
        rfid = self.generate_unique(rfid_type_num[0], rfid_type_num[1])
        qr = my.get_qr(qr=qr, x=480, y=220)
        return f"{my.header}{title}{my.get_content(Y=60,text=text)}{my.get_content(Y=110,text=text2)}{my.get_content(Y=150,text=text3)}{my.get_content(Y=200,text=text4)}{my.get_rfid(rfid)}{qr}{my.footer}"

    def cloud_print(self):
        self.send_print_job(
            self.generate_cmd(self.titleVar.get(), [
                self.textVar.get(),
                self.text2Var.get(),
                self.text3Var.get(),
                self.text4Var.get()
            ], (self.comboVar.get(), self.combo2Var.get()), self.qrVar.get()))

    def on_closing(self):
        if messagebox.askokcancel("退出", "你确定要退出吗？"):
            self.quit()
            self.process.terminate()
            self.destroy()


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
