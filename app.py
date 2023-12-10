# Importing Required Libraries
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.add_vertical_space import add_vertical_space
import matplotlib.pyplot as plt

# Models
from Models.LongTermAnalysis import LONG_TERM_ANALYSIS

def main():
    st.set_page_config(page_title="Oil Production Forecasting")

    st.title("OIL PRODUCTION FORECASTING")
    st.sidebar.header("US-OIL-PRODUCTION")
    forecast_selected = st.sidebar.selectbox('Select a Forecast', ["Short-Term Forecast", "Long-Term Forecast"])
    button_selected = st.sidebar.button(':red[ANALYZE]')

    if button_selected:
        st.header("Forecast: {}".format(forecast_selected))

        if forecast_selected == "Short-Term Forecast":
            # prediction_class = short_term_predict()
            prediction_class = 1

            if prediction_class == 0:
                st.metric(label="OIL PRODUCTION DIRECTION", value="DOWN", delta="-0")
                style_metric_cards()
            else:
                st.metric(label="OIL PRODUCTION DIRECTION", value="UP", delta="+1")
                style_metric_cards()
    
        else:
            no_of_months = 18
            #no_of_months = st.slider("Number of Months you wanna forecast", min_value=18, max_value=24)
            #slide_button_selected = st.button(':green[FORECAST]')

            lta = LONG_TERM_ANALYSIS(no_of_months)
            lta.long_term_prediction()
            output_df = lta.output_df

            fig, ax = plt.subplots()
            ax.plot(output_df.index, output_df['NBEATS_PREDICTION'], label='NBEATS PREDICTION', color='orange')
            ax.plot(output_df.index, output_df['TSA_PREDICTION'], label='TSA PREDICTION', color='green')
            ax.set_xlabel('Date')
            ax.set_ylabel('Oil Production (Thou. Bbl)')
            ax.legend()

            # Display the plot in Streamlit
            st.subheader("FORECASTING PLOT")
            st.pyplot(fig)

            add_vertical_space(2)
            
            st.subheader("FORECASTING VALUES")
            st.dataframe(output_df, use_container_width=True)


if __name__=='__main__':
    main()
