from enum import Enum
import os

from tag import Tag

class Template():

    def __init__(self,p=1):
        self.header="JOB\nDEF MD=5,TR=1,DR=1,DK=10,SP=3,MO=0,PW=840,PH=360,MK=2,PG=32,LM=0,RM=0,TM=0,BM=0,GM=1\nSTART\n\n"
        self.footer=f"QTY P={p}\nEND\nJOBE\n"

    @staticmethod
    def get_content(cls=None,**kwargs):
        """文本打印
        
        关键字参数:
        WD -- 字符宽，16<=WD<=256，硬件默认32
        LG -- 字符高，16<=LG<=256，硬件默认32
        text -- 欲打印的文本
        X -- 文本横坐标，0<=X<=1100，硬件默认0
        Y -- 文本纵坐标，0<=Y<=标签最大高度，硬件默认0

        Return: str, 返回字符串的打印文本指令
        """
        wd=kwargs.get("WD",32)
        lg=kwargs.get("LG",32)
        x=kwargs.get("X",cls.START_POINT.value[0] if cls else 90)
        y=kwargs.get("Y",cls.START_POINT.value[1] if cls else 10)
        text=kwargs.get("text","")
        if len(text)<=32*1024:
            content=f"""FONT TP=103,WD={wd},LG={lg},LS=5,BO=0\nTEXT X={x},Y={y}\n{text}\n\n
            """
            return content
        raise MemoryError("整个文本不能超过 32K 字节。The whole text is no more than 32k bytes.")

    @staticmethod
    def get_rfid(rfid):
        content=f"""RFID MD=2,LEN={int(len(rfid)/2)}\n{rfid}\n\n"""
        return content

    @staticmethod
    def get_qr(qr,x=0,y=0):
        """打印二维码
        
        关键字参数:
        qr -- 二维码的值
        x -- 二维码横坐标，0<=x<=100，硬件默认0
        y -- 二维码纵坐标，0<=y<=标签最大高度，硬件默认0

        Return: str, 返回字符串的打印二维码指令
        """
        
        content=f"""QR X={x},Y={y}\n{qr}\n\n"""
        return content

    def get_simple(self,text):
        return f"{self.header}{Template.get_content(text=text)}{self.footer}"
    
    @staticmethod
    def interpret(cmd:str):
        if os.name =='nt':
            return cmd.encode('ansi')
        else:
            return cmd.encode('gtk')
    
    @staticmethod
    def make_txt(cmd:str,filename:str):
        with open(f"commands/{str}.txt",encoding='utf-8') as f:
            f.write(cmd)