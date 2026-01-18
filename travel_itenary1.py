import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium
import requests
import time
from style import CSS_STYLE, MAIN_TITLE_HTML, SIDEBAR_HEADER_HTML, get_stats_card, get_activity_card, get_activity_styling, DAY_COLORS, get_day_color_indicator, get_section_header, get_traffic_badge, get_delay_badge, get_distance_badge

st.set_page_config(page_title="Smart Travel Itinerary", layout="wide")

# -------Session init-------------
if "itinerary" not in st.session_state:
    st.session_state.itinerary = None

#-------Your API Key--------------
DEFAULT_API_KEY = "AIzaSyAQlGmMpr-oq_ZL0U0khgECyZZPrK-WQww"

# ----------Helps in loading the data----------- 
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

#----------Budget for the itinerary-------------
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

# -------------Travel time helper with live traffic API-------------- 
class TrafficAwareTravelCalculator:
    def __init__(self, api_key=None, mode="driving"):
        self.api_key = api_key
        self.mode = mode
        self.cache = {}
        self.use_api = api_key is not None and api_key.strip() != ""
        self.api_status = "Not configured" if not self.use_api else "Ready"
        self.total_api_calls = 0
        self.successful_api_calls = 0
        
    def get_traffic_level(self, duration_seconds, duration_in_traffic_seconds=None):
        """Determine traffic level based on traffic delay"""
        if duration_in_traffic_seconds is None:
            return "Unknown", 0
        
        delay_percentage = ((duration_in_traffic_seconds - duration_seconds) / duration_seconds) * 100
        
        if delay_percentage < 5:
            return "Light Traffic", delay_percentage
        elif delay_percentage < 20:
            return "Moderate Traffic", delay_percentage
        elif delay_percentage < 50:
            return "Heavy Traffic", delay_percentage
        else:
            return "Severe Traffic", delay_percentage
    
    def get_traffic_emoji(self, traffic_level):
        """Get emoji for traffic level"""
        traffic_emojis = {
            "Light Traffic": "🟢",
            "Moderate Traffic": "🟡", 
            "Heavy Traffic": "🟠",
            "Severe Traffic": "🔴",
            "Unknown": "⚫"
        }
        return traffic_emojis.get(traffic_level, "⚫")
    
    def get_travel_time_with_traffic(self, origin_lat, origin_lon, dest_lat, dest_lon, departure_time="now"):
        """Get travel time with live traffic data from API"""
        
        # Create cache key
        cache_key = f"{origin_lat},{origin_lon}_{dest_lat},{dest_lon}"
        
        # Check cache (valid for 15 minutes for traffic data)
        if cache_key in self.cache:
            cached_time, cached_result = self.cache[cache_key]
            if time.time() - cached_time < 900:  # 15 minutes
                return cached_result
        
        if not self.use_api:
            return {
                "success": False,
                "error": "API not configured",
                "hours": None,
                "text": "No traffic data",
                "traffic_level": "Unknown",
                "traffic_emoji": "⚫",
                "delay_percentage": 0
            }
        
        try:
            # Google Maps Distance Matrix API endpoint
            url = "https://maps.googleapis.com/maps/api/distancematrix/json"
            
            params = {
                "origins": f"{origin_lat},{origin_lon}",
                "destinations": f"{dest_lat},{dest_lon}",
                "mode": self.mode,
                "departure_time": departure_time,
                "traffic_model": "best_guess",
                "key": self.api_key,
                "units": "metric"
            }
            
            self.total_api_calls += 1
            response = requests.get(url, params=params, timeout=15)
            data = response.json()
            
            if data["status"] == "OK":
                element = data["rows"][0]["elements"][0]
                
                if element["status"] == "OK":
                    # Get normal duration
                    normal_duration_seconds = element["duration"]["value"]
                    
                    # Get duration with traffic if available
                    if "duration_in_traffic" in element:
                        traffic_duration_seconds = element["duration_in_traffic"]["value"]
                        traffic_text = element["duration_in_traffic"]["text"]
                        has_traffic_data = True
                    else:
                        traffic_duration_seconds = normal_duration_seconds
                        traffic_text = element["duration"]["text"]
                        has_traffic_data = False
                    
                    # Calculate traffic level
                    traffic_level, delay_percentage = self.get_traffic_level(
                        normal_duration_seconds, 
                        traffic_duration_seconds if has_traffic_data else None
                    )
                    
                    # Get traffic emoji
                    traffic_emoji = self.get_traffic_emoji(traffic_level)
                    
                    # Convert to hours
                    travel_time_hours = traffic_duration_seconds / 3600
                    
                    # Get distance if available
                    distance_km = element.get("distance", {}).get("value", 0) / 1000 if "distance" in element else None
                    
                    result = {
                        "success": True,
                        "hours": travel_time_hours,
                        "text": traffic_text,
                        "distance_km": distance_km,
                        "traffic_level": traffic_level,
                        "traffic_emoji": traffic_emoji,
                        "delay_percentage": delay_percentage,
                        "has_traffic_data": has_traffic_data,
                        "normal_duration_text": element["duration"]["text"],
                        "traffic_duration_text": traffic_text
                    }
                    
                    # Cache the result
                    self.cache[cache_key] = (time.time(), result)
                    self.successful_api_calls += 1
                    
                    return result
                    
                else:
                    self.api_status = f"Route error: {element.get('status', 'Unknown')}"
                    return {
                        "success": False,
                        "error": element.get('status', 'Route not found'),
                        "hours": None,
                        "text": "Route not available",
                        "traffic_level": "Unknown",
                        "traffic_emoji": "⚫",
                        "delay_percentage": 0
                    }
                    
            elif data["status"] == "REQUEST_DENIED":
                error_msg = data.get('error_message', 'API key invalid or missing required permissions')
                self.api_status = f"API denied: {error_msg}"
                return {
                    "success": False,
                    "error": error_msg,
                    "hours": None,
                    "text": "API access denied",
                    "traffic_level": "Unknown",
                    "traffic_emoji": "⚫",
                    "delay_percentage": 0
                }
                
            else:
                error_msg = data.get('error_message', data['status'])
                self.api_status = f"API Error: {error_msg}"
                return {
                    "success": False,
                    "error": error_msg,
                    "hours": None,
                    "text": "API error",
                    "traffic_level": "Unknown",
                    "traffic_emoji": "⚫",
                    "delay_percentage": 0
                }
                
        except requests.exceptions.Timeout:
            self.api_status = "API timeout"
            return {
                "success": False,
                "error": "Request timeout",
                "hours": None,
                "text": "Network timeout",
                "traffic_level": "Unknown",
                "traffic_emoji": "⚫",
                "delay_percentage": 0
            }
            
        except requests.exceptions.RequestException as e:
            self.api_status = f"Network error: {str(e)}"
            return {
                "success": False,
                "error": str(e),
                "hours": None,
                "text": "Network error",
                "traffic_level": "Unknown",
                "traffic_emoji": "⚫",
                "delay_percentage": 0
            }
            
        except Exception as e:
            self.api_status = f"Error: {str(e)}"
            return {
                "success": False,
                "error": str(e),
                "hours": None,
                "text": "Unknown error",
                "traffic_level": "Unknown",
                "traffic_emoji": "⚫",
                "delay_percentage": 0
            }
    
    def get_travel_time(self, origin_lat, origin_lon, dest_lat, dest_lon, travel_type="intra_city"):
        """Get travel time using API with live traffic - NO FALLBACK"""
        
        # Always try API first
        api_result = self.get_travel_time_with_traffic(origin_lat, origin_lon, dest_lat, dest_lon)
        
        if api_result["success"]:
            return api_result
        else:
            # If API fails, calculate distance and provide estimate
            km = geodesic((origin_lat, origin_lon), (dest_lat, dest_lon)).km
            
            # Basic speed estimates (no traffic data)
            if travel_type == "inter_city":
                speed = 60  # Highway speed
            else:
                speed = 30  # City speed
            
            travel_time_hours = km / speed
            hours = int(travel_time_hours)
            minutes = int((travel_time_hours - hours) * 60)
            
            if hours > 0:
                text = f"{hours}h {minutes}min (estimated)"
            else:
                text = f"{minutes} min (estimated)"
            
            return {
                "success": False,
                "error": api_result["error"],
                "hours": travel_time_hours,
                "text": text,
                "distance_km": km,
                "traffic_level": "No Traffic Data",
                "traffic_emoji": "⚫",
                "delay_percentage": 0,
                "has_traffic_data": False,
                "normal_duration_text": text,
                "traffic_duration_text": text
            }
    
    def get_api_stats(self):
        """Get API statistics"""
        success_rate = (self.successful_api_calls / self.total_api_calls * 100) if self.total_api_calls > 0 else 0
        return {
            "total_calls": self.total_api_calls,
            "successful_calls": self.successful_api_calls,
            "success_rate": success_rate,
            "cache_size": len(self.cache),
            "status": self.api_status
        }

# Initialize traffic-aware travel calculator
travel_calculator = TrafficAwareTravelCalculator(api_key=DEFAULT_API_KEY)

def travel_hours_between_cities(city1, city2):
    """Calculate travel hours between two cities using live traffic API"""
    origin_center = city_center(city1)
    dest_center = city_center(city2)
    
    result = travel_calculator.get_travel_time(
        origin_center[0], origin_center[1],
        dest_center[0], dest_center[1],
        travel_type="inter_city"
    )
    return result

def travel_hours_between_places(place1, place2):
    """Calculate travel hours between two places using live traffic API"""
    result = travel_calculator.get_travel_time(
        place1.Latitude, place1.Longitude,
        place2.Latitude, place2.Longitude,
        travel_type="intra_city"
    )
    return result

# ================= HELPERS =================
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
    
    # API Settings
    st.markdown("---")
    st.markdown("### 🚗 Live Traffic Settings")
    
    # Traffic mode selection
    traffic_mode = st.selectbox(
        "Traffic Calculation Mode",
        ["Live Traffic (Best Guess)", "Live Traffic (Pessimistic)", "Live Traffic (Optimistic)", "No Traffic"],
        index=0,
        help="Choose how traffic is calculated"
    )
    
    # Display API status
    api_stats = travel_calculator.get_api_stats()
    
    status_col1, status_col2 = st.columns([3, 1])
    with status_col1:
        if travel_calculator.use_api:
            st.markdown(f"**API Status:** `{api_stats['status']}`")
        else:
            st.markdown("**API Status:** Not configured")
    
    with status_col2:
        if travel_calculator.use_api and api_stats['total_calls'] > 0:
            success_color = "green" if api_stats['success_rate'] > 80 else "orange" if api_stats['success_rate'] > 50 else "red"
            st.markdown(f"<span style='color: {success_color}; font-weight: bold;'>{api_stats['success_rate']:.0f}%</span>", unsafe_allow_html=True)
    
    # Custom API key option
    custom_api_key = st.text_input(
        "Custom API Key (Optional)", 
        type="password",
        help="Leave empty to use default key, or enter your own",
        value=""
    )
    
    # Use custom key if provided
    if custom_api_key.strip():
        travel_calculator.api_key = custom_api_key
        travel_calculator.use_api = True
        st.info("Using custom API key")
    else:
        travel_calculator.api_key = DEFAULT_API_KEY
        travel_calculator.use_api = True
        st.info("Using default API key")
    
    # Test API connection
    if st.button("Test Traffic API", key="test_api"):
        with st.spinner("Testing API connection..."):
            test_result = travel_calculator.get_travel_time_with_traffic(
                19.0760, 72.8777,  # Mumbai coordinates
                18.5204, 73.8567   # Pune coordinates
            )
            
            if test_result["success"]:
                st.success(f"✅ API Connected! Travel time: {test_result['text']}")
                st.info(f"Traffic: {test_result['traffic_emoji']} {test_result['traffic_level']}")
                if test_result['has_traffic_data'] and test_result['delay_percentage'] > 0:
                    st.info(f"Traffic delay: +{test_result['delay_percentage']:.1f}%")
            else:
                st.error(f"❌ API Error: {test_result['error']}")

    if st.button("Generate Itinerary", use_container_width=True, type="primary"):
        # Configure traffic model based on selection
        if "Pessimistic" in traffic_mode:
            traffic_model = "pessimistic"
        elif "Optimistic" in traffic_mode:
            traffic_model = "optimistic"
        else:
            traffic_model = "best_guess"
        
        # Update departure time for traffic calculations
        departure_time = "now"  # Could be made configurable
        
        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)

        visited = set()
        exhausted_cities = set()
        itinerary = {}
        current_city = city
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Traffic statistics
        traffic_summary = {
            "total_travel_segments": 0,
            "with_traffic_data": 0,
            "traffic_levels": {"Light Traffic": 0, "Moderate Traffic": 0, "Heavy Traffic": 0, "Severe Traffic": 0},
            "total_traffic_delay_minutes": 0
        }

        for d in range(1, days + 1):
            cur = start_dt
            day_plan = []
            last_place = None
            meals = {"breakfast": False, "lunch": False, "dinner": False}
            
            status_text.text(f"Planning Day {d}...")
            progress_bar.progress((d-1)/days)

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

                    # Get travel time with live traffic between cities
                    travel_result = travel_hours_between_cities(current_city, next_city)
                    traffic_summary["total_travel_segments"] += 1
                    
                    if travel_result["success"]:
                        hrs = travel_result["hours"]
                        travel_time_text = travel_result["text"]
                        traffic_level = travel_result["traffic_level"]
                        traffic_emoji = travel_result["traffic_emoji"]
                        has_traffic_data = travel_result["has_traffic_data"]
                        
                        if has_traffic_data:
                            traffic_summary["with_traffic_data"] += 1
                            traffic_summary["traffic_levels"][traffic_level] += 1
                            
                            # Calculate delay in minutes
                            if travel_result["delay_percentage"] > 0:
                                delay_minutes = (hrs * 60 * travel_result["delay_percentage"] / 100)
                                traffic_summary["total_traffic_delay_minutes"] += delay_minutes
                    else:
                        # Fallback if API fails
                        hrs = travel_result["hours"]
                        travel_time_text = travel_result["text"]
                        traffic_level = "No Traffic Data"
                        traffic_emoji = "⚫"
                        has_traffic_data = False

                    day_plan.append({
                        "Place": f"Travel: {current_city} → {next_city}",
                        "Category": "travel_city",
                        "Time": f"{cur.strftime('%H:%M')} - {(cur + timedelta(hours=hrs)).strftime('%H:%M')}",
                        "Travel_Time": travel_time_text,
                        "Traffic_Level": traffic_level,
                        "Traffic_Emoji": traffic_emoji,
                        "Has_Traffic_Data": has_traffic_data,
                        "Delay_Percentage": travel_result.get("delay_percentage", 0),
                        "Distance_km": travel_result.get("distance_km", 0)
                    })

                    cur += timedelta(hours=hrs)
                    current_city = next_city
                    last_place = None
                    continue

                nxt = pool.sort_values("Priority", ascending=False).iloc[0]

                if last_place is not None:
                    # Get travel time with live traffic between places
                    travel_result = travel_hours_between_places(last_place, nxt)
                    traffic_summary["total_travel_segments"] += 1
                    
                    if travel_result["success"]:
                        t = travel_result["hours"]
                        travel_time_text = travel_result["text"]
                        traffic_level = travel_result["traffic_level"]
                        traffic_emoji = travel_result["traffic_emoji"]
                        has_traffic_data = travel_result["has_traffic_data"]
                        
                        if has_traffic_data:
                            traffic_summary["with_traffic_data"] += 1
                            traffic_summary["traffic_levels"][traffic_level] += 1
                            
                            # Calculate delay in minutes
                            if travel_result["delay_percentage"] > 0:
                                delay_minutes = (t * 60 * travel_result["delay_percentage"] / 100)
                                traffic_summary["total_traffic_delay_minutes"] += delay_minutes
                    else:
                        # Fallback if API fails
                        t = travel_result["hours"]
                        travel_time_text = travel_result["text"]
                        traffic_level = "No Traffic Data"
                        traffic_emoji = "⚫"
                        has_traffic_data = False

                    day_plan.append({
                        "Place": f"Travel: {last_place.Place} → {nxt.Place}",
                        "Category": "travel_place",
                        "Time": f"{cur.strftime('%H:%M')} - {(cur + timedelta(hours=t)).strftime('%H:%M')}",
                        "Travel_Time": travel_time_text,
                        "Traffic_Level": traffic_level,
                        "Traffic_Emoji": traffic_emoji,
                        "Has_Traffic_Data": has_traffic_data,
                        "Delay_Percentage": travel_result.get("delay_percentage", 0),
                        "Distance_km": travel_result.get("distance_km", 0)
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
        
        progress_bar.progress(1.0)
        status_text.text("Itinerary generated successfully!")
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()
        
        # Store traffic summary in session state
        st.session_state.traffic_summary = traffic_summary
        st.session_state.itinerary = itinerary

# ================= DISPLAY =================
if st.session_state.itinerary:
    # Show API and traffic status
    api_stats = travel_calculator.get_api_stats()
    
    if travel_calculator.use_api:
        cols = st.columns([3, 1])
        with cols[0]:
            st.success(f"✅ Using live traffic data | API Success Rate: {api_stats['success_rate']:.0f}%")
        with cols[1]:
            st.info(f"API Calls: {api_stats['total_calls']}")
    else:
        st.warning("⚠️ Live traffic data not available. Using estimated travel times.")
    
    # Traffic Summary Section
    if hasattr(st.session_state, 'traffic_summary'):
        traffic_summary = st.session_state.traffic_summary
        
        st.markdown(get_section_header("🚦", "Traffic Analysis"), unsafe_allow_html=True)
        
        traffic_cols = st.columns(4)
        
        with traffic_cols[0]:
            st.markdown(get_stats_card(
                f"{traffic_summary['with_traffic_data']}/{traffic_summary['total_travel_segments']}",
                "Routes with Traffic Data"
            ), unsafe_allow_html=True)
        
        with traffic_cols[1]:
            delay_hours = traffic_summary['total_traffic_delay_minutes'] / 60
            st.markdown(get_stats_card(
                f"{delay_hours:.1f}h",
                "Total Traffic Delay"
            ), unsafe_allow_html=True)
        
        with traffic_cols[2]:
            # Find most common traffic level
            if traffic_summary['traffic_levels']:
                most_common = max(traffic_summary['traffic_levels'].items(), key=lambda x: x[1])
                st.markdown(get_stats_card(
                    most_common[0].split()[0],
                    "Most Common Traffic"
                ), unsafe_allow_html=True)
        
        with traffic_cols[3]:
            avg_delay = (traffic_summary['total_traffic_delay_minutes'] / 
                        traffic_summary['with_traffic_data'] if traffic_summary['with_traffic_data'] > 0 else 0)
            st.markdown(get_stats_card(
                f"{avg_delay:.0f} min",
                "Avg Delay per Route"
            ), unsafe_allow_html=True)
    
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
    cols = st.columns(5)
    
    total_places = sum(len(day_plan) for day_plan in st.session_state.itinerary.values())
    total_meals = sum(1 for day_plan in st.session_state.itinerary.values() 
                      for activity in day_plan if activity["Category"] == "food")
    total_travel = sum(1 for day_plan in st.session_state.itinerary.values() 
                       for activity in day_plan if "travel" in activity["Category"])
    total_days = len(st.session_state.itinerary)
    
    # Count traffic-aware routes
    traffic_aware_routes = sum(1 for day_plan in st.session_state.itinerary.values() 
                               for activity in day_plan if "travel" in activity["Category"] 
                               and activity.get("Has_Traffic_Data", False))
    
    with cols[0]:
        st.markdown(get_stats_card(total_places, "Total Activities"), unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(get_stats_card(total_meals, "Meal Breaks"), unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown(get_stats_card(total_travel, "Travel Segments"), unsafe_allow_html=True)
    
    with cols[3]:
        st.markdown(get_stats_card(total_days, "Days"), unsafe_allow_html=True)
    
    with cols[4]:
        color = "green" if traffic_aware_routes > 0 else "orange"
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-value" style="color: {color};">{traffic_aware_routes}</div>
            <div class="stats-label">Live Traffic Routes</div>
        </div>
        """, unsafe_allow_html=True)

    # Traffic Legend
    st.markdown(get_section_header("🎨", "Traffic Legend"), unsafe_allow_html=True)
    
    legend_cols = st.columns(3)
    
    with legend_cols[0]:
        st.markdown("**Traffic Levels:**", unsafe_allow_html=True)
        st.markdown('<div style="display: flex; align-items: center; margin-bottom: 8px;">🟢 Light Traffic (0-5% delay)</div>', unsafe_allow_html=True)
        st.markdown('<div style="display: flex; align-items: center; margin-bottom: 8px;">🟡 Moderate Traffic (5-20% delay)</div>', unsafe_allow_html=True)
        st.markdown('<div style="display: flex; align-items: center; margin-bottom: 8px;">🟠 Heavy Traffic (20-50% delay)</div>', unsafe_allow_html=True)
        st.markdown('<div style="display: flex; align-items: center; margin-bottom: 8px;">🔴 Severe Traffic (>50% delay)</div>', unsafe_allow_html=True)
    
    with legend_cols[1]:
        st.markdown("**Travel Types:**", unsafe_allow_html=True)
        st.markdown('<div class="category-badge sightseeing-badge" style="margin-bottom: 8px;">📍 Sightseeing</div>', unsafe_allow_html=True)
        st.markdown('<div class="category-badge meal-badge" style="margin-bottom: 8px;">🍽️ Meal Break</div>', unsafe_allow_html=True)
        st.markdown('<div class="category-badge travel-badge" style="margin-bottom: 8px;">🚌 City Travel</div>', unsafe_allow_html=True)
        st.markdown('<div class="category-badge travel-badge" style="margin-bottom: 8px;">🚗 Local Travel</div>', unsafe_allow_html=True)
    
    with legend_cols[2]:
        st.markdown("**Map Markers:**", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size: 0.9rem; color: #666;">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <div style="width: 20px; height: 20px; background-color: #FFD700; border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; 
                            margin-right: 8px; color: #333; font-weight: bold; font-size: 10px;">1</div>
                <span>Activity order for each day</span>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <div style="width: 12px; height: 12px; background-color: #FFD700; border-radius: 50%; 
                            margin-right: 8px;"></div>
                <span>Circle color represents day</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Enhanced Itinerary Display with Traffic Information
    st.markdown(get_section_header("📅", "Detailed Itinerary with Live Traffic"), unsafe_allow_html=True)
    
    for i, (day, acts) in enumerate(st.session_state.itinerary.items()):
        day_color = DAY_COLORS[i % len(DAY_COLORS)]
        
        # Calculate day statistics
        day_travel_segments = sum(1 for a in acts if "travel" in a.get('Category', ''))
        day_traffic_routes = sum(1 for a in acts if "travel" in a.get('Category', '') and a.get('Has_Traffic_Data', False))
        
        # Day header with expander
        expander_text = f"**{day}** - {len(acts)} activities • {day_travel_segments} travel segments"
        if day_traffic_routes > 0:
            expander_text += f" • {day_traffic_routes} with live traffic"
        
        with st.expander(expander_text, expanded=True):
            
            for a in acts:
                emoji, badge_html, card_class = get_activity_styling(a)
                
                # Add traffic information for travel activities
                if "travel" in a.get('Category', ''):
                    traffic_emoji = a.get('Traffic_Emoji', '⚫')
                    traffic_level = a.get('Traffic_Level', 'No Traffic Data')
                    delay_percentage = a.get('Delay_Percentage', 0)
                    distance_km = a.get('Distance_km')
                    
                    # Build badge container HTML
                    badge_container_html = f'<div class="badge-container">{badge_html}'
                    
                    # Add traffic badge
                    traffic_badge = get_traffic_badge(traffic_level, traffic_emoji)
                    if traffic_badge:
                        badge_container_html += traffic_badge
                    
                    # Add delay badge if there's delay
                    delay_badge = get_delay_badge(delay_percentage)
                    if delay_badge:
                        badge_container_html += delay_badge
                    
                    # Add distance badge if available
                    distance_badge = get_distance_badge(distance_km)
                    if distance_badge:
                        badge_container_html += distance_badge
                    
                    badge_container_html += '</div>'
                else:
                    # For non-travel activities, just use the basic badge
                    badge_container_html = f'<div class="badge-container">{badge_html}</div>'
                
                st.markdown(get_activity_card(a['Place'], a['Time'], emoji, badge_container_html, card_class), unsafe_allow_html=True)
        
        st.markdown("")
