import json
import pandas as pd

# Carregar o arquivo JSON
with open("gis_osm_roads_free_auto_estradas.json", "r") as f:
    data = json.load(f)

# Criar uma lista de dados com osm_id e outros atributos
dados = []
for feature in data:
    osm_id = feature.get('osm_id')  # Pega o osm_id
    fclass = feature.get('fclass')  # Classe da estrada
    name = feature.get('name')  # Nome da estrada
    ref = feature.get('ref')  # Refer�ncia
    maxspeed = feature.get('maxspeed')  # Velocidade m�xima
    bridge = feature.get('bridge')  # Se � ponte
    tunnel = feature.get('tunnel')  # Se � t�nel

    dados.append({
        "osm_id": osm_id,
        "fclass": fclass,
        "name": name,
        "ref": ref,
        "maxspeed": maxspeed,
        "bridge": bridge,
        "tunnel": tunnel
    })

# Criar um DataFrame com os dados
df = pd.DataFrame(dados)

# Salvar o DataFrame em um arquivo Excel
df.to_excel("Autoestrada.xlsx", index=False)
