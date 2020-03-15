
import random

def random_color(mode='rgb',r=None,g=None,b=None):
    """获取随机颜色"""
    mode = mode.lower()
    if mode == 'hex':
        value = list(range(10))
        value.extend(['A','B','C','D','E','F'])
        color = '#'
        for i in range(6): color += str(random.choice(value))
    elif mode == 'rgb':
        if r is None: r = random.randint(50, 200)
        if g is None: g = random.randint(50,200)
        if b is None : b = random.randint(50,200)
        color = 'rgb({},{},{})'.format(r,g,b)

    elif mode == 'background':
        r = random.randint(140, 255)
        g = random.randint(140,255)
        b = random.randint(140,255)
        color = 'rgb({},{},{})'.format(r, g, b)

    elif mode == 'font':
        r = random.randint(0, 100)
        g = random.randint(0,100)
        b = random.randint(0,100)
        color = 'rgb({},{},{})'.format(r,g,b)

    else: raise TypeError("invalid parameter {}".format(mode))

    return color

def get_css():
    color = []
    for i in range(6):
        color.extend([random_color("font"), random_color("background")])
    color = tuple(color)
    # print(color)

    SHEET_SCREEN = """
    *{color:%s; background-color:%s;height:30px; border:0}
    
    QPushButton{color:%s; background-color:%s; border:0; height:30px; width:60px}
    QPushButton:hover{color:%s;background-color:%s;}

    QPushButton:pressed{color:%s;background-color:%s;}
    
    
    QLinEdit,QLabel{color:%s; background-color:%s;height:30px; border:0}
    
    QComboBox,QComboBox QAbstractItemView {
        border: 0;
        selection-background-color: %s;
        background-color:%s;
        font:YaHei 30px;
        }
    
    
    """ % color
    return SHEET_SCREEN
#QAbstractItemView