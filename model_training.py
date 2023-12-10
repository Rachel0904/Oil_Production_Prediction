import pandas as pd
from darts import TimeSeries
from darts.models import NBEATSModel
from darts.utils.missing_values import fill_missing_values

file_path = "C://Users/Rachel/Downloads/GH/Oil_Production_Prediction/Data/US_DATA.csv"
df = pd.read_csv(file_path)

df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
series = TimeSeries.from_dataframe(df, value_cols=['OILPRODUS'])
series = fill_missing_values(series)

# Define the model
model = NBEATSModel(input_chunk_length=24, output_chunk_length=12, n_epochs=100)
model.fit(series, verbose=True)

model_path = 'C://Users/Rachel/Downloads/GH/Oil_Production_Prediction/Models/Model_Pickle/nbeats.th'  # Specify the path where you want to save the model
model.save(model_path)

