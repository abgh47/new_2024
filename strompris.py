#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime
import warnings

import altair as alt
import pandas as pd
import requests
import requests_cache

requests_cache.install_cache()


warnings.filterwarnings("ignore", ".*convert_dtype.*", FutureWarning)




def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API.

    Parameters:
    - date (datetime.date, optional): The date for which to fetch prices. Defaults to today.
    - location (str): The location code. Defaults to "NO1" (Oslo).

    Returns:
    pd.DataFrame: A DataFrame containing the fetched data with columns 'NOK_per_kWh' and 'time_start'.
    """
    if date is None:
        date = datetime.date.today()

    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date.year}/{'{:02d}'.format(date.month)}-{'{:02d}'.format(date.day)}_{location.strip()}.json"
    r = requests.get(url)

    json = r.json()
    data = {"NOK_per_kWh":[],"time_start":[]}
    for i in json:
        data["NOK_per_kWh"].append(i["NOK_per_kWh"])
        data["time_start"].append(pd.to_datetime(i["time_start"]))
    df = pd.DataFrame(data)
    return df


# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {"NO1":"Oslo","NO2":"Kristiansand","NO3":"Trondheim ","NO4":"Tromsø","NO5":"Bergen"}



def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations: list[str] = tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame.

    Parameters:
    - end_date (datetime.date, optional): The end date for fetching prices. Defaults to today.
    - days (int): The number of days to fetch prices for. Defaults to 7.
    - locations (list[str]): The list of locations to fetch prices for. Defaults to all locations.

    Returns:
    pd.DataFrame: A DataFrame containing the fetched data with columns 'NOK_per_kWh', 'time_start', 'location_code', and 'location'.
    """
    if not locations:
        locations = tuple(LOCATION_CODES.keys())
    df = None
    if end_date is None:
        end_date = datetime.date.today()
    for i in locations:
        i=i.strip()
        start_date = end_date - datetime.timedelta(days=days)
        while start_date != end_date:
            temp = fetch_day_prices(start_date,location=i)
            temp["location_code"]= i
            temp["location"] = LOCATION_CODES[i]
            if df is None:
                df = temp
            else:
                df = pd.concat([df,temp])
            start_date =start_date+ datetime.timedelta(days=1)
    return df





def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the data to plot with columns 'time_start', 'NOK_per_kWh', and 'location'.

    Returns:
    alt.Chart: Altair chart object representing the plotted data.
    """
    df["time_start"] = pd.to_datetime(df["time_start"],utc=True)
    chart = alt.Chart(df).mark_line().encode(
    x="time_start:T",
    y="NOK_per_kWh:Q",
    color="location:N"
    ).properties(width=600,height=400)
    return chart


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
