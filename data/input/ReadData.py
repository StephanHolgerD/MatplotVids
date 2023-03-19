import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
plt.style.use('bmh')
import numpy as np
from bokeh.palettes import Accent
import pandas as pd
from collections import Counter
import numpy as np
from tqdm import tqdm
import math
import random
import ffmpeg
from glob import glob


class ReadDataFile():
    def __init__(self,df,CatColumn = '',MinAppearance = 5):
        self.df = df      
        self.CatColumn = CatColumn  
        self.MinAppearance = MinAppearance 
    
    def CreateCounterDict(self):
        self.CounterDict = Counter(self.df[self.CatColumn])
        self.CounterDict = {k:v for k,v in self.CounterDict.items() if v >= self.MinAppearance}
        self.CounterDict=dict(sorted(self.CounterDict.items(), key=lambda item: item[1],reverse=True))
    
        