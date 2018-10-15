#code taken from : https://pypi.org/project/weather-api/
#code modified to fit project

#checks weather forecast, temperature high and low
from weather import Weather, Unit
weather = Weather(unit=Unit.FAHRENHEIT)

def checkWeather(city):
    location = weather.lookup_by_location(city)
    condition = location.condition
    
    # Get weather forecasts for today
    
    forecasts = location.forecast
    
    forecast = forecasts[0]
    lst = [condition.text,forecast.text,forecast.date,forecast.high,forecast.low]
    return lst
    
