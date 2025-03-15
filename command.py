class Command(object):

    @staticmethod
    def get_str_from_dict(origin):
        all=[]
        for k,v in origin.items():
            kv=f"{k}={v}"
            all.append(kv)
        return ','.join(all)

    
    def __init__(self, p=1, **kwargs):
        all=[]
        for k,v in kwargs.items():
            kv=f"{k}={v}"
            all.append(kv)
        self.header="JOB\nDEF "+Command.get_str_from_dict(kwargs)+"\nSTART\n\n"
        self.footer=f"QTY P={p}\nEND\nJOBE\n"

    @staticmethod
    def get_font(**kwargs):
        if kwargs:
            cfg=Command.get_str_from_dict(kwargs)
            return f"FONT {cfg}"
        else:
            return f"FONT TP=103,WD=30,LG=30,LS=5,BO=0"
        
    @staticmethod
    def get_loc(y,x=40,l=1):
        return f"TEXT X={x},Y={y},L={l}"
    
    @staticmethod
    def write(text,title=None):
        if title:
            return f"{title}：{text}"
        return text
    
    @staticmethod
    def get_rfid(value,md=2,l=1,len=10):
        return f"RFID MD={md},L={l},LEN={len}\n{value}\n\n"
    
    @staticmethod
    def get_QR(value,**kwargs):
        cfg=Command.get_str_from_dict(kwargs)
        return f"QR {cfg}\n{value}\n\n"
    
    def simple_content(self,**kwargs)->str:
        """生成打印的内容，包括打印设置，带两回车。不设定编码。
        
        Keyword arguments:
        argument -- 参数设定为字典的形式，如coord的元组(x,y)，标签的可选标题title及内容text等
        Return: str, 返回打印的内容，包括设置字体、打印位置及打印的文字
        """
        
        return f"{self.get_font()}\n{self.get_loc(x=kwargs["coord"][0],y=kwargs["coord"][1])}\n{self.write(title=kwargs.get("title"),text=kwargs['text'])}\n\n"