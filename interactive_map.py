"""
interactive_map.py
------------------
Run this script to generate an interactive HTML map file.

Requirements:
    pip install folium

Usage:
    python interactive_map.py

Output:
    interactive_map.html  — open in any browser or host on GitHub Pages
"""

import folium
from folium.plugins import MarkerCluster, Fullscreen, MiniMap

# ── 1. Base map ────────────────────────────────────────────────────────────────
# Starting location: Kumasi, Ghana
start_coords = [6.6885, -1.6244]

m = folium.Map(
    location=start_coords,
    zoom_start=13,
    tiles="CartoDB positron",          # clean, light basemap
    control_scale=True,                # shows a scale bar
)

# ── 2. Extra tile layers (user can toggle them) ────────────────────────────────
folium.TileLayer("OpenStreetMap", name="OpenStreetMap").add_to(m)
folium.TileLayer("CartoDB dark_matter", name="Dark Mode").add_to(m)
folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    name="Satellite",
).add_to(m)

# ── 3. Sample locations ────────────────────────────────────────────────────────
places = [
    {
        "name": "Kumasi Central Market",
        "coords": [6.6932, -1.6241],
        "category": "Market",
        "description": "One of the largest open-air markets in West Africa.",
        "icon": "shopping-cart",
        "color": "orange",
    },
    {
        "name": "Manhyia Palace Museum",
        "coords": [6.7023, -1.6162],
        "category": "Heritage",
        "description": "Royal palace of the Ashanti King (Asantehene).",
        "icon": "institution",
        "color": "red",
    },
    {
        "name": "Kejetia Bus Terminal",
        "coords": [6.6955, -1.6257],
        "category": "Transport",
        "description": "Major intercity transport hub in Kumasi.",
        "icon": "bus",
        "color": "blue",
    },
    {
        "name": "Kumasi Cultural Centre",
        "coords": [6.6870, -1.6180],
        "category": "Culture",
        "description": "Hosts craft markets, museums, and cultural events.",
        "icon": "star",
        "color": "purple",
    },
    {
        "name": "KNUST Botanical Garden",
        "coords": [6.6745, -1.5716],
        "category": "Nature",
        "description": "Beautiful garden on the KNUST campus.",
        "icon": "leaf",
        "color": "green",
    },
]

# ── 4. Add markers with popups & tooltips ─────────────────────────────────────
marker_cluster = MarkerCluster(name="Clustered Markers").add_to(m)

for place in places:
    popup_html = f"""
    <div style="font-family: Arial, sans-serif; min-width: 180px;">
        <h4 style="margin:0 0 6px; color:#333;">{place['name']}</h4>
        <span style="background:#eee; padding:2px 6px; border-radius:4px;
                     font-size:11px; color:#666;">{place['category']}</span>
        <p style="margin:8px 0 0; font-size:13px; color:#555;">
            {place['description']}
        </p>
    </div>
    """
    folium.Marker(
        location=place["coords"],
        tooltip=place["name"],               # shown on hover
        popup=folium.Popup(popup_html, max_width=260),
        icon=folium.Icon(
            color=place["color"],
            icon=place["icon"],
            prefix="fa",                     # FontAwesome icons
        ),
    ).add_to(marker_cluster)

# ── 5. Draw a simple route connecting the places ───────────────────────────────
route_coords = [p["coords"] for p in places]
folium.PolyLine(
    locations=route_coords,
    color="#E63946",
    weight=2.5,
    opacity=0.7,
    tooltip="Sample route",
    dash_array="8 4",
).add_to(m)

# ── 6. Plugins ─────────────────────────────────────────────────────────────────
Fullscreen(position="topright").add_to(m)         # fullscreen button
MiniMap(toggle_display=True).add_to(m)            # small overview map

# Layer control must be added LAST so it sees all layers
folium.LayerControl(collapsed=False).add_to(m)

# ── 7. Save ────────────────────────────────────────────────────────────────────
output_file = "interactive_map.html"
m.save(output_file)
print(f"✅  Map saved to '{output_file}'")
print("   Open it in your browser, or push it to GitHub Pages!")
