import numpy as np
import pandas as pd
import os
import datetime


class Combine:
    def __init__(self, app) -> None:
        self.app = app

        if not os.path.exists(os.path.join(self.app.datas, 'combines')):
            os.mkdir(os.path.join('datas', 'combines'))

        self.path = os.path.join('datas', 'combines')

    def __missing_value(self, df):
        '''
        passing an excel or csv station data  -> produce tuple(total rain, meanT, maxT, minT)

        '''
        # --- temp ---
        for i in range(23):
            if i != 0 and df['T'][i] == str('/'):
                df['T'][i] = df['T'][i-1]
            elif df['T'][i] == str('/'):
                df['T'][i] = df['T'][i+1]
        for i in range(23, 0, -1):
            if i != 23 and df['T'][i] == str('/'):
                df['T'][i] = df['T'][i+1]
            elif df['T'][i] == str('/'):
                df['T'][i] = df['T'][i-1]
        try:
            temparature = np.array(df['T'], dtype='float')
        except:
            total = 0
            num = 0
            for i in range(24):
                try:
                    total += float(df['T'][i])
                    num += 1
                except:
                    continue
            mean = total/num
            for i in range(24):
                if df['T'][i] in ('/', 'X'):
                    df['T'][i] = mean
            temparature = np.array(df['T'], dtype='float')
        meanT = np.mean(temparature)
        maxT = np.max(temparature)
        minT = np.min(temparature)
        # --- rain ---
        rain = df['Rain']
        rain_total = 0
        for i in range(len(df['Hour'])):
            if rain[i] in ('T', '/', '&', 'X'):
                rain[i] = int(0)
            rain_total = rain_total + float(rain[i])

        return rain_total, meanT, minT, maxT

    def use(self):
        folderName = f'{self.app.select_area.get()}from{self.app.select_date.get()}'
        if not os.path.exists(os.path.join(self.path, folderName)):
            os.mkdir(os.path.join(self.path, folderName))

        for stNo in self.app.pastdata.areaStationsList[self.app.select_area.get()]:
            if f'{stNo}.csv' in os.listdir(os.path.join(self.path, folderName)):
                pass
            else:
                break
        else:
            return
        isXlsx = False
        for timedelta in range(2, 9):
            date_ = datetime.date(
                *self.app.str_tuple_date_change(self.app.select_date.get())) - datetime.timedelta(timedelta)
            dateFolderName = self.app.str_tuple_date_change(
                (date_.year, date_.month, date_.day)
            )

            for files in os.listdir(os.path.join(self.app.datas, f'{self.app.select_area.get()}{dateFolderName}')):
                '''files is raw grabbing data'''
                print(files)
                df = pd.read_excel(os.path.join(
                    self.app.datas, f'{self.app.select_area.get()}{dateFolderName}', files))
                processed_data = self.__missing_value(df)

                if isXlsx == False:
                    data = {"rain": processed_data[0], "meanT": processed_data[1],
                            "minT": processed_data[2], "maxT": processed_data[3]}
                    df = pd.DataFrame(data, index=[0])
                    df.to_csv(os.path.join(
                        self.path, folderName, f'{self.app.delete_extension(files)}.csv'), index=True)
                else:
                    df = pd.read_csv(os.path.join(
                        self.path, folderName, f'{self.app.delete_extension(files)}.csv'))
                    data = {"rain": processed_data[0], "meanT": processed_data[1],
                            "minT": processed_data[2], "maxT": processed_data[3]}
                    df = df.append(data, ignore_index=True)

                    df.to_csv(os.path.join(
                        self.path, folderName, f'{self.app.delete_extension(files)}.csv'), index=False)

            isXlsx = True


if __name__ == '__main__':
    pass
