import folium
import os, sys, json
from folium.plugins import MarkerCluster


def nahraj_geojson(jmeno_souboru):
    """ Načte soubor typu geojson a ošetří nekorektní vstupy. """
    try:
        with open(os.path.join(sys.path[0], jmeno_souboru+".geojson"), "r", encoding="UTF-8") as file:
            data = json.load(file)

    except PermissionError:
        print(f"K souboru {jmeno_souboru} nemá program přístup.")
        exit()
    except FileNotFoundError:
        print(f"Soubor {jmeno_souboru} nebyl nenalezen.")
        exit()
    except ValueError:
        print(f"Soubor {jmeno_souboru} je chybný.")
        exit()

    return data


# ! Hlavní část programu
data = nahraj_geojson("kontejnery")

# ? mapa
prg_map = folium.Map(location=[50.0506483, 14.4608981], zoom_start=11)
marker_cluster = MarkerCluster().add_to(prg_map)

# geojson parcelování
for feature in data['features']:
    
    geo = feature['geometry']["coordinates"][1],feature['geometry']["coordinates"][0]
    x_geo = geo[0]
    y_geo = geo[1]
    adresa = feature['properties']['STATIONNAME']
    m_cast = feature['properties']['CITYDISTRICT']
    pristup = feature['properties']['PRISTUP']
    id_code = feature['properties']['STATIONNUMBER']

    html = """<p>Adresa: {adresa}<br>
                    Městská část: {m_cast}<br>
                    Přístup: {pristup}<br>
                    ID: {id}"""

    html_complete = html.format(adresa=adresa, m_cast=m_cast, pristup=pristup, id=id_code)
    info = folium.Html(html_complete, script=True)
    popup = folium.Popup(info, max_width=2650)

    if pristup == "volně":
        color = "green"
        icon = "glyphicon glyphicon-eye-open"
    elif pristup == "obyvatelům domu":
        color = "red"
        icon = "glyphicon glyphicon-eye-close"

    # ? Vytváření bodů
    folium.Marker(location=[x_geo, y_geo], tooltip=adresa, popup=popup, 
                icon=folium.Icon(color=color, icon_color="white", icon=icon)).add_to(marker_cluster)


prg_map.save("map.html")
