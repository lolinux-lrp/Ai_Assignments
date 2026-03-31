import os
import urllib.request
from typing import Dict, List
import warnings

# Suppress Shapely deprecation warnings that might occur with some Geopandas versions
warnings.filterwarnings("ignore")

try:
    import geopandas as gpd
    import matplotlib.pyplot as plt
except ImportError:
    print("Please install required libraries by running:")
    print("pip install geopandas matplotlib")
    exit(1)

from csp import CSP, Constraint

class MapColoringConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1: str = place1
        self.place2: str = place2

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        return assignment[self.place1] != assignment[self.place2]

def download_geojson(filepath: str):
    url = "https://raw.githubusercontent.com/gggodhwani/telangana_boundaries/master/districts.json"
    if not os.path.exists(filepath):
        print("Downloading Telangana districts GeoJSON...")
        urllib.request.urlretrieve(url, filepath)
        print("Download complete.")

def main():
    geojson_path = "telangana_districts.geojson"
    download_geojson(geojson_path)
    
    print("Loading geographic data...")
    gdf = gpd.read_file(geojson_path)
    
    # Identify the column containing district names
    name_col = None
    for col in gdf.columns:
        if col.lower() in ["district", "dist_name", "shape_name", "dtname", "name", "d_n"]:
            name_col = col
            break
            
    if not name_col:
        name_col = [c for c in gdf.columns if c != 'geometry'][0]

    districts = gdf[name_col].tolist()
    
    # Red, Green, Blue, Yellow in nice pastel hex codes
    colors = ["#FF9999", "#99FF99", "#9999FF", "#FFFF99"] 
    
    domains: Dict[str, List[str]] = {}
    for district in districts:
        domains[district] = colors

    csp: CSP[str, str] = CSP(districts, domains)
    
    print("Extracting geographical adjacencies (this may take a few seconds)...")
    added = set()
    for i, row1 in gdf.iterrows():
        d1 = row1[name_col]
        geom1 = row1['geometry']
        for j, row2 in gdf.iterrows():
            if j <= i: continue
            d2 = row2[name_col]
            geom2 = row2['geometry']
            
            # If the polygons touch or intersect, add a constraint
            if geom1.touches(geom2) or geom1.intersects(geom2):
                pair = tuple(sorted([d1, d2]))
                if pair not in added:
                    csp.add_constraint(MapColoringConstraint(d1, d2))
                    added.add(pair)
                    
    print("Solving CSP...")
    solution: Dict[str, str] = csp.backtracking_search()
    
    if solution is None:
        print("No solution found.")
    else:
        print("Solution found!")
        
        gdf['Color'] = gdf[name_col].map(solution)
        
        print("Generating and saving the image...")
        fig, ax = plt.subplots(1, 1, figsize=(12, 12))
        gdf.plot(color=gdf['Color'], edgecolor='black', linewidth=0.5, ax=ax)
        
        # Add labels at the centroid of each district
        for x, y, label in zip(gdf.geometry.centroid.x, gdf.geometry.centroid.y, gdf[name_col]):
            ax.text(x, y, label, fontsize=7, ha='center', va='center', 
                    bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=1))
            
        plt.title("Telangana Map Coloring (CSP)", fontsize=16)
        plt.axis('off')
        
        output_image = "telangana_colored_map.png"
        plt.savefig(output_image, dpi=300, bbox_inches='tight')
        print(f"Image successfully saved to {output_image}")
        
        # Remove blocking plt.show()
        # plt.show()

if __name__ == "__main__":
    main()
