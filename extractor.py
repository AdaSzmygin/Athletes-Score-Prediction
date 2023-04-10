from os import walk
import pandas as pd
filenames=next(walk("Weather_data/"))[2]

Temperature=[]
Humidity=[]
Pressure=[]
Precipitation=[]
Condition=[]

for i in range(len(filenames)):
                data=[]
                with open("Weather_data/"+filenames[i], 'r') as file:
                    # read a list of lines into data
                    data = file.readlines()
                try: 
                    Temperature.append(data[0])
                    Humidity.append(data[1])
                    Pressure.append(data[2])
                    Precipitation.append(data[3])

                except IndexError:
                    Temperature.append('')
                    Humidity.append('')
                    Pressure.append('')
                    Precipitation.append('')
                try:
                    Condition.append(data[4])
                except IndexError:
                    Condition.append('')
                    
                    
                    
weatherdataDict={
    'Temperature':Temperature,
    'Humidity':Humidity,
    'Pressure':Pressure,
    'Precipitation':Precipitation,
    'Condition':Condition
}
wd=pd.DataFrame(weatherdataDict)
wd.to_csv('WeatherDataHistory.csv')