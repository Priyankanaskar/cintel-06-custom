# ------------------------------------------------------------------------------------------------------------------------
# Imports at the top - PyShiny EXPRESS VERSION
# ---------------------------------------------------------------------------------------------------------------------

import faicons as fa
import plotly.express as px
from shinywidgets import render_plotly
import asyncio
from shiny import reactive, render, req
from shiny.express import input, ui
import random
from datetime import datetime
from datetime import date, timedelta
from collections import deque
import pandas as pd
from scipy import stats
import shinyswatch

# Original UI layout and style setup
ui.HTML(
    """
  <style>
  body {
    background-color: #ADD8E6;
    color: #333; 
    font-family: Arial-bold, gothic;
    font-size: 16px; 
    font-weight: normal; 
    font-style: bold; 
    text-decoration: none; 
    text-transform: none; 
    line-height: 1.5; 
    letter-spacing: normal;
  }
  /* Add border style to headers 
  h1, h2, h3, h4, h5, h6 {
    border-bottom: 2px solid #333;
    padding-bottom: 5px; 
    margin-bottom: 10px; 
  }
  </style>
"""
)

# Load data and compute static values
tips = px.data.tips()
bill_rng = (min(tips.total_bill), max(tips.total_bill))

# Add page title and sidebar
ui.page_opts(title="Kansas Barbecue Dashboard", fillable=True,)

# Theme
shinyswatch.theme.materia()

with ui.sidebar(open="desktop",style="background-color: #e0ffff"):
    ui.input_slider(
        "total_bill",
        "Bill amount",
        min=bill_rng[0],
        max=bill_rng[1],
        value=bill_rng,
        pre="$",
    )
    ui.input_checkbox_group(
        "time",
        "Food service",
        ["Lunch", "Dinner", "Weekend Brunch"],
        selected=["Lunch", "Dinner", "Weekend Brunch"],
        inline=True,
    )
    ui.input_action_button("reset", "Reset filter")
    
    # Default value is the date in client's time zone
    ui.input_date("date2", "Date:")

    ui.hr()
    ui.h6("Links:")
    ui.a(
        "GitHub Source",
        href="https://github.com/Priyankanaskar/cintel-05-cintel",
        target="_blank",
    )

    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    
    ui.a("Pyshiny Express",
        href="https://shiny.posit.co/py/api/express/", target= "_blank")
   
# In Shiny Express, everything not in the sidebar is in the main panel--------------------------------------------------

ui.input_action_button("do_compute", "Tip Calculator")


@render.ui
@reactive.event(input.do_compute)
async def compute():
    with ui.Progress(min=1, max=10) as p:
        p.set(message="Calculation in progress", detail="This may take few second...")

        for i in range(1, 15):
            p.set(i, message="How much should I tip")
            await asyncio.sleep(0.1)

    return " Hope You enjoy our service!...Please Visit Again ! "


# Add main content
ICONS = {
    "user": fa.icon_svg("user", "regular"),
    
    "wallet": fa.icon_svg("wallet"),
    
    "currency-dollar": fa.icon_svg("dollar-sign"),
    
    "gear": fa.icon_svg("gear"),
}

with ui.layout_columns(fill=False):
    with ui.value_box(showcase=ICONS["user"],theme="bg-gradient-blue-red"):
        
        "Total tippers"

        @render.express
        def total_tippers():
            tips_data().shape[0]

    with ui.value_box(showcase=ICONS["wallet"],theme="bg-gradient-blue-red"):
        "Average tip"

        @render.express
        def average_tip():
            d = tips_data()
            if d.shape[0] > 0:
                perc = d.tip / d.total_bill
                f"{perc.mean():.1%}"

    with ui.value_box(showcase=ICONS["currency-dollar"],theme="bg-gradient-blue-red"):
        "Average bill"

        @render.express
        def average_bill():
            d = tips_data()
            if d.shape[0] > 0:
                bill = d.total_bill.mean()
                f"${bill:.2f}"


with ui.layout_columns(col_widths=[6, 6, 12]):
    with ui.card(full_screen=True, style="background-color: #e6e6fa "):
        ui.card_header("Tips Table ")
        ICONS["user"]
        @render.data_frame
        def table():
            return render.DataGrid(tips_data())

    with ui.card(full_screen=True ,style="background-color: #e6e6fa "):
        with ui.card_header(class_="d-flex justify-content-between align-items-center"):
            "Weekly bill vs tip"
            with ui.popover(title="Add a color variable", placement="top"):
                ICONS["gear"]
                ui.input_radio_buttons(
                    "scatter_color",
                    None,
                    ["none", "sex", "smoker", "day", "time"],
                    inline=True,
                )

        @render_plotly
        def scatterplot():
            color = input.scatter_color()
            return px.scatter(
                tips_data(),
                x="total_bill",
                y="tip",
                color=None if color == "none" else color,
                trendline="lowess",
            )

    with ui.card(full_screen=True,style="background-color: #e6e6fa "):
        with ui.card_header(class_="d-flex justify-content-between align-items-center"):
            "Tip Percentages"
            with ui.popover(title="Add a color variable"):
                ICONS["gear"]
                ui.input_radio_buttons(
                    "tip_perc_y",
                    "Split by:",
                    ["sex", "smoker", "day", "time"],
                    selected="day",
                    inline=True,
                )

        @render_plotly
        def tip_perc():
            from ridgeplot import ridgeplot

            dat = tips_data()
            dat["percent"] = dat.tip / dat.total_bill
            yvar = input.tip_perc_y()
            uvals = dat[yvar].unique()

            samples = [[dat.percent[dat[yvar] == val]] for val in uvals]

            plt = ridgeplot(
                samples=samples,
                labels=uvals,
                bandwidth=0.01,
                colorscale="viridis",
                colormode="row-index",
            )

            plt.update_layout(
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5
                )
            )

            return plt


# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------


@reactive.calc
def tips_data():
    bill = input.total_bill()
    idx1 = tips.total_bill.between(bill[0], bill[1])
    idx2 = tips.time.isin(input.time())
    return tips[idx1 & idx2]


@reactive.effect
@reactive.event(input.reset)
def _():
    ui.update_slider("total_bill", value=bill_rng)
    ui.update_checkbox_group("time", selected=["Lunch", "Dinner"])
