# Config Import
from Config.Model_Paths import model_paths

# Importing necessary library
import pickle
import pandas as pd
from darts.models import NBEATSModel

class LONG_TERM_ANALYSIS:

    def __init__(self, no_of_months):

        self.no_of_months = no_of_months
        self.output_df = pd.DataFrame()

    def form_df(self):
        temp_df = pd.read_csv(model_paths["DATA"])
        #temp_df = pd.read_csv("C://Users/Rachel/Downloads/FP-2/Data/US_DATA.csv")
        
        t = list(range(1, len(temp_df) + 1))
        temp_df['Date'] = pd.to_datetime(temp_df['Date'])
        temp_df['month'] = temp_df['Date'].dt.month
        temp_df['t'] = t
        temp_df.set_index('Date', inplace=True)

        # Find the last month number and last t
        last_t = temp_df.iloc[-1]['t']
        last_month = temp_df.iloc[-1]['month']
        last_date = temp_df.index[-1]

        # Generate t(s) and month(s)
        t_list = [last_t+idx+1 for idx, i in enumerate(range(self.no_of_months))]
        month_list = []
        for idx, i in enumerate(range(self.no_of_months)):
            month = last_month + idx + 1
            month = (month - 1) % 12 + 1
            month_list.append(month)

        start_of_next_month = pd.date_range(start=last_date, periods=2, freq='M')[0]
        next_dates = pd.date_range(start=start_of_next_month, periods=self.no_of_months, freq='MS')

        df = pd.DataFrame()
        df['t']     = t_list
        df['month'] = month_list
        df['month'] = df['month'].astype(int)
        df['Date']  = next_dates
        df.set_index('Date', inplace=True)
        df['Oil_Production'] = 0

        month_dummies = pd.get_dummies(df['month'], prefix='month', drop_first=True)
        for col in month_dummies.columns:
            values = month_dummies[col]
            month_dummies[col] = [1 if val==True else 0 for val in values]

        df = pd.concat([df, month_dummies], axis=1)

        drop_columns = ["month"]
        df = df.drop(drop_columns, axis=1)

        return df

    def trend_seasonality_ar_predict(self):

        # Trend and Seasonality
        # Load the model from the file
        with open(model_paths["Trend_Seasonality"], 'rb') as file:
        #with open("C://Users/Rachel/Downloads/FP-2/Models/Model_Pickle/Trend_Seasonality.pkl", 'rb') as file:
            trend_seasonality_model = pickle.load(file)

        # AR Model
        with open(model_paths["AR"], 'rb') as file:
        #with open("C://Users/Rachel/Downloads/FP-2/Models/Model_Pickle/AR.pkl", 'rb') as file:
            ar_model = pickle.load(file)

        # Create a df
        df = self.form_df()
        pred_1 = trend_seasonality_model.predict(df)
        pred_2 = ar_model.forecast(steps=self.no_of_months)
        final_pred = pred_1 + pred_2
        df["Oil_Production"] = final_pred
        
        df_ = df.copy()
        df_["TSA_PREDICTION"] = df_["Oil_Production"]
        df_ = df_[["TSA_PREDICTION"]]
        self.output_df = df_

    def nbeats_predict(self):
        model_path = model_paths["NBEATS"]
        #model_path = "C://Users/Rachel/Downloads/FP-2/Models/Model_Pickle/nbeats.th"

        model = NBEATSModel(input_chunk_length=24, output_chunk_length=12, n_epochs=100)
        loaded_model = model.load(model_path)
        pred = loaded_model.predict(self.no_of_months)
        pred_df = pred.pd_dataframe()
        self.output_df["NBEATS_PREDICTION"] = pred_df["OILPRODUS"].values


    def long_term_prediction(self):
        self.trend_seasonality_ar_predict()
        self.nbeats_predict()

#lta = LONG_TERM_ANALYSIS(no_of_months=18)
#lta.long_term_prediction()
    
