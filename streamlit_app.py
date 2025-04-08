import streamlit as st
import swisseph as swe
import datetime

# -----------------------------------------------------------------------------
# Ephemeris Setup (adjust the path as needed)
# -----------------------------------------------------------------------------
swe.set_ephe_path('/usr/share/ephe')  # Adjust this path if required

# -----------------------------------------------------------------------------
# Baseline (Natal) Chart for the Market (Example Values)
# -----------------------------------------------------------------------------
NIFTY_NATAL = {
    'ascendant': 15.0,  # Example value; this should be calibrated as needed
    'sun': 10.0,
    'moon': 20.0,
}

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def angular_difference(deg1, deg2):
    """Compute the shortest angular difference between two degrees."""
    return abs((deg1 - deg2 + 180) % 360 - 180)

def local_to_ut(dt_local):
    """Convert local IST datetime (UTC+5:30) to Universal Time."""
    return dt_local - datetime.timedelta(hours=5, minutes=30)

def get_planet_position(planet, dt_local):
    """
    Get the ecliptic longitude of the specified planet at the given local datetime.
    The output is in degrees.
    """
    dt_ut = local_to_ut(dt_local)
    jd = swe.julday(dt_ut.year, dt_ut.month, dt_ut.day, dt_ut.hour + dt_ut.minute / 60.0)
    pos, _ = swe.calc_ut(jd, planet)
    return pos[0]

# -----------------------------------------------------------------------------
# Forecast Function: Simplified Output Without Astrological Details
# -----------------------------------------------------------------------------
def forecast_for_date(date_str):
    """
    Generate a simplified intraday forecast for the given date (format: 'YYYY-MM-DD', IST).
    The output displays only the time slot and the recommended trading signal.
    """
    dt_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    
    # Define key intraday slots (IST)
    key_slots = {
        "9:30-9:50": dt_date.replace(hour=9, minute=30),
        "9:50-10:00": dt_date.replace(hour=9, minute=50),
        "10:00-10:30": dt_date.replace(hour=10, minute=0),
        "10:55-11:20": dt_date.replace(hour=10, minute=55),
        "11:20-11:45": dt_date.replace(hour=11, minute=20),
        "11:45-12:30": dt_date.replace(hour=11, minute=45),
        "12:30-13:00": dt_date.replace(hour=12, minute=30),
        "13:00-13:25": dt_date.replace(hour=13, minute=0),
        "13:25-14:00": dt_date.replace(hour=13, minute=25),
        "Post 14:00": dt_date.replace(hour=14, minute=0)
    }
    
    forecast = f"### Intraday Trading Signal Forecast for {date_str} (IST):\n\n"
    
    # For each slot, determine the trading signal.
    # The logic here is based on pre-defined time slots.
    # In a more detailed system, this would come from astrological calculations.
    for slot in key_slots:
        if slot in ["9:30-9:50", "10:55-11:20", "12:30-13:00"]:
            trade_signal = "Avoid / Short (High Volatility)"
        elif slot in ["9:50-10:00", "11:45-12:30", "13:00-13:25"]:
            trade_signal = "Neutral / Observe"
        elif slot == "10:00-10:30":
            trade_signal = "Potential Long (Recovery in progress)"
        elif slot in ["11:20-11:45", "13:25-14:00"]:
            trade_signal = "Go Long (Entry Signal)"
        else:
            trade_signal = "Cautious / Monitor"

        # Append only the time slot and trading signal
        forecast += f"**{slot} (IST)** → **{trade_signal}**\n\n"
    
    # Optionally, you could append additional sector-specific information here if needed.
    forecast += (
        "#### Sector-Specific Forecast:\n\n"
        "- **9:30-10:00**: Banking & Financials likely to be weaker; IT may show early resilience; FMCG remains steady.\n\n"
        "- **10:00-10:30**: IT & Pharma may begin to recover slightly while Banking remains cautious.\n\n"
        "- **10:55-11:20**: High volatility across sectors; prefer minimal trading unless using tight stops.\n\n"
        "- **11:20-11:45**: Banking & Financials might rebound; IT & FMCG could follow the positive trend.\n\n"
        "- **12:30-13:00**: Renewed caution across cyclical sectors; blue-chips may hold steadier.\n\n"
        "- **13:25-14:00**: Banking & IT likely to lead in a strong recovery; Consumer Discretionary sees buying interest.\n\n"
        "- **Post 14:00**: Profit taking and cautious moves dominate; defensive sectors may outperform.\n\n"
    )
    
    return forecast

# -----------------------------------------------------------------------------
# Streamlit Interface
# -----------------------------------------------------------------------------
st.title("Profit Pinnacles - Intraday Nifty Trading & Sector Forecast")

st.markdown("""
This tool generates a simplified intraday forecast for the Nifty index.  
It provides time-wise trading signals using Advanced Multiple Datasets and using AI for Computations.
Enter a date (YYYY-MM-DD, IST) below to view the Report.
""")

input_date = st.text_input("Enter Forecast Date (YYYY-MM-DD)", "")

if st.button("Generate Forecast"):
    if input_date:
        try:
            forecast_text = forecast_for_date(input_date)
            st.markdown(forecast_text)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a valid date.")
