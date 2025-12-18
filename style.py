# ================= STYLES =================
CSS_STYLE = """
<style>
    /* Main theme colors */
    :root {
        --primary: #1E3A8A;
        --primary-light: #3B82F6;
        --secondary: #047857;
        --accent: #DC2626;
        --background: #F8FAFC;
        --surface: #FFFFFF;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
        --border: #E5E7EB;
        --sidebar-bg: #1F2937;
        --header-white: #FFFFFF;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        background-color: var(--background);
    }
    
    /* Header styling */
    .stTitle h1 {
        color: var(--primary);
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border);
        font-weight: 700;
        font-size: 2rem;
    }
    
    /* Subheader styling - WHITE TEXT for specific headers */
    h2, h3 {
        color: var(--header-white) !important;
        font-weight: 600 !important;
        background: linear-gradient(135deg, #1E3A8A, #3B82F6);
        padding: 12px 20px;
        border-radius: 8px;
        margin-top: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Specific header icons */
    h2::before, h3::before {
        margin-right: 10px;
        font-size: 1.2em;
    }
    
    /* Sidebar styling - DARK THEME */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
    }
    
    section[data-testid="stSidebar"] .stSelectbox,
    section[data-testid="stSidebar"] .stSlider,
    section[data-testid="stSidebar"] .stTimeInput,
    section[data-testid="stSidebar"] .stButton button {
        color: #F9FAFB !important;
    }
    
    section[data-testid="stSidebar"] label {
        color: #D1D5DB !important;
        font-weight: 500 !important;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #F9FAFB !important;
        background: none !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    
    /* Sidebar button styling */
    section[data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, var(--primary-light), var(--primary));
        color: white !important;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border-radius: 8px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Activity cards styling */
    .activity-card {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.75rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-left: 4px solid;
        background-color: var(--surface);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .activity-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Meal activities */
    .meal-card {
        background-color: #F0F9FF;
        border-left-color: #0EA5E9;
    }
    
    /* Sightseeing activities */
    .sightseeing-card {
        background-color: #F0FDF4;
        border-left-color: #10B981;
    }
    
    /* City-to-city travel */
    .city-travel-card {
        background-color: #FFFBEB;
        border-left-color: #F59E0B;
    }
    
    /* Place-to-place travel */
    .place-travel-card {
        background-color: #FEF3C7;
        border-left-color: #F59E0B;
    }
    
    /* Category badges */
    .category-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .meal-badge {
        background-color: #E0F2FE;
        color: #0369A1;
    }
    
    .travel-badge {
        background-color: #FEF3C7;
        color: #92400E;
    }
    
    .sightseeing-badge {
        background-color: #DCFCE7;
        color: #166534;
    }
    
    /* Traffic badges */
    .traffic-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .light-traffic {
        background-color: #10B981;
        color: white;
    }
    
    .moderate-traffic {
        background-color: #F59E0B;
        color: white;
    }
    
    .heavy-traffic {
        background-color: #F97316;
        color: white;
    }
    
    .severe-traffic {
        background-color: #DC2626;
        color: white;
    }
    
    .no-traffic-data {
        background-color: #6B7280;
        color: white;
    }
    
    /* Day color badges */
    .day-color-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 8px;
        color: white;
        text-shadow: 0 1px 1px rgba(0,0,0,0.2);
    }
    
    /* Legend styling */
    .legend-container {
        background-color: var(--surface);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid var(--border);
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Statistics cards */
    .stats-card {
        background-color: var(--surface);
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid var(--border);
        transition: transform 0.2s ease;
    }
    
    .stats-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stats-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary);
    }
    
    .stats-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-top: 0.25rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        margin-bottom: 0.5rem !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #F3F4F6 !important;
    }
    
    /* Divider styling */
    hr {
        margin: 1.5rem 0 !important;
        border: none !important;
        border-top: 1px solid var(--border) !important;
    }
    
    /* Map container */
    .folium-map {
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        border: 1px solid var(--border) !important;
    }
    
    /* Time display in activities */
    .time-display {
        background-color: #F9FAFB;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        color: var(--text-primary);
        border: 1px solid var(--border);
    }
    
    /* Custom header styling */
    .custom-header {
        background: linear-gradient(135deg, #1E3A8A, #3B82F6);
        color: white !important;
        padding: 12px 20px;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Section containers */
    .section-container {
        margin: 2rem 0;
    }
    
    /* Day indicator styling */
    .day-indicator {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.25rem;
        color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Map legend styling */
    .map-legend {
        background-color: white;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        font-size: 0.8rem;
        line-height: 1.5;
    }
    
    /* Badge container for multiple badges */
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
    }
    
    /* Delay badge */
    .delay-badge {
        background-color: #EF4444;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.7rem;
        display: inline-flex;
        align-items: center;
    }
    
    /* Distance badge */
    .distance-badge {
        background-color: #3B82F6;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.7rem;
        display: inline-flex;
        align-items: center;
    }
</style>
"""

# HTML for main title with gradient effect
MAIN_TITLE_HTML = """
<div style="background: linear-gradient(135deg, #1E3A8A, #3B82F6); padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem;">
    <h1 style="color: white; margin: 0; font-size: 2.5rem;">🧳 Smart Travel Itinerary Generator</h1>
    <p style="color: #E0F2FE; margin: 0.5rem 0 0 0; font-size: 1rem;">Plan your perfect trip with AI-powered itinerary suggestions</p>
</div>
"""

# HTML for sidebar header
SIDEBAR_HEADER_HTML = """
<div style="padding: 0.5rem 0 1.5rem 0;">
    <h3 style="color: #F9FAFB; margin: 0;">✈️ Trip Configuration</h3>
    <p style="color: #9CA3AF; margin: 0.25rem 0 1rem 0; font-size: 0.9rem;">Customize your travel experience</p>
</div>
"""

# Day colors - changed Day 1 to bright yellow for better visibility
DAY_COLORS = ["#FFD700", "#2563EB", "#059669", "#7C3AED", "#DC2626", "#EA580C", "#1E40AF", "#7C2D12", "#3730A3", "#86198F"]

# HTML for white gradient headers
def get_section_header(icon, text):
    return f"""
    <div class="custom-header">
        <h3 style="color: white; margin: 0; display: flex; align-items: center;">
            <span style="margin-right: 10px; font-size: 1.2em;">{icon}</span>
            {text}
        </h3>
    </div>
    """

# HTML for statistics cards
def get_stats_card(value, label):
    return f"""
    <div class="stats-card">
        <div class="stats-value">{value}</div>
        <div class="stats-label">{label}</div>
    </div>
    """

# HTML for activity cards - UPDATED to handle badge containers properly
def get_activity_card(place, time, emoji, badge_container_html, card_class):
    return f"""
    <div class="activity-card {card_class}">
        {badge_container_html}
        <div style="display: flex; align-items: flex-start; margin-bottom: 8px;">
            <span style="font-size: 1.5rem; margin-right: 12px; margin-top: 2px;">{emoji}</span>
            <div style="flex: 1;">
                <h4 style="margin: 0 0 8px 0; color: #1F2937; font-size: 1.05rem; font-weight: 600;">{place}</h4>
                <div style="display: flex; align-items: center; margin-top: 4px;">
                    <span class="time-display">{time}</span>
                </div>
            </div>
        </div>
    </div>
    """

# HTML for category badges
def get_category_badge(category_type, text):
    if category_type == "meal":
        return f'<span class="category-badge meal-badge">{text}</span>'
    elif category_type == "travel":
        return f'<span class="category-badge travel-badge">{text}</span>'
    elif category_type == "sightseeing":
        return f'<span class="category-badge sightseeing-badge">{text}</span>'
    return f'<span class="category-badge">{text}</span>'

# HTML for day color indicator
def get_day_color_indicator(day_name, color):
    return f"""
    <div class="day-indicator" style="background-color: {color};">
        <div style="width: 10px; height: 10px; background-color: white; border-radius: 50%; margin-right: 6px;"></div>
        {day_name}
    </div>
    """

# Get traffic badge HTML
def get_traffic_badge(traffic_level, traffic_emoji):
    traffic_class = ""
    if traffic_level == "Light Traffic":
        traffic_class = "light-traffic"
    elif traffic_level == "Moderate Traffic":
        traffic_class = "moderate-traffic"
    elif traffic_level == "Heavy Traffic":
        traffic_class = "heavy-traffic"
    elif traffic_level == "Severe Traffic":
        traffic_class = "severe-traffic"
    else:
        traffic_class = "no-traffic-data"
    
    return f'<span class="traffic-badge {traffic_class}">{traffic_emoji} {traffic_level}</span>'

# Get delay badge HTML
def get_delay_badge(delay_percentage):
    if delay_percentage > 0:
        return f'<span class="delay-badge">⚠️ +{delay_percentage:.0f}% delay</span>'
    return ""

# Get distance badge HTML
def get_distance_badge(distance_km):
    if distance_km:
        return f'<span class="distance-badge">📏 {distance_km:.1f} km</span>'
    return ""

# Helper to get appropriate badge and styling for activity
def get_activity_styling(activity):
    category = activity.get('Category', '')
    place = activity['Place']
    
    if category == 'food':
        if 'Breakfast' in place:
            return "🍳", get_category_badge("meal", "Breakfast"), "meal-card"
        elif 'Lunch' in place:
            return "🍽️", get_category_badge("meal", "Lunch"), "meal-card"
        elif 'Dinner' in place:
            return "🍛", get_category_badge("meal", "Dinner"), "meal-card"
        else:
            return "🍽️", get_category_badge("meal", "Meal"), "meal-card"
    
    elif category == 'travel_city':
        return "🚌", get_category_badge("travel", "City Travel"), "city-travel-card"
    
    elif category == 'travel_place':
        return "🚗", get_category_badge("travel", "Local Travel"), "place-travel-card"
    
    else:
        return "📍", get_category_badge("sightseeing", "Sightseeing"), "sightseeing-card"
