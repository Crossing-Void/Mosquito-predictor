from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


class Extreme1D:
    plt.rcParams['figure.dpi'] = 150

    def __init__(self, app) -> None:
        self.app = app

    def __calculate(self, csv_name):
        df = pd.read_csv(csv_name)
        x = np.linspace(1, 7, 7)
        y = df[self.app.select_model.get()]
        plt.scatter(x, y, color='blue', label="station")

        f = CubicSpline(x, y)
        x1 = np.linspace(1, 7, 60002)
        func = f(x1)
        slope = np.zeros(60000)

        for i in range(1, len(func)-1):
            slope[i-1] = abs(func[i+1]-func[i-1])/(x1[i+1]-x1[i-1])

        rank = []
        for j in range(6):
            interval = slope[j*10000:(j+1)*10000]
            ext = np.argsort(interval)+1
            opt = ext[0]+10000*j
            rank.append(opt)

        rank = np.insert(rank, 0, 0)
        rank = np.insert(rank, 6, -1)
        plt.plot(x1, f(x1))
        plt.xlabel("Day")
        plt.ylabel("Mosquito Index")
        plt.scatter(x1[rank], f(x1[rank]), color='red', label="optimization")
        maxvalue = np.max(f(x1[rank]))
        minvalue = np.min(f(x1[rank]))

        plt.legend()
        plt.savefig(os.path.join(
            self.path, f'ploting-1D({self.app.select_model.get()})', self.app.delete_extension(
                os.path.split(csv_name)[-1])+'.png'))
        plt.clf()
        return maxvalue, minvalue

    def ploting_all_st(self):
        '''
        all station will have single img for a week change
        '''
        self.path = os.path.join(
            self.app.datas, 'combines', f'{self.app.select_area.get()}from{self.app.select_date.get()}')

        if not os.path.exists(os.path.join(self.path, f'ploting-1D({self.app.select_model.get()})')):
            os.mkdir(os.path.join(
                self.path, f'ploting-1D({self.app.select_model.get()})'))

        fileList = [_ for _ in os.listdir(self.path) if os.path.splitext(
            os.path.join(self.path, _))[-1] == '.csv']

        df = pd.DataFrame(pd.np.empty((len(fileList), 3)))
        index = [self.app.delete_extension(fileName) for fileName in fileList]
        df.columns = ["station", "minT", "maxT"]
        df['station'] = index

        minT, maxT = [], []

        for csvfile in fileList:
            max, min = self.__calculate(os.path.join(self.path, csvfile))
            minT.append(min)
            maxT.append(max)

        df['minT'] = minT
        df['maxT'] = maxT
        df.to_csv(os.path.join(
            self.path, f'ploting-1D({self.app.select_model.get()})', 'all.csv'), index=False)
