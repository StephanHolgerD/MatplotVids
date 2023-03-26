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



def PlotCircles(SizeDict,CoordDict,title,colDict,ax,maxW):
    for k,v in SizeDict.items():
        radius=math.sqrt(v/np.pi)
        x = CoordDict[k][0]
        y = CoordDict[k][1]
        circle1 = plt.Circle((x, y), radius,color=colDict[k],zorder=0)
        ax.add_patch(circle1)
        ax.text(CoordDict[k][0], CoordDict[k][1],k,ha='center',va='center',fontsize=((4*radius)),zorder=1,weight='bold')
    ax.set(xlim=((-1*maxW),maxW),ylim=((-1*maxW),maxW))
    ax.axis('off')
    #plt.subplots_adjust(top=1,bottom=0,left=0,right=1)
    #ax.set_title(title, y=1.0, pad=-14)
    #ax.set(title=title)
    ax.set_title(title, loc='left')
    #plt.savefig(name,facecolor='lavenderblush',dpi=150)
    #plt.close()
    #return ax
    
def randomColor():
 #   return 'red'
    return (np.random.randint(100,255)/255,np.random.randint(100,255)/255,np.random.randint(100,255)/255)