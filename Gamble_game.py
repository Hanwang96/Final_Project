import pandas as pd
import numpy as np
import collections
import pandas as pd
from numpy.linalg import cholesky
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import truncnorm
from scipy.stats import norm
from random import uniform
import threading as thd
import time
import datetime
import pylab
# df = pd.DataFrame({'a':[1,2,3],'b':[1,2,3]})
# df['a'] += 1
# print(df)


x = np.linspace(0, 6000, 1200)

y = np.sin(x)
a = plt.figure()
a = plt.plot(x,y)
a.show()
# plt.savefig("easyplot.jpg")