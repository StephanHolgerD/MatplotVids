import pandas as pd
import matplotlib.pyplot as plt
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



class FigureScheduler():
    def __init__(self,df,CatColumn = '',MinAppearance = 5,ResolutionFactor= 10,TimeCol = 'submissiondate',GroupingFreq='2W'):
        self.df = df      
        self.CatColumn = CatColumn  
        self.MinAppearance = MinAppearance 
        self.ResolutionFactor = ResolutionFactor
        self.TimeCol = TimeCol
        self.GroupingFreq = GroupingFreq
        self.FilterAppearances()
        self.CalcCounts()


    def FilterAppearances(self):
        TotalCount=Counter(self.df[self.CatColumn])
        self.OverThreshold = set([k for k,v in TotalCount.items() if v >= self.MinAppearance])
        self.df = self.df[self.df[self.CatColumn].isin(self.OverThreshold)]

    
    def CalcCounts(self):
        FrameCatCountDict = {k:0 for k in self.OverThreshold}
        FrameDict = {}
        TimeArray = []
        FrameCounter = 0
        for date,lines in self.df.groupby(pd.Grouper(level=self.TimeCol, freq=self.GroupingFreq)):
            if lines.empty:
                continue

            ChunkLen = len(lines)
            NumberOfFrames = ChunkLen*self.ResolutionFactor
            CatCounts=Counter(lines[self.CatColumn])
            CatFactor = {}
            for k,v in CatCounts.items():
                fac = v/NumberOfFrames
                CatFactor[k] = fac
            
            CountD = {}
            for frame in range(NumberOfFrames):
                frameD = {}
                for k,v in CatFactor.items():
                    FrameCatCountDict[k] = FrameCatCountDict[k] + v
                for k,v in FrameCatCountDict.items():
                    frameD[k]=v

                
                
                TimeArray.append(date)
                FrameDict[FrameCounter]=frameD
                
                FrameCounter = FrameCounter + 1                    
        self.FramePlotDict = FrameDict
        self.TimeArray = TimeArray
    
    