import datetime

from Epftoolbox_original_code import _lear
import pandas as pd
import os
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date,time
sns.set(rc={'figure.figsize':(6,36)})
path_datasets_folder = str(Path.cwd().parent) + '\Dataframes_with_coefficients'
path_forecasts_folder = str(Path.cwd().parent) + '\Forecasts_for_plots'
path_real_prices = os.path.join(path_datasets_folder,'Real_prices.csv')

def plot_coefficient_matrix_heatmap(name_csv,calibration_window,start=None,end=None,
                                    from_hour = '00:00',to_hour='23:00'):
    """

    Parameters
    ----------
    path_file

    Returns
    -------

    """
    path_file = os.path.join(path_datasets_folder,name_csv)
    dataframe_coefficients = pd.read_csv(path_file)
    if start != None:
        day_selection = (dataframe_coefficients['datetime'] >= start) & (dataframe_coefficients['datetime'] <= end)# + datetime.timedelta(hours=23))
        filtered_dataframe = dataframe_coefficients.loc[day_selection]
    else:
        filtered_dataframe = dataframe_coefficients
    print(filtered_dataframe)
    filtered_dataframe = filtered_dataframe.set_index(pd.DatetimeIndex(filtered_dataframe['datetime'])).drop(columns=['Unnamed: 0','datetime'])
    filtered_dataframe = filtered_dataframe.between_time(from_hour,to_hour) #16 hours per day
    # filtered_dataframe_night = filtered_dataframe.between_time('22:30','06:30')#8 hours per night
    # print(filtered_dataframe_day,filtered_dataframe,filtered_dataframe_night)
    # filtered_dataframe = filtered_dataframe.apply(lambda y: (y - y.mean()) / y.std(), axis=0)
    # filtered_dataframe_day = filtered_dataframe_day.apply(lambda y: (y - y.mean()) / y.std(), axis=0)
    # filtered_dataframe_night = filtered_dataframe_night.apply(lambda y: (y - y.mean()) / y.std(), axis=0)
    nb_hours = datetime.datetime.strptime(to_hour, '%H:%M') - datetime.datetime.strptime(from_hour, '%H:%M')
    print(nb_hours)
    nb_row = int((nb_hours.seconds+3600)/3600*7*4) #15*7 hours per week => four week average

    # If we want to normalize the data?
    # filtered_dataframe = filtered_dataframe.rolling(nb_row).mean()[nb_row-1:]
    abs_dataframe = abs(filtered_dataframe)
    sum_row = abs_dataframe.sum(axis=0)
    print(sum_row.nlargest(12))
    # filtered_dataframe_night = filtered_dataframe_night.rolling(nb_row).mean()[nb_row-1:]
    plt.figure(figsize=(12,8))
    ax = sns.heatmap(filtered_dataframe,yticklabels=nb_row*2,cmap='seismic',vmin=-0.8,vmax = 0.8,center=0)#seismic#RdYlGn#Spectral #coolwarm yticklabels = 8760/nb_row
    ax.set_title('Coefficients for CW' + str(calibration_window)+' from '+str(filtered_dataframe.index[0]) + ' until ' +str(filtered_dataframe.index[-1]))
    plt.tight_layout()
    plt.show()


plot_coefficient_matrix_heatmap(name_csv='Raw_coefficientsFull_Dataset_CW728.csv',calibration_window=728,
                               start='2020-01-01 00:00:00',end='2022-12-31 23:00:00'
                                # ,from_hour='11:30',to_hour='12:30'
                                )

# df = pd.read_csv(r'C:\Users\jdeblauw\Documents\GitHub\Belgian_DAM_forecasting_paper\Cleaned_code\Dataframes_with_Coefficients\Raw_coefficientsFull_Dataset_CW56.csv')
# df2 = pd.read_csv(r'C:\Users\jdeblauw\Documents\GitHub\Belgian_DAM_forecasting_paper\Cleaned_code\Dataframes_with_Coefficients\Raw_coefficientsFull_Dataset_CW728.csv')
# print(df,df2)
#
# # df = df.drop(columns=['Unnamed: 0','Unnamed: 0.1'])
# #df = df.reset_index().rename(columns={df.index.name:'Unnamed: 0'})
# # df2 = df2.set_index('Unnamed: 0')
# df2 = df2.rename(columns={"Unnamed: 0": "datetime"})
# # df2.index.name = 'datetime'
# print(df,df2)
# df2.to_csv(r'C:\Users\jdeblauw\Documents\GitHub\Belgian_DAM_forecasting_paper\Cleaned_code\Dataframes_with_Coefficients\Raw_coefficientsFull_Dataset_CW728.csv')

# df = pd.read_csv(r'C:\Users\jdeblauw\Documents\GitHub\Belgian_DAM_forecasting_paper\Cleaned_code\Dataframes_with_Coefficients\Raw_coefficientsFull_Dataset_CW112.csv')
# df = df.drop(columns=['index'])
# df.to_csv(r'C:\Users\jdeblauw\Documents\GitHub\Belgian_DAM_forecasting_paper\Cleaned_code\Dataframes_with_Coefficients\Raw_coefficientsFull_Dataset_CW112.csv',mode = 'w')
#
