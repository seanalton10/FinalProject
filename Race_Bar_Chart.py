import pandas as pd
import bar_chart_race as bcr
import warnings
warnings.filterwarnings('ignore')

#load data
dataset = pd.read_csv('2017.csv', delimiter=',')

#count totals for each airline on each day
grouped = dataset.groupby(['FL_DATE','OP_CARRIER'],as_index=False).size()

#create pivot table of daily values for each airline
pivot = pd.pivot(grouped, index='FL_DATE', columns="OP_CARRIER", values="size").reset_index()

#set date field to datetime
pivot['FL_DATE'] = pd.to_datetime(pivot['FL_DATE'])

#set date column as index
pivot = pivot.set_index('FL_DATE')

#create running total dataframe
cumulative_sum = (pivot.cumsum())

#record indxex of cumulative sum
dates = cumulative_sum.index

#create empty array that will store the weekly dates
weekly_dates = []

#add every 7th date from dates into weekly dates
for date in range(len(dates)):
    if date % 7 == 0:
        weekly_dates.append(dates[date])

#reset the index in cumulative sum to numbers
df_no_date = cumulative_sum.reset_index()

#drop the FL_DATE column for now since the groupby functionality doesn't operate on dates
df_no_date = df_no_date.drop(columns=['FL_DATE'])

#group the df_no_date by every 7th date
N = 7
df_no_date = df_no_date.groupby(df_no_date.index // N).sum()

#drop last row and weekly date since data values do not include a full week
df_no_date = df_no_date[:-1]
weekly_dates.pop()

#create final dataframe
df_final = df_no_date

#insert FL_DATE again with weekly dates and make them index
df_final['FL_DATE'] = weekly_dates
df_final = df_final.set_index('FL_DATE')

print("creating chart...")  

#to create video file you need to have ffmpeg installed...that can be done on mac using the tutorial below
#https://www.youtube.com/watch?v=H1o6MWnmwpY

#this takes about 5 minutes to complete depending on computer specs
bcr.bar_chart_race(
                    df = df_final, 
                    img_label_folder = "bar_image_logos",   #indicte folder to identify logos with bars
                    n_bars = 10, 
                    orientation='h', 
                    sort='desc',
                    title='Domestic Flight Counts by Airline',
                    shared_fontdict={'family': 'Helvetica', 'weight': 'bold',
                                    'color': 'black'},
                    period_summary_func=lambda v, r: {'x': .98, 'y': .2, 
                                          's': f'Total Flights: {v.sum():,.0f}', 
                                          'ha': 'right', 'size': 11},   #record total flights
                    bar_label_font=6,   #this is text number inside bar
                    tick_label_font=8,  #this is text carrier code
                    period_template =  '%B %d, %Y',     #date format indicated on chart
                    bar_textposition='inside', 
                    fixed_max=True,       #make the max value static
                    perpendicular_bar_func='median',    #create a moving median line
                    filename = 'airlines.mp4',
)
