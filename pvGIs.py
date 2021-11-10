import pandas as pd
import datetime
from timezonefinder import TimezoneFinder
from pvlib.forecast import GFS,NAM


def getPredictions(latitude,longitude):
    obj= TimezoneFinder()
    timeZone=obj.timezone_at(lng=latitude, lat=longitude)
    start = pd.Timestamp(datetime.date.today(), tz=timeZone)
    end = start + pd.Timedelta(days=7)
    model = GFS()
    raw_data=model.get_data(latitude,longitude,start,end)
    data = raw_data
    data = model.rename(data)
    data['temp_air'] = model.kelvin_to_celsius(data['temp_air'])
    data['wind_speed'] = model.uv_to_speed(data)
    windSpeed = data['wind_speed']
    temperatures = data['temp_air']
    
    irrad_data = model.cloud_cover_to_irradiance(data['total_clouds'])
    data = data.join(irrad_data, how='outer')
    data = data[model.output_variables]
    
    #Cloud scaling algorith to calculate ghi,dni,dhi
    data = model.rename(raw_data)
    irrads = model.cloud_cover_to_irradiance(data['total_clouds'], how='clearsky_scaling')
    ghi = irrad_data.loc[irrad_data['ghi'] != 0]
    ghiMean = ghi['ghi'].mean()
    windSpeedMean = windSpeed.mean()
    temperaturesMean = temperatures.mean()
    results= {'avgWindSpeed':windSpeedMean,'avgTemperatures':temperaturesMean,'ghi':ghiMean}
    return results

def test():
    return "Test()"