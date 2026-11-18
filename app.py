
import streamlit as st
import requests
import html


# ==================================
# PAGE CONFIGURATION
# ==================================

st.set_page_config(
    page_title="Weather Outfit",
    page_icon="🌤️",
    layout="wide"
)


# ==================================
# WEATHER API FUNCTIONS
# ==================================

def get_weather(city):
    try:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return None

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "")

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,weather_code",
            "timezone": "auto"
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current"]

        temperature = current["temperature_2m"]
        weather_code = current["weather_code"]

        if weather_code == 0:
            condition = "Sunny"

        elif weather_code in [1, 2, 3, 45, 48]:
            condition = "Cloudy"

        elif weather_code in [
            51, 53, 55, 56, 57,
            61, 63, 65, 66, 67,
            71, 73, 75, 77,
            80, 81, 82, 85, 86,
            95, 96, 99
        ]:
            condition = "Rainy"

        else:
            condition = "Cloudy"

        return {
            "city": city_name,
            "country": country,
            "temperature": temperature,
            "weather": condition
        }

    except requests.exceptions.RequestException:
        return "connection_error"


# ==================================
# CUSTOM CSS
# ==================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.stApp {
    background-color: #F8F5F0;
    color: #514438;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background-color: transparent;
}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

h1, h2, h3 {
    color: #514438 !important;
}

/* HEADER */

.hero-header {
    position: relative;
    overflow: hidden;
    background: linear-gradient(
        120deg,
        #EDE2D5 0%,
        #D9C5AE 100%
    );
    border: 1px solid #E3D4C3;
    border-radius: 24px;
    padding: 38px 40px;
    margin: 5px 0 30px 0;
}

.hero-header:after {
    content: "☀";
    position: absolute;
    right: 45px;
    top: -35px;
    font-size: 160px;
    color: rgba(255, 255, 255, 0.34);
    transform: rotate(12deg);
    pointer-events: none;
}

.hero-kicker {
    color: #8A725C;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2.2px;
    margin-bottom: 12px;
}

.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 46px;
    line-height: 1.2;
    font-weight: 700;
    color: #514438;
    margin-bottom: 10px;
}

.subtitle {
    color: #766452;
    font-size: 15px;
    line-height: 1.7;
    max-width: 520px;
}

.hero-tag {
    display: inline-block;
    margin-top: 20px;
    padding: 8px 15px;
    border: 1px solid rgba(128, 107, 88, 0.28);
    border-radius: 30px;
    color: #6F5A47;
    font-size: 11px;
    letter-spacing: 0.7px;
    background: rgba(255, 255, 255, 0.35);
}

/* SECTION */

.section-title {
    font-size: 21px;
    font-weight: 700;
    color: #514438;
    margin-top: 22px;
    margin-bottom: 12px;
}

/* WEATHER CARD */

.weather-card {
    background: linear-gradient(
        120deg,
        #E9DED0,
        #D8C5AF
    );
    border-radius: 18px;
    padding: 26px;
    color: #514438;
    margin: 15px 0 22px 0;
}

.weather-label {
    font-size: 13px;
    color: #766452;
    letter-spacing: 1px;
    font-weight: 600;
}

.weather-temp {
    font-size: 46px;
    font-weight: 700;
    margin: 5px 0;
}

.weather-location {
    color: #766452;
    font-size: 14px;
    margin-top: 5px;
}

.temperature-tag {
    display: inline-block;
    margin-top: 12px;
    padding: 6px 12px;
    border-radius: 20px;
    background: #F1E8DE;
    color: #806B58;
    font-size: 12px;
    font-weight: 600;
}

/* INFORMATION CARD */

.info-card {
    background-color: #FFFFFF;
    border: 1px solid #EAE1D7;
    border-radius: 15px;
    padding: 22px;
    min-height: 110px;
}

.info-label {
    color: #9A8878;
    font-size: 13px;
    margin-bottom: 9px;
}

.info-value {
    color: #514438;
    font-size: 17px;
    font-weight: 600;
}

/* RECOMMENDATION */

.recommendation-title {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    color: #514438;
    margin: 28px 0 5px 0;
}

.recommendation-subtitle {
    color: #958576;
    font-size: 14px;
    margin-bottom: 20px;
}

/* CLOTHING CARD */

.clothing-card {
    background-color: #FFFFFF;
    border: 1px solid #EAE1D7;
    border-radius: 16px;
    padding: 22px 12px;
    min-height: 165px;
    text-align: center;
}

.clothing-icon {
    font-size: 36px;
    margin-bottom: 13px;
}

.clothing-label {
    color: #A08D7C;
    font-size: 12px;
    margin-bottom: 9px;
    font-weight: 600;
    letter-spacing: 1px;
}

.clothing-name {
    color: #514438;
    font-size: 14px;
    font-weight: 600;
    line-height: 1.5;
}

/* STYLE NOTE */

.outfit-note {
    background-color: #EFE7DD;
    border-radius: 12px;
    padding: 19px;
    color: #685746;
    margin-top: 20px;
    font-size: 14px;
    line-height: 1.8;
}

/* BUTTON */

.stButton > button {
    background-color: #806B58;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    width: 100%;
}

.stButton > button:hover {
    background-color: #665341;
    color: white;
}

/* INPUT */

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background-color: #FFFFFF;
    border-color: #E5D9CC;
    border-radius: 10px;
}

hr {
    border-color: #E8DED3;
}

</style>
""", unsafe_allow_html=True)


# ==================================
# HEADER
# ==================================

st.html("""
<div class="hero-header">

    <div class="hero-kicker">
        YOUR DAILY STYLE COMPANION
    </div>

    <div class="main-title">
        Weather Outfit
    </div>

    <div class="subtitle">
        Find an outfit that feels right for the weather
        and whatever your day has planned.
    </div>

    <div class="hero-tag">
        ☁ WEATHER-BASED OUTFIT GUIDE
        &nbsp; · &nbsp;
        ✦ DAILY INSPIRATION
    </div>

</div>
""")


# ==================================
# SESSION STATE
# ==================================

if "auto_weather" not in st.session_state:
    st.session_state.auto_weather = None

if "show_recommendation" not in st.session_state:
    st.session_state.show_recommendation = False


# ==================================
# WEATHER INPUT
# ==================================

st.html("""
<div class="section-title">
    Weather Information
</div>
""")

mode = st.radio(
    "Choose weather source",
    ["Manual", "Automatic"],
    horizontal=True
)

weather = None
temperature = None
city_name = "Your Location"


# ==================================
# MANUAL MODE
# ==================================

if mode == "Manual":

    col1, col2 = st.columns(2)

    with col1:
        weather = st.selectbox(
            "Weather condition",
            ["Sunny", "Cloudy", "Rainy", "Windy"]
        )

    with col2:
        temperature = st.number_input(
            "Temperature (°C)",
            min_value=-10,
            max_value=60,
            value=25
        )

    if st.button("Find My Outfit"):
        st.session_state.show_recommendation = True


# ==================================
# AUTOMATIC MODE
# ==================================

else:

    city = st.text_input(
        "Enter your city",
        placeholder="Example: Surabaya"
    )

    if st.button("Get Current Weather"):

        if not city.strip():
            st.warning("Please enter your city name.")

        else:
            with st.spinner("Getting current weather..."):

                result = get_weather(city.strip())

            if result is None:

                st.session_state.auto_weather = None
                st.session_state.show_recommendation = False

                st.error(
                    "City not found. Please try another city."
                )

            elif result == "connection_error":

                st.error(
                    "Unable to connect to weather service."
                )

            else:

                st.session_state.auto_weather = result
                st.session_state.show_recommendation = True

    if st.session_state.auto_weather is not None:

        weather_data = st.session_state.auto_weather

        weather = weather_data["weather"]
        temperature = weather_data["temperature"]

        city_name = weather_data["city"]

        if weather_data["country"]:
            city_name += ", " + weather_data["country"]

        st.success(
            f"Weather data for {city_name} successfully retrieved!"
        )

        st.write(f"Current temperature: **{temperature}°C**")
        st.write(f"Weather condition: **{weather}**")


# ==================================
# ACTIVITY SELECTION
# ==================================

st.html("""
<div class="section-title">
    Your Activity
</div>
""")

activity = st.selectbox(
    "What are you going to do?",
    [
        "College",
        "Casual Outing",
        "Outdoor Activities"
    ]
)


# ==================================
# OUTFIT RECOMMENDATION
# ==================================

st.divider()

st.html("""
<div class="section-title">
    Outfit Recommendation
</div>
""")


if weather is not None and temperature is not None:

    if mode == "Automatic":
        show_result = st.session_state.show_recommendation

    else:
        show_result = st.session_state.show_recommendation

    if show_result:

        # ==================================
        # 1. TEMPERATURE CATEGORY
        # ==================================

        if temperature < 20:

            temperature_category = "Very Cold"

            top = "Sweater / Thick Knitwear"
            outer = "Warm Jacket"
            bottom = "Thick Long Pants"
            shoes = "Closed Shoes"

        elif temperature <= 23:

            temperature_category = "Cool"

            top = "Knitwear / Long-sleeve Top"
            outer = "Light Jacket"
            bottom = "Long Pants"
            shoes = "Sneakers"

        elif temperature <= 27:

            temperature_category = "Mild"

            top = "T-shirt / Casual Blouse"
            outer = "Light Cardigan"
            bottom = "Straight Pants"
            shoes = "Casual Sneakers"

        elif temperature <= 31:

            temperature_category = "Warm"

            top = "Lightweight Shirt"
            outer = "No Outerwear"
            bottom = "Lightweight Pants"
            shoes = "Breathable Sneakers"

        else:

            temperature_category = "Hot"

            top = "Breathable Cotton / Linen Top"
            outer = "No Outerwear"
            bottom = "Airy Wide-leg Pants"
            shoes = "Breathable Shoes"


        # ==================================
        # 2. ACTIVITY ADJUSTMENT
        # ==================================

        if activity == "College":

            if temperature < 20:
                top = "Neat Knitwear"

            elif temperature <= 23:
                top = "Long-sleeve Blouse"

            elif temperature <= 27:
                top = "Neat Blouse"

            elif temperature <= 31:
                top = "Casual Shirt or Blouse"

            else:
                top = "Lightweight Cotton Shirt"

            bottom = "Straight Pants"

            shoes = (
                "Closed Shoes"
                if temperature < 20
                else "Casual Sneakers"
            )


        elif activity == "Casual Outing":

            if temperature < 20:

                top = "Cozy Knitwear"
                bottom = "Long Pants"

            elif temperature <= 23:

                top = "Long-sleeve Casual Top"
                bottom = "Jeans"

            elif temperature <= 27:

                top = "Casual Blouse"
                bottom = "Jeans"

            elif temperature <= 31:

                top = "Casual T-shirt"
                bottom = "Wide-leg Pants"

            else:

                top = "Lightweight Casual Top"
                bottom = "Linen / Wide-leg Pants"

            shoes = (
                "Closed Shoes"
                if temperature < 20
                else "Flats or Casual Sneakers"
            )


        elif activity == "Outdoor Activities":

            if temperature < 20:
                top = "Thermal / Warm Sportswear"

            elif temperature <= 23:
                top = "Long-sleeve Sportswear"

            elif temperature <= 27:
                top = "Comfortable Activewear"

            elif temperature <= 31:
                top = "Breathable Sportswear"

            else:
                top = "Lightweight Quick-dry Sportswear"

            bottom = "Jogger Pants"

            shoes = "Walking Shoes"


        # ==================================
        # 3. WEATHER ADJUSTMENT
        # ==================================

        if weather == "Rainy":

            outer = "Waterproof Jacket"
            shoes = "Water-resistant Shoes"

        elif weather == "Windy":

            if temperature < 20:
                outer = "Warm Windproof Jacket"
            else:
                outer = "Light Windbreaker"

        elif weather == "Sunny":

            if temperature >= 24:
                outer = "No Outerwear Needed"


        # ==================================
        # 4. WEATHER SUMMARY
        # ==================================

        safe_city = html.escape(city_name)

        st.html(f"""
        <div class="weather-card">

            <div class="weather-label">
                YOUR WEATHER TODAY
            </div>

            <div class="weather-temp">
                {temperature}°C
            </div>

            <div>
                {weather} Weather
            </div>

            <div class="weather-location">
                📍 {safe_city}
            </div>

            <div class="temperature-tag">
                {temperature_category} Temperature
            </div>

        </div>
        """)


        # ==================================
        # 5. ACTIVITY INFORMATION
        # ==================================

        col1, col2 = st.columns(2)

        with col1:

            st.html(f"""
            <div class="info-card">

                <div class="info-label">
                    Your Activity
                </div>

                <div class="info-value">
                    {activity}
                </div>

            </div>
            """)

        with col2:

            st.html(f"""
            <div class="info-card">

                <div class="info-label">
                    Weather & Temperature
                </div>

                <div class="info-value">
                    {weather} · {temperature_category}
                </div>

            </div>
            """)


        # ==================================
        # 6. RECOMMENDATION HEADING
        # ==================================

        st.html("""
        <div class="recommendation-title">
            Your Suggested Outfit
        </div>

        <div class="recommendation-subtitle">
            A comfortable outfit for your daily activities.
        </div>
        """)


        # ==================================
        # 7. CLOTHING CARDS
        # ==================================

        clothing_items = [
            ("👕", "TOP", top),
            ("🧥", "OUTERWEAR", outer),
            ("👖", "BOTTOM", bottom),
            ("👟", "FOOTWEAR", shoes)
        ]

        columns = st.columns(4)

        for column, item in zip(columns, clothing_items):

            icon, label, name = item

            with column:

                st.html(f"""
                <div class="clothing-card">

                    <div class="clothing-icon">
                        {icon}
                    </div>

                    <div class="clothing-label">
                        {label}
                    </div>

                    <div class="clothing-name">
                        {name}
                    </div>

                </div>
                """)


        # ==================================
        # 8. TEMPERATURE TIPS
        # ==================================

        if temperature < 20:

            temperature_tip = (
                "Layer your outfit and choose "
                "warm, comfortable fabrics."
            )

        elif temperature <= 23:

            temperature_tip = (
                "A light extra layer can keep "
                "you comfortable."
            )

        elif temperature <= 27:

            temperature_tip = (
                "A light and flexible outfit "
                "should work well."
            )

        elif temperature <= 31:

            temperature_tip = (
                "Choose breathable fabrics "
                "to stay comfortable."
            )

        else:

            temperature_tip = (
                "Choose loose, airy fabrics "
                "and stay hydrated."
            )


        # ==================================
        # 9. WEATHER TIPS
        # ==================================

        if weather == "Rainy":

            note = (
                "Bring an umbrella and choose "
                "water-resistant footwear."
            )

        elif weather == "Sunny":

            note = (
                "Stay comfortable and consider "
                "bringing sunglasses."
            )

        elif weather == "Windy":

            note = (
                "A lightweight windbreaker can help "
                "protect you from the wind."
            )

        else:

            note = (
                "Choose comfortable layers to stay "
                "cozy throughout the day."
            )


        # ==================================
        # 10. STYLE NOTE
        # ==================================

        st.html(f"""
        <div class="outfit-note">

            <b>Temperature Tip · {temperature_category}</b>
            <br>

            {temperature_tip}

            <br><br>

            <b>Weather Note</b>
            <br>

            {note}

        </div>
        """)

        st.success(
            "Your outfit recommendation is ready!"
        )


elif mode == "Automatic" and st.session_state.auto_weather is None:

    st.info(
        "Enter your city and click Get Current Weather "
        "to see your outfit recommendation."
    )

else:

    st.info(
        "Click Find My Outfit to get your outfit recommendation."
    )


# ==================================
# FOOTER
# ==================================

st.divider()

st.html("""
<div style="
    text-align: center;
    color: #A39384;
    font-size: 12px;
    padding: 10px 0;
">
    Weather Outfit · Dress comfortably, whatever the weather.
</div>
""")
