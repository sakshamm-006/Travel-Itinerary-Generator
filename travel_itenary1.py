import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium
from style import CSS_STYLE, MAIN_TITLE_HTML, SIDEBAR_HEADER_HTML, get_stats_card, get_activity_card, get_activity_styling, DAY_COLORS, get_day_color_indicator, get_section_header

st.set_page_config(page_title="Smart Travel Itinerary", layout="wide")

# ================= SESSION INIT =================
if "itinerary" not in st.session_state:
    st.session_state.itinerary = None

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_excel("DataSet_Travel_Itenary.xlsx")

    df = df.rename(columns={
        "state": "State",
        "city": "City",
        "place_name": "Place",
        "place_type": "Category",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "avg_visit_duration_hr": "Visit_Duration",
        "opening_time_24h": "Open_Time",
        "closing_time_24h": "Close_Time",
        "visit_priority": "Priority",
        "budget_category": "Budget"
    })

    df["Category"] = df["Category"].astype(str).str.lower()
    df["Priority"] = pd.to_numeric(df["Priority"], errors="coerce").fillna(3)
    return df

df = load_data()

# ================= BUDGET =================
def normalize_budget(x):
    x = str(x).lower()
    if "low" in x:
        return "low"
    if "medium" in x:
        return "medium"
    return "high"

df["Budget_Normalized"] = df["Budget"].apply(normalize_budget)

def filter_by_budget(df_city, user_budget):
    if user_budget == "low":
        return df_city[df_city.Budget_Normalized == "low"]
    if user_budget == "medium":
        return df_city[df_city.Budget_Normalized.isin(["low", "medium"])]
    return df_city

# ================= HELPERS =================
def travel_hours(km):
    return round(km / 35, 2)

def intra_city_travel_time(p1, p2):
    km = geodesic((p1.Latitude, p1.Longitude), (p2.Latitude, p2.Longitude)).km
    return max(0.25, round(km / 30, 2))

def filter_by_companion(df_city, who):
    if who == "family":
        banned = ["pub", "bar", "club", "nightlife"]
        return df_city[~df_city.Category.str.contains('|'.join(banned), case=False)]
    return df_city

def city_center(city):
    r = df[df.City == city].iloc[0]
    return (r.Latitude, r.Longitude)

def get_next_city(current_city, visited, exhausted_cities):
    base = city_center(current_city)

    temp = df[
        (~df.Place.isin(visited)) &
        (~df.City.isin(exhausted_cities)) &
        (df.City != current_city)
    ].copy()

    if temp.empty:
        return None

    temp["dist"] = temp.apply(
        lambda r: geodesic(base, (r.Latitude, r.Longitude)).km,
        axis=1
    )

    for level in [4, 2]:
        c = temp[temp.Priority >= level]
        if not c.empty:
            return c.sort_values("dist").iloc[0].City

    return None

# ================= MAP BUILDER =================
def build_itinerary_map(itinerary, df):
    first = None
    for acts in itinerary.values():
        for a in acts:
            row = df[df.Place == a["Place"]]
            if not row.empty:
                first = [row.iloc[0].Latitude, row.iloc[0].Longitude]
                break
        if first:
            break

    if not first:
        return None

    m = folium.Map(location=first, zoom_start=11, tiles="OpenStreetMap")
    
    # Add day color legend to map
    legend_html = """
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 180px; height: auto;
                background-color: white; 
                padding: 10px; 
                border-radius: 5px;
                color: black;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                z-index: 9999;
                font-size: 0.9rem;">
        <div style="font-weight: bold; margin-bottom: 8px; border-bottom: 1px solid #ddd; padding-bottom: 5px;">Day Colors</div>
    """
    
    for i, day in enumerate(itinerary.keys()):
        color = DAY_COLORS[i % len(DAY_COLORS)]
        legend_html += f"""
        <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <div style="width: 12px; height: 12px; background-color: {color}; 
                       border-radius: 50%; margin-right: 8px; border: 1px solid #666;"></div>
            <span style="font-size: 0.85rem;">{day}</span>
        </div>
        """
    
    legend_html += "</div>"
    
    m.get_root().html.add_child(folium.Element(legend_html))

    for i, (day, acts) in enumerate(itinerary.items()):
        coords = []
        color = DAY_COLORS[i % len(DAY_COLORS)]
        stop = 1

        for a in acts:
            row = df[df.Place == a["Place"]]
            if row.empty:
                continue

            lat, lon = row.iloc[0].Latitude, row.iloc[0].Longitude
            coords.append((lat, lon))

            folium.Marker(
                [lat, lon],
                popup=f"""
                <div style="font-family: Arial, sans-serif;">
                    <div style="font-weight: bold; color: {color}; font-size: 14px;">{day}</div>
                    <div style="font-size: 12px; margin: 5px 0;">📍 {a['Place']}</div>
                    <div style="font-size: 11px; color: #666;">🕐 {a['Time']}</div>
                </div>
                """,
                icon=folium.DivIcon(
                    html=f"""
                    <div style="
                        background:{color};
                        color:white;
                        border-radius:50%;
                        width:26px;
                        height:26px;
                        line-height:26px;
                        text-align:center;
                        font-weight:bold;
                        border: 2px solid white;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                        font-size: 12px;
                    ">{stop}</div>
                    """
                )
            ).add_to(m)
            stop += 1

        if len(coords) > 1:
            folium.PolyLine(coords, color=color, weight=4, opacity=0.7, dash_array='5, 5' if 'travel' in day.lower() else None).add_to(m)

    return m

# ================= UI =================
# Apply CSS styles
st.markdown(CSS_STYLE, unsafe_allow_html=True)

# Main title with gradient effect
st.markdown(MAIN_TITLE_HTML, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(SIDEBAR_HEADER_HTML, unsafe_allow_html=True)
    
    state = st.selectbox("Select State", sorted(df.State.unique()))
    city = st.selectbox("Select City", sorted(df[df.State == state].City.unique()))
    days = st.slider("Number of Days", 1, 10, 4)
    budget = st.selectbox("Budget", ["low", "medium", "high"])
    with_whom = st.selectbox("Travelling With", ["family", "friends", "solo"])
    
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.time_input("Day Start", datetime.strptime("09:00", "%H:%M"))
    with col2:
        end_time = st.time_input("Day End", datetime.strptime("21:00", "%H:%M"))

    if st.button("Generate Itinerary", use_container_width=True):
        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)

        visited = set()
        exhausted_cities = set()
        itinerary = {}
        current_city = city

        for d in range(1, days + 1):
            cur = start_dt
            day_plan = []
            last_place = None
            meals = {"breakfast": False, "lunch": False, "dinner": False}

            while cur < end_dt:
                if cur.hour < 9 and not meals["breakfast"]:
                    day_plan.append({"Place": "Breakfast", "Category": "food",
                                     "Time": f"{cur.strftime('%H:%M')} - 09:00"})
                    cur = cur.replace(hour=9, minute=0)
                    meals["breakfast"] = True
                    continue

                if 12 <= cur.hour < 14 and not meals["lunch"]:
                    day_plan.append({"Place": "Lunch", "Category": "food",
                                     "Time": f"{cur.strftime('%H:%M')} - {(cur + timedelta(hours=1)).strftime('%H:%M')}"})
                    cur += timedelta(hours=1)
                    meals["lunch"] = True
                    continue

                if cur.hour >= 19 and not meals["dinner"]:
                    start = max(cur, cur.replace(hour=19, minute=30))
                    end = start + timedelta(hours=1)
                    day_plan.append({"Place": "Dinner", "Category": "food",
                                     "Time": f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}"})
                    cur = end
                    meals["dinner"] = True
                    continue

                pool = df[df.City == current_city]
                pool = filter_by_companion(pool, with_whom)
                pool = filter_by_budget(pool, budget)
                pool = pool[~pool.Place.isin(visited)]

                if pool.empty:
                    exhausted_cities.add(current_city)
                    next_city = get_next_city(current_city, visited, exhausted_cities)
                    if not next_city:
                        break

                    km = geodesic(city_center(current_city), city_center(next_city)).km
                    hrs = travel_hours(km)

                    day_plan.append({
                        "Place": f"Travel: {current_city} → {next_city}",
                        "Category": "travel_city",
                        "Time": f"{cur.strftime('%H:%M')} - {(cur + timedelta(hours=hrs)).strftime('%H:%M')}"
                    })

                    cur += timedelta(hours=hrs)
                    current_city = next_city
                    last_place = None
                    continue

                nxt = pool.sort_values("Priority", ascending=False).iloc[0]

                if last_place is not None:
                    t = intra_city_travel_time(last_place, nxt)
                    day_plan.append({
                        "Place": f"Travel: {last_place.Place} → {nxt.Place}",
                        "Category": "travel_place",
                        "Time": f"{cur.strftime('%H:%M')} - {(cur + timedelta(hours=t)).strftime('%H:%M')}"
                    })
                    cur += timedelta(hours=t)

                visit_hr = nxt.Visit_Duration if nxt.Visit_Duration > 0 else 2
                end_visit = cur + timedelta(hours=visit_hr)
                if end_visit > end_dt:
                    break

                day_plan.append({
                    "Place": nxt.Place,
                    "Category": nxt.Category,
                    "Time": f"{cur.strftime('%H:%M')} - {end_visit.strftime('%H:%M')}"
                })

                visited.add(nxt.Place)
                last_place = nxt
                cur = end_visit

            itinerary[f"Day {d}"] = day_plan

        st.session_state.itinerary = itinerary

# ================= DISPLAY =================
if st.session_state.itinerary:
    # Map section
    st.markdown(get_section_header("🗺️", "Trip Overview Map"), unsafe_allow_html=True)
    trip_map = build_itinerary_map(st.session_state.itinerary, df)
    if trip_map:
        st_folium(trip_map, width=1200, height=500, key="map")
    
    # Day color indicators
    st.markdown("**Day Color Key on Map:**")
    day_cols = st.columns(len(st.session_state.itinerary))
    for i, (day, col) in enumerate(zip(st.session_state.itinerary.keys(), day_cols)):
        color = DAY_COLORS[i % len(DAY_COLORS)]
        with col:
            st.markdown(get_day_color_indicator(day, color), unsafe_allow_html=True)
    
    st.markdown("---")

    # Trip Statistics
    st.markdown(get_section_header("📊", "Trip Overview"), unsafe_allow_html=True)
    cols = st.columns(4)
    
    total_places = sum(len(day_plan) for day_plan in st.session_state.itinerary.values())
    total_meals = sum(1 for day_plan in st.session_state.itinerary.values() 
                      for activity in day_plan if activity["Category"] == "food")
    total_travel = sum(1 for day_plan in st.session_state.itinerary.values() 
                       for activity in day_plan if "travel" in activity["Category"])
    total_days = len(st.session_state.itinerary)
    
    with cols[0]:
        st.markdown(get_stats_card(total_places, "Total Activities"), unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(get_stats_card(total_meals, "Meal Breaks"), unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown(get_stats_card(total_travel, "Travel Segments"), unsafe_allow_html=True)
    
    with cols[3]:
        st.markdown(get_stats_card(total_days, "Days"), unsafe_allow_html=True)

    # Activity Legend
    st.markdown(get_section_header("🎨", "Activity Legend"), unsafe_allow_html=True)
    
    legend_cols = st.columns(2)
    
    with legend_cols[0]:
        st.markdown("**Activity Types:**", unsafe_allow_html=True)
        st.markdown('<div class="category-badge sightseeing-badge" style="margin-bottom: 8px;">📍 Sightseeing</div>', unsafe_allow_html=True)
        st.markdown('<div class="category-badge meal-badge" style="margin-bottom: 8px;">🍽️ Meal Break</div>', unsafe_allow_html=True)
        st.markdown('<div class="category-badge travel-badge" style="margin-bottom: 8px;">🚌 City Travel</div>', unsafe_allow_html=True)
        st.markdown('<div class="category-badge travel-badge" style="margin-bottom: 8px;">🚗 Local Travel</div>', unsafe_allow_html=True)
    
    with legend_cols[1]:
        st.markdown("**Map Markers:**", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size: 0.9rem; color: #666;">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <div style="width: 20px; height: 20px; background-color: #FFD700; border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; 
                            margin-right: 8px; color: #333; font-weight: bold; font-size: 10px;">1</div>
                <span>Number indicates activity order for each day</span>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <div style="width: 12px; height: 12px; background-color: #FFD700; border-radius: 50%; 
                            margin-right: 8px;"></div>
                <span>Circle color represents the day</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 100%; height: 2px; background-color: #FFD700; margin-right: 8px;"></div>
                <span>Lines connect activities in sequence</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Enhanced Itinerary Display
    st.markdown(get_section_header("📅", "Detailed Itinerary"), unsafe_allow_html=True)
    
    for i, (day, acts) in enumerate(st.session_state.itinerary.items()):
        day_color = DAY_COLORS[i % len(DAY_COLORS)]
        
        # Day header with expander
        with st.expander(f"**{day}** - {len(acts)} activities • Estimated time: {len(acts)*2} hours", expanded=True):
            
            for a in acts:
                emoji, badge_html, card_class = get_activity_styling(a)
                st.markdown(get_activity_card(a['Place'], a['Time'], emoji, badge_html, card_class), unsafe_allow_html=True)
        
        st.markdown("")