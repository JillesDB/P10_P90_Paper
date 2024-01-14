import datetime

from Epftoolbox_original_code import _lear
import pandas as pd
import os
from Epftoolbox_original_code.evaluation import MAE
from pathlib import Path
import clock_plot
import clock_plot.clock as cp
import plotly
from datetime import date,time

path_datasets_folder = str(Path.cwd().parent) + '\Datasets'
path_forecasts_folder = str(Path.cwd().parent) + '\Dataframes_with_Coefficients'



def generate_clock_plot_from_existing_file(path_file,calibration_window,group_curves_by = 'date',
                                           covariate_family = 'Lagged_Prices',filter={}):
    """

    Parameters
    ----------
    path_file
    group_curves_by: can be any of the following: year,month,day,date,hour,season.
    For documentation, see https://github.com/ES-Catapult/clock_plot/blob/main/README.md

    covariate_family: should be one of the following strings:
    'Lagged_Prices','Wind','Solar','Fossil_Fuels','FR_Generation_Load','Swiss_Prices','BE_Load_Weather'

    Returns
    -------

    """
    dataframe_coefficient = pd.read_csv(path_file)
    begin_date = dataframe_coefficient['datetime'].iloc[0]
    end_date  = dataframe_coefficient['datetime'].iloc[-1]
    if group_curves_by == 'variable family':
        dataframe_coefficients_long_form = dataframe_coefficient.melt(id_vars=["datetime"], value_vars=["Solar", "Wind", "Lagged_Prices", "Fossil_Fuels", "FR_Generation_Load",'Swiss_Prices','BE_Load_Weather'])
        dataframe_coefficients_long_form.rename(columns={"variable": "variable family"}, inplace=True)
        print(dataframe_coefficients_long_form.head())
        if filter=={}:
            fig = cp.clock_plot(dataframe_coefficients_long_form,datetime_col='datetime',
                      value_col='value',color='variable family',filters=filter,
                                #title='All Coefficients for CW 112')
                            title='All Coefficients for CW{} from 1 Jan 2020 until 31 Dec 2022'.format(calibration_window,str(begin_date),str(end_date)))
        else:
            fig = cp.clock_plot(dataframe_coefficients_long_form, datetime_col='datetime',
                                value_col='value', color='variable family', filters=filter,
                                # title='All Coefficients for CW 112')
                                title='Fossil Fuel Coefficients for CW{} in 2021}'.format(calibration_window, str(filter)))
    else:
        fig = cp.clock_plot(dataframe_coefficient, datetime_col='datetime', filters=filter,
                            value_col=str(covariate_family), color=group_curves_by,
                            title='{} Coefficients for CW {}, in 2022'.format(str(covariate_family),calibration_window,str(filter)))
                           # title='{} Coefficients for CW {}\n from {} until {}'.format(str(covariate_family),calibration_window,str(begin_date),str(end_date)))
    fig.show()



# generate_clock_plot_from_existing_file(path_file=r'C:\Users\r0763895\Documents\Masterthesis\Masterthesis\Code\epftoolbox\Cleaned_code\Dataframes_with_Coefficients\Data_clock_plot_Lagged_Prices_dataframe_Example_dataframe_CW56.csv',
#                                        group_curves_by='month')
# generate_clock_plot_from_existing_file(path_file=r'C:\Users\r0763895\Documents\Masterthesis\Masterthesis\Code\epftoolbox\Cleaned_code\Dataframes_with_Coefficients\Aggregated_Coefficients_Full_Dataset_CW728.csv',
#                              calibration_window=728,group_curves_by='variable family',filter={'year': 2020})
# generate_clock_plot_from_existing_file(path_file=r'/Dataframes_with_Coefficients\Aggregated_Coefficients_Full_Dataset_CW56.csv',
#                                        calibration_window=56, group_curves_by='season', covariate_family='Fossil_Fuels', filter={'year': 2022})
#generate_clock_plot_from_existing_file(path_file=r'C:\Users\r0763895\Documents\Masterthesis\Masterthesis\Code\epftoolbox\Cleaned_code\Dataframes_with_Coefficients\Aggregated_Coefficients_Full_Dataset_CW728.csv',
 #                            calibration_window=728,group_curves_by='variable family',filter={'year': 2022})