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


class PaceCircles():
    def __init__(self,ReadDataFile):
        self.ReadDataFile = ReadDataFile
        self.ShuffleDict = self.RandomizeOrder(self.ReadDataFile.CounterDict)
        #self.CirclePositions = [0,30,60,90,120,150,180,210,240,270,300,330]
        self.CirclePositions = list(range(0,360,10))
        self.PlaceDatacircles(self.ShuffleDict)
        

    def GetDistance(self,p1,p2):
        x1=p1[0]
        y1=p1[1]
        x2=p2[0]
        y2 = p2[1]
        xD = abs(x1-x2)**2
        yD = abs(y1-y2)**2
        dist = math.sqrt((xD+yD))
        return dist
    
    
    
    def RandomizeOrder(self, ShuffleDict):
        l = list(ShuffleDict)
        m = l[0]
        l.pop(0)
        random.shuffle(l)
        NewD=dict()
        l = [m]+l
        for k in l:
            NewD[k]=ShuffleDict[k]
        return NewD


    
    
    def CalcCirclePositions(self,radius):
        newP=[]
        newPP=[]
        for PlacedGene in self.coords:

            PlacedGeneX = PlacedGene[2][0]
            PlacedGeneY = PlacedGene[2][1]
            PlacedGeneWidth = PlacedGene[1]
            for grad in self.CirclePositions:
                x = round(float(radius*np.cos(grad) + PlacedGeneX),1)
                y = round(float(radius*np.sin(grad) + PlacedGeneY),1)
                newP.append((x,y))
                
                xx = round(float((radius+PlacedGeneWidth)*np.cos(grad) + PlacedGeneX),1)
                yy = round(float((radius+PlacedGeneWidth)*np.sin(grad) + PlacedGeneY),1)
                newPP.append((xx,yy))
        return newP,newPP
    
    def CalcDistanceToCenter(self,radius):
        dist=[]
        CenterGene = self.coords[0]
        for p in self.OuterPositions:
            dd = []
            toclose=0
            if p=='':
                dist.append(0)
                continue
            distance = self.GetDistance(p,CenterGene[2])
            if distance<(radius+CenterGene[1]):
                toclose=1
            else:
                dd.append(self.GetDistance(p,CenterGene[2]))
                    
            if toclose==0:
                dist.append(dd)
            else:
                dist.append(0)
                
        return dist
        
        
    def CalcOverlapWithOtherCircles(self,radius):
        AvailablePositions = [x for x in self.OuterPositions]
        for PlacedGene in self.coords[1:]:
            for n,p in enumerate(AvailablePositions):
                if p == '':
                    continue
                distance = self.GetDistance(p,PlacedGene[2])
                
                if distance<(radius+PlacedGene[1]):
                    AvailablePositions[n] = ''
        return AvailablePositions
        
    def ChooseCirclePositions(self,radius,CatVal):
        smallest = ''
        for pos,posOnCirc,distance in zip(self.AvailablePositions,self.InnerPositions,self.dist):
            if distance==0:
                continue
            if pos =='':
                continue
            total = sum(distance)
            if smallest == '' and posOnCirc not in self.takenPlaces:
                returnP = [(CatVal,radius,(pos),(posOnCirc))]
                smallest = total
                continue
            if smallest=='':
                continue
            
            
            if total <= smallest and posOnCirc not in self.takenPlaces:
                if total<smallest:
                    returnP = [(CatVal,radius,(pos),(posOnCirc))]
                else:
                    returnP.append((CatVal,radius,(pos),(posOnCirc)))
            else:
                continue
            
        returnP = random.choice(returnP) 
        return returnP
        
        
    def PlaceDatacircles(self, DictToPlace):
        self.coords = []
        counter = 0
        self.InnerPositions = []
        self.OuterPositions = []

        for CatVal,radius in tqdm(DictToPlace.items(),total=len(DictToPlace)):
            
            radius=math.sqrt(radius/np.pi)
            if self.coords==[]:
                self.coords.append((CatVal,radius,(0,0),(0,0)))
                counter=counter+1
            else:
                self.takenPlaces = set([x[3] for x in self.coords])
                self.InnerPositions,self.OuterPositions = self.CalcCirclePositions(radius)
                #self.InnerPositions = self.InnerPositions + newP
                #self.OuterPositions = self.OuterPositions + newPP
                self.dist = self.CalcDistanceToCenter(radius)
                self.AvailablePositions =  self.CalcOverlapWithOtherCircles(radius)
                
                smallest = ''
                hits = []
                
                CiclePosition = self.ChooseCirclePositions(radius,CatVal)
                self.coords.append(CiclePosition)
                counter = counter + 1

            
                    
            
        
        
            
            
