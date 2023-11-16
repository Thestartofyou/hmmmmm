import geopandas as gpd
from shapely.geometry import Point, Polygon

def simplify_geometry(geometry, tolerance=0.001):
    # Simplify the geometry to reduce the number of vertices
    return geometry.simplify(tolerance)

def process_tax_map(input_shapefile, output_folder, attribute_column):
    # Read the shapefile into a GeoDataFrame
    gdf = gpd.read_file(input_shapefile)

    # Simplify the geometry to reduce the size
    gdf['geometry'] = gdf['geometry'].apply(simplify_geometry)

    # Create output folder if it doesn't exist
    import os
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over unique values in the specified attribute column
    for value in gdf[attribute_column].unique():
        # Create a GeoDataFrame for each unique value
        subset_gdf = gdf[gdf[attribute_column] == value]

        # Save the GeoDataFrame to a GeoJSON file
        output_file = os.path.join(output_folder, f'{value}.geojson')
        subset_gdf.to_file(output_file, driver='GeoJSON')

if __name__ == "__main__":
    # Example usage
    input_shapefile = 'path/to/tax_assessor_map.shp'
    output_folder = 'path/to/output_folder'
    attribute_column = 'property_id'

    process_tax_map(input_shapefile, output_folder, attribute_column)
