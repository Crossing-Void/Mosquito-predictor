from joblib import load
import pandas as pd
import numpy as np
import os


class ToPredict:
    def __init__(self, app) -> None:
        self.app = app

    def get_all_models(self):
        '''
        include extension
        '''
        parse = '.joblib'
        return [files for files in os.listdir(self.app.models) if
                os.path.splitext(os.path.join(self.app.models, files))[-1] == parse]

    def analyze(self):
        '''
        using without model extension
        '''
        modelName = self.app.select_model.get()
        model = load(os.path.join(self.app.models, modelName+'.joblib'))

        folder = os.path.join(self.app.datas, 'combines',
                              f'{self.app.select_area.get()}from{self.app.select_date.get()}')

        for file in os.listdir(folder):
            if not os.path.isdir(temp := os.path.join(folder, file)):
                df = pd.read_csv(temp)
                pre_data = df.iloc[:, 1:5]
                prediction = np.array(model.predict(pre_data))

                if modelName in df.columns:
                    df[modelName] = prediction
                else:
                    df.insert(
                        len(df.columns), column=modelName, value=prediction)
                df.to_csv(temp, index=False)
