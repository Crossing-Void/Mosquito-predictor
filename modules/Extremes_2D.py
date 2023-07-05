from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.crs as crs
import cartopy.feature as cfeature
import matplotlib.tri as mtri
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import random
import datetime
import send2trash


class Extreme2D:
    plt.rcParams['figure.dpi'] = 150

    def __init__(self, app):
        self.app = app

    def __gradient_method(self, ex, ey):
        scatter_x = []
        scatter_y = []
        for i in range(900):
            ini_x = random.randint(20, 80)
            ini_y = random.randint(20, 80)
            flag = False
            xold = None
            yold = None
            for j in range(20):
                x_norm = np.ma.getdata(ex)[ini_x][ini_y]
                y_norm = np.ma.getdata(ey)[ini_x][ini_y]
                try:
                    x_norm = int(np.ceil(x_norm))
                    y_norm = int(np.ceil(y_norm))
                    xold = ini_x
                    yold = ini_y
                    ini_x = ini_x+x_norm
                    ini_y = ini_y+y_norm
                    if xold == ini_x and yold == ini_y:
                        scatter_x.append(xold)
                        scatter_y.append(yold)
                        flag = True
                        break
                except:
                    if xold != None and yold != None:
                        scatter_x.append(xold)
                        scatter_y.append(yold)
                    flag = True
                    break
            if flag != True:
                scatter_x.append(ini_x)
                scatter_y.append(ini_y)

        return scatter_x, scatter_y

    def __mos_tri(self, location, concentration, day):
        '''
        plot a day concentration (only one day!)
        '''
        lon = np.array(location[0])
        lat = np.array(location[1])
        maxLon, minLon = np.max(lon), np.min(lon)
        maxLat, minLat = np.max(lat), np.min(lat)
        scale = '10m'

        ax = plt.axes(projection=crs.PlateCarree())
        ax.add_feature(cfeature.LAND.with_scale(scale))
        ax.add_feature(cfeature.COASTLINE.with_scale(scale))
        ax.coastlines(scale)
        ax.add_feature(cfeature.OCEAN.with_scale(scale))
        ax.add_feature(cfeature.BORDERS.with_scale(scale), linestyle=':')
        ax.set_xticks(np.linspace(0, 180, 901))
        ax.set_yticks(np.linspace(0, 90, 451))
        lon_formatter = LongitudeFormatter()
        lat_formatter = LatitudeFormatter()
        ax.xaxis.set_major_formatter(lon_formatter)
        ax.yaxis.set_major_formatter(lat_formatter)

        xi, yi = np.meshgrid(np.linspace(minLon-0.05, maxLon+0.05, 100),
                             np.linspace(minLat-0.05, maxLat+0.05, 100))
        xu, yu = np.meshgrid(np.linspace(minLon-0.05, maxLon+0.05, 25),
                             np.linspace(minLat-0.05, maxLat+0.05, 25))

        mesh = mtri.Triangulation(lon, lat)
        f = mtri.CubicTriInterpolator(mesh, concentration, kind='geom')
        ex, ey = f.gradient(xi, yi)
        E_norm = np.sqrt(ex**2 + ey**2)
        zi_cubic_geom = f(xi, yi)

        maxpoint = np.max(zi_cubic_geom)
        maxposition = np.argwhere(zi_cubic_geom == maxpoint)
        minpoint = np.min(zi_cubic_geom)
        minposition = np.argwhere(zi_cubic_geom == minpoint)
        #print(maxpoint)
        dot1 = maxposition[0][0]
        dot2 = maxposition[0][1]
        dot3 = minposition[0][0]
        dot4 = minposition[0][1]

        level = np.arange(0, 1050, 50)

        ax = plt.triplot(mesh, marker="o", zorder=5,)
        ax = plt.contourf(xi, yi, zi_cubic_geom,
                          levels=level, cmap='jet', extend='both')
        levels = np.linspace(0, 1000, 21)
        ax = plt.colorbar(ticks=levels)
        '''
        # -_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_-
        (ex1, ey1) = f.gradient(xu, yu)
        E_norm1 = np.sqrt(ex1**2 + ey1**2)
        ax = plt.quiver(xu, yu, ex1/E_norm1, ey1/E_norm1, units='xy', scale=50., zorder=10, color="#111111",
                        width=0.002, headwidth=6., headlength=3., headaxislength=3)
        # -_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_--_Arrow_-
        '''
        scatter_x, scatter_y = self.__gradient_method(ex/E_norm, ey/E_norm)
        compare_number = zi_cubic_geom[scatter_x, scatter_y]
        #print(compare_number)
        position_for_gradient = np.argmax(compare_number)
        #print(position_for_gradient)
        self.maximumList.insert(0,zi_cubic_geom[scatter_x[position_for_gradient]][scatter_y[position_for_gradient]])
        #print(zi_cubic_geom[scatter_x[position_for_gradient]][scatter_y[position_for_gradient]])
        scatter_x[position_for_gradient], scatter_y[position_for_gradient]

        ax = plt.scatter(xi[scatter_x[position_for_gradient]][scatter_y[position_for_gradient]], yi[scatter_x[position_for_gradient]]
                         [scatter_y[position_for_gradient]], color='red', s=100, zorder=12, label="gradient")

        ax = plt.plot(xu, yu, 'k-', lw=0.5, alpha=0.5)
        ax = plt.plot(xu.T, yu.T, 'k-', lw=0.5, alpha=0.5)
        ax = plt.scatter(xi[dot1][dot2], yi[dot1][dot2], color='black',
                         s=200, label='maximum', marker="o", zorder=11)
        ax = plt.scatter(xi[dot3][dot4], yi[dot3][dot4], color='fuchsia',
                         s=200, label='minimum', marker="o", zorder=11)

        predictDate = datetime.date(*self.app.str_tuple_date_change(self.app.select_date.get())) + \
            datetime.timedelta(day)
        ax = plt.title(f'{self.app.str_tuple_date_change(predictDate)}')
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.065), ncol=3)

        plt.savefig(
            os.path.join(self.path, f'ploting-2D({self.app.select_model.get()})',
                         f'{self.app.select_area.get()}  {self.app.str_tuple_date_change(predictDate)}.png')
        )
        plt.clf()

    def ploting_week(self):
        '''
        plot a week (folder like 桃園市from2022-12-12), path(str)
        '''
        self.path = os.path.join(self.app.datas, 'combines',
                                 f'{self.app.select_area.get()}from{self.app.select_date.get()}')
        try:
            send2trash.send2trash(os.path.join(
                self.path, f'ploting-2D({self.app.select_model.get()})'))
        except:
            pass
        os.mkdir(os.path.join(
            self.path, f'ploting-2D({self.app.select_model.get()})'))

        allStInfo = self.app.pastdata.areaStationsList[self.app.select_area.get(
        )]
        location = [(data['stLon'], data['stLat'])
                    for data in allStInfo.values()]
        location = list(zip(*location))

        for day in range(7):  # 0 stand for day7, 6 stand for day1, day1 is current day!!
            day_data = np.zeros(0)
            for file in os.listdir(self.path):
                if not os.path.isdir(temp := (os.path.join(self.path, file))):
                    df = pd.read_csv(temp)
                    add = df[self.app.select_model.get()][day]
                    day_data = np.append(day_data, add)

            self.__mos_tri(location, day_data, (6-day))
