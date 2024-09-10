"""
strompris fastapi app entrypoint
"""

import datetime
import os
from typing import Dict, List, Optional
import pandas as pd
import altair as alt
from fastapi import FastAPI, Form, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from strompris import (
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_prices,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")




@app.get("/",response_class=HTMLResponse)
async def render(request: Request, location_codes: Optional[Dict[str,str]] = LOCATION_CODES, today: datetime.date=datetime.date.today())-> None:
    """
    Render the strompris.html template.

    Parameters:
    - request (Request): The FastAPI request object.
    - location_codes (Optional[Dict[str, str]]): Location code dictionary (default: LOCATION_CODES).
    - today (datetime.date): The current date (default: today's date).

    Returns:
    None
    """
    chart = plot_prices(fetch_prices(end_date=today,locations=location_codes))
    return templates.TemplateResponse("strompris.html", {"request":request,"chart":chart.to_html(),"NowDate":today,"locations":location_codes})



@app.get("/plot_prices.json",response_class=JSONResponse)
async def plot(locations:Optional[List[str]]=Query(default=None),end: datetime.date=None,days:int=7) -> None:
    """
    Get JSON representation of the energy prices chart.

    Parameters:
    - locations (Optional[List[str]]): List of locations (optional).
    - end (datetime.date): End date (optional).
    - days (int): Number of days (default: 7).

    Returns:
    None
    """
    chart=plot_prices(fetch_prices(end_date=end,locations=locations,days=days))
    return chart.to_dict()

def main():
    """Launches the application on port 5000 with uvicorn"""
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
