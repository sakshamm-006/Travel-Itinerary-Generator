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
# ================= PREMIUM STYLES - REDESIGNED FOR RECRUITER IMPACT =================
CSS_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Root Design Tokens ── */
    :root {
        --ink:        #0D0F14;
        --ink-soft:   #3D4354;
        --ink-muted:  #8890A4;
        --canvas:     #F5F6FA;
        --surface:    #FFFFFF;
        --surface-2:  #F0F2F8;
        --border:     #E2E5EF;
        --border-s:   #C8CCE0;

        --brand:      #2563EB;
        --brand-dark: #1845C0;
        --brand-glow: rgba(37, 99, 235, 0.18);
        --brand-pale: #EEF3FD;

        --emerald:    #059669;
        --emerald-pale: #ECFDF5;
        --amber:      #D97706;
        --amber-pale: #FFFBEB;
        --rose:       #E11D48;
        --rose-pale:  #FFF1F4;
        --violet:     #7C3AED;
        --violet-pale:#F5F3FF;
        --sky:        #0284C7;
        --sky-pale:   #F0F9FF;

        --sidebar-bg: #0D0F14;
        --sidebar-surface: #181B24;
        --sidebar-border: #262B38;
        --sidebar-text: #CDD2E0;
        --sidebar-muted: #636A80;

        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 24px;

        --shadow-xs: 0 1px 3px rgba(13,15,20,0.06), 0 1px 2px rgba(13,15,20,0.04);
        --shadow-sm: 0 2px 8px rgba(13,15,20,0.08), 0 1px 3px rgba(13,15,20,0.05);
        --shadow-md: 0 4px 16px rgba(13,15,20,0.10), 0 2px 6px rgba(13,15,20,0.06);
        --shadow-lg: 0 8px 32px rgba(13,15,20,0.12), 0 4px 12px rgba(13,15,20,0.07);
        --shadow-brand: 0 4px 20px rgba(37,99,235,0.22);
    }

    /* ── Global Reset ── */
    *, *::before, *::after { box-sizing: border-box; }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'DM Sans', sans-serif;
        background-color: var(--canvas) !important;
        color: var(--ink);
    }

    .main .block-container {
        padding: 2rem 2.5rem 3rem 2.5rem;
        max-width: 1280px;
    }

    /* ── Typography overrides ── */
    h1, h2, h3, h4 {
        font-family: 'Sora', sans-serif;
        letter-spacing: -0.02em;
    }

    /* Remove Streamlit default heading styles so our custom HTML takes over */
    h2, h3 {
        background: none !important;
        box-shadow: none !important;
        color: var(--ink) !important;
        padding: 0 !important;
        margin: 0 !important;
        border-radius: 0 !important;
        font-size: inherit !important;
        font-weight: inherit !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--sidebar-border);
    }

    section[data-testid="stSidebar"] > div { padding: 1.5rem 1.25rem; }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: var(--sidebar-text) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.85rem !important;
    }

    section[data-testid="stSidebar"] .stSelectbox > div > div,
    section[data-testid="stSidebar"] .stTimeInput > div > div {
        background: var(--sidebar-surface) !important;
        border: 1px solid var(--sidebar-border) !important;
        border-radius: var(--radius-sm) !important;
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"] { display: none; }
    section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div:first-child {
        background: var(--sidebar-border) !important;
    }
    section[data-testid="stSidebar"] .stSlider [data-baseweb="thumb"] {
        background: var(--brand) !important;
        border: 2px solid white !important;
        box-shadow: var(--shadow-brand) !important;
    }

    /* Sidebar generate button */
    section[data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, var(--brand), var(--brand-dark)) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem 1.5rem !important;
        font-family: 'Sora', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.01em !important;
        width: 100% !important;
        cursor: pointer !important;
        box-shadow: var(--shadow-brand) !important;
        transition: all 0.2s ease !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(37,99,235,0.35) !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: var(--sidebar-border) !important;
        margin: 1.25rem 0 !important;
    }

    /* ── Main area buttons ── */
    .stButton button {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        border-radius: var(--radius-sm) !important;
        transition: all 0.2s ease !important;
    }

    /* ── Metrics ── */
    [data-testid="metric-container"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        padding: 1rem 1.25rem !important;
        box-shadow: var(--shadow-xs) !important;
    }
    [data-testid="metric-container"] label {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        color: var(--ink-muted) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-family: 'Sora', sans-serif !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: var(--ink) !important;
    }

    /* ── Expanders ── */
    .streamlit-expanderHeader {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        font-family: 'Sora', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        color: var(--ink) !important;
        padding: 0.75rem 1rem !important;
        transition: background 0.15s !important;
    }
    .streamlit-expanderHeader:hover { background: var(--surface-2) !important; }

    /* ── Divider ── */
    hr {
        border: none !important;
        border-top: 1px solid var(--border) !important;
        margin: 2rem 0 !important;
    }

    /* ── Activity Cards ── */
    .activity-card {
        background: var(--surface);
        border-radius: var(--radius-md);
        padding: 1rem 1.125rem;
        margin-bottom: 0.625rem;
        border: 1px solid var(--border);
        border-left: 4px solid var(--brand);
        box-shadow: var(--shadow-xs);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .activity-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }

    .meal-card        { border-left-color: var(--sky);     background: var(--sky-pale); }
    .sightseeing-card { border-left-color: var(--emerald); background: var(--emerald-pale); }
    .city-travel-card { border-left-color: var(--amber);   background: var(--amber-pale); }
    .place-travel-card{ border-left-color: var(--amber);   background: var(--amber-pale); }

    /* ── Badges ── */
    .category-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 10px;
        border-radius: 100px;
        font-family: 'Sora', sans-serif;
        font-size: 0.68rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 6px;
    }
    .meal-badge        { background: #DBEAFE; color: #1D4ED8; }
    .travel-badge      { background: #FDE68A; color: #92400E; }
    .sightseeing-badge { background: #BBF7D0; color: #065F46; }

    /* Traffic badges */
    .traffic-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 9px;
        border-radius: 100px;
        font-size: 0.68rem;
        font-weight: 600;
        margin-left: 6px;
    }
    .light-traffic    { background: #D1FAE5; color: #065F46; }
    .moderate-traffic { background: #FEF3C7; color: #92400E; }
    .heavy-traffic    { background: #FFEDD5; color: #9A3412; }
    .severe-traffic   { background: #FFE4E6; color: #9F1239; }
    .no-traffic-data  { background: #F3F4F6; color: #6B7280; }

    /* Distance / Delay badges */
    .delay-badge    { background: #FEE2E2; color: #991B1B; padding: 3px 9px; border-radius: 100px; font-size: 0.68rem; font-weight: 600; display: inline-flex; align-items: center; gap: 3px; }
    .distance-badge { background: #DBEAFE; color: #1E40AF; padding: 3px 9px; border-radius: 100px; font-size: 0.68rem; font-weight: 600; display: inline-flex; align-items: center; gap: 3px; }

    /* Day indicator pills */
    .day-indicator {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 100px;
        font-family: 'Sora', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        color: white;
        box-shadow: var(--shadow-xs);
        margin: 3px;
    }

    /* ── Stats cards ── */
    .stats-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1.125rem 1rem;
        text-align: center;
        box-shadow: var(--shadow-xs);
        transition: transform 0.18s, box-shadow 0.18s;
    }
    .stats-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
    .stats-value {
        font-family: 'Sora', sans-serif;
        font-size: 1.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--brand), var(--violet));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
    }
    .stats-label {
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--ink-muted);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 4px;
    }

    /* ── Legend container ── */
    .legend-container {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-xs);
    }

    /* ── Time display ── */
    .time-display {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 500;
        color: var(--ink-soft);
        background: var(--surface-2);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 3px 8px;
    }

    /* ── Map container ── */
    .folium-map, iframe {
        border-radius: var(--radius-lg) !important;
        box-shadow: var(--shadow-md) !important;
        border: 1px solid var(--border) !important;
    }

    /* ── Chat input ── */
    [data-testid="stChatInput"] textarea {
        font-family: 'DM Sans', sans-serif !important;
        border-radius: var(--radius-md) !important;
        border-color: var(--border-s) !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: var(--brand) !important;
        box-shadow: 0 0 0 3px var(--brand-glow) !important;
    }

    /* ── Text input ── */
    .stTextInput input {
        font-family: 'DM Sans', sans-serif !important;
        border-radius: var(--radius-sm) !important;
        border-color: var(--border-s) !important;
        transition: border-color 0.15s, box-shadow 0.15s !important;
    }
    .stTextInput input:focus {
        border-color: var(--brand) !important;
        box-shadow: 0 0 0 3px var(--brand-glow) !important;
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        border-radius: var(--radius-sm) !important;
        border-color: var(--border-s) !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── Alert / info box ── */
    .stAlert {
        border-radius: var(--radius-md) !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── Download button ── */
    .stDownloadButton button {
        border-radius: var(--radius-sm) !important;
        font-family: 'Sora', sans-serif !important;
        font-weight: 600 !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border-s); border-radius: 6px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--ink-muted); }
</style>
"""

# ── Main Hero Banner ──────────────────────────────────────────────────────────
MAIN_TITLE_HTML = """
<div style="
    position: relative;
    background: linear-gradient(135deg, #0D1B4B 0%, #1845C0 55%, #2563EB 100%);
    border-radius: 20px;
    padding: 2.5rem 2.75rem;
    margin-bottom: 2rem;
    overflow: hidden;
    box-shadow: 0 8px 40px rgba(37,99,235,0.30);
">
    <!-- decorative circles -->
    <div style="position:absolute;top:-60px;right:-60px;width:280px;height:280px;border-radius:50%;background:rgba(255,255,255,0.05);"></div>
    <div style="position:absolute;bottom:-80px;right:120px;width:200px;height:200px;border-radius:50%;background:rgba(255,255,255,0.04);"></div>
    <div style="position:absolute;top:50%;left:65%;width:120px;height:120px;border-radius:50%;background:rgba(255,255,255,0.035);transform:translateY(-50%);"></div>

    <!-- pill tag -->
    <div style="
        display:inline-flex; align-items:center; gap:6px;
        background:rgba(255,255,255,0.12);
        border:1px solid rgba(255,255,255,0.18);
        border-radius:100px; padding:5px 14px;
        font-family:'Sora',sans-serif; font-size:0.72rem; font-weight:600;
        color:rgba(255,255,255,0.90); letter-spacing:0.08em; text-transform:uppercase;
        margin-bottom:1rem;
    ">
        ✦ &nbsp; AI-Powered Itinerary
    </div>

    <h1 style="
        font-family:'Sora',sans-serif;
        font-size:2.4rem; font-weight:800;
        color:#FFFFFF; margin:0 0 0.5rem 0;
        letter-spacing:-0.03em; line-height:1.1;
    ">🧳 Smart Travel Itinerary</h1>

    <p style="
        font-family:'DM Sans',sans-serif;
        color:rgba(255,255,255,0.70); margin:0;
        font-size:1.0rem; font-weight:400; max-width:480px;
    ">Personalized multi-day plans with live traffic, weather &amp; AI recommendations — built for Rajasthan &amp; beyond.</p>
</div>
"""

# ── Sidebar Header ────────────────────────────────────────────────────────────
SIDEBAR_HEADER_HTML = """
<div style="padding:0.25rem 0 1.75rem 0; border-bottom:1px solid #262B38; margin-bottom:1.5rem;">
    <div style="
        display:inline-flex; align-items:center; gap:6px;
        background:rgba(37,99,235,0.20); border:1px solid rgba(37,99,235,0.35);
        border-radius:100px; padding:4px 12px; margin-bottom:0.875rem;
        font-family:'Sora',sans-serif; font-size:0.68rem; font-weight:600;
        color:#93C5FD; letter-spacing:0.08em; text-transform:uppercase;
    ">✈ Trip Configuration</div>
    <h3 style="
        font-family:'Sora',sans-serif; font-size:1.15rem; font-weight:700;
        color:#FFFFFF; margin:0 0 0.25rem 0; letter-spacing:-0.02em;
    ">Plan Your Journey</h3>
    <p style="font-family:'DM Sans',sans-serif; color:#636A80; font-size:0.8rem; margin:0;">
        Adjust preferences to generate your ideal itinerary.
    </p>
</div>
"""

# ── Day colour palette (vivid, distinct) ─────────────────────────────────────
DAY_COLORS = [
    "#2563EB",  # blue
    "#059669",  # emerald
    "#D97706",  # amber
    "#7C3AED",  # violet
    "#E11D48",  # rose
    "#0284C7",  # sky
    "#D946EF",  # fuchsia
    "#EA580C",  # orange
    "#0891B2",  # cyan
    "#65A30D",  # lime
]

# ── Section header component ──────────────────────────────────────────────────
def get_section_header(icon, text):
    return f"""
    <div style="
        display:flex; align-items:center; gap:12px;
        margin:2rem 0 1.25rem 0;
        padding-bottom:0.75rem;
        border-bottom:2px solid #E2E5EF;
    ">
        <div style="
            width:40px; height:40px; border-radius:10px;
            background:linear-gradient(135deg,#2563EB,#7C3AED);
            display:flex; align-items:center; justify-content:center;
            font-size:1.1rem; flex-shrink:0;
            box-shadow:0 4px 12px rgba(37,99,235,0.25);
        ">{icon}</div>
        <h3 style="
            font-family:'Sora',sans-serif; font-size:1.15rem; font-weight:700;
            color:#0D0F14; margin:0; letter-spacing:-0.02em;
        ">{text}</h3>
    </div>
    """

# ── Stats card ────────────────────────────────────────────────────────────────
def get_stats_card(value, label):
    return f"""
    <div class="stats-card">
        <div class="stats-value">{value}</div>
        <div class="stats-label">{label}</div>
    </div>
    """

# ── Activity card ─────────────────────────────────────────────────────────────
def get_activity_card(place, time, emoji, badge_container_html, card_class):
    return f"""
    <div class="activity-card {card_class}">
        {badge_container_html}
        <div style="display:flex; align-items:flex-start; gap:12px;">
            <div style="
                width:38px; height:38px; border-radius:10px;
                background:rgba(255,255,255,0.80);
                display:flex; align-items:center; justify-content:center;
                font-size:1.25rem; flex-shrink:0;
                box-shadow:0 2px 6px rgba(0,0,0,0.06);
            ">{emoji}</div>
            <div style="flex:1; min-width:0;">
                <p style="
                    font-family:'Sora',sans-serif; font-size:0.92rem;
                    font-weight:600; color:#0D0F14; margin:0 0 6px 0;
                    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
                ">{place}</p>
                <span class="time-display">{time}</span>
            </div>
        </div>
    </div>
    """

# ── Category badge helpers ────────────────────────────────────────────────────
def get_category_badge(category_type, text):
    cls = {"meal": "meal-badge", "travel": "travel-badge", "sightseeing": "sightseeing-badge"}.get(category_type, "")
    return f'<span class="category-badge {cls}">{text}</span>'

# ── Day colour indicator ──────────────────────────────────────────────────────
def get_day_color_indicator(day_name, color):
    return f"""
    <div class="day-indicator" style="background-color:{color};">
        <div style="width:8px;height:8px;background:#FFFFFF;border-radius:50%;opacity:0.85;"></div>
        {day_name}
    </div>
    """

# ── Traffic badge ─────────────────────────────────────────────────────────────
def get_traffic_badge(traffic_level, traffic_emoji):
    cls_map = {
        "Light Traffic":    "light-traffic",
        "Moderate Traffic": "moderate-traffic",
        "Heavy Traffic":    "heavy-traffic",
        "Severe Traffic":   "severe-traffic",
    }
    cls = cls_map.get(traffic_level, "no-traffic-data")
    return f'<span class="traffic-badge {cls}">{traffic_emoji} {traffic_level}</span>'

# ── Delay badge ───────────────────────────────────────────────────────────────
def get_delay_badge(delay_percentage):
    if delay_percentage > 0:
        return f'<span class="delay-badge">⚠ +{delay_percentage:.0f}% delay</span>'
    return ""

# ── Distance badge ────────────────────────────────────────────────────────────
def get_distance_badge(distance_km):
    if distance_km:
        return f'<span class="distance-badge">📏 {distance_km:.1f} km</span>'
    return ""

# ── Activity styling resolver ─────────────────────────────────────────────────
def get_activity_styling(activity):
    category = activity.get('Category', '')
    place    = activity['Place']

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
        return "🚌", get_category_badge("travel", "City Travel"),  "city-travel-card"
    elif category == 'travel_place':
        return "🚗", get_category_badge("travel", "Local Travel"), "place-travel-card"
    else:
        return "📍", get_category_badge("sightseeing", "Sightseeing"), "sightseeing-card"
