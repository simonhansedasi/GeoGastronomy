from pathlib import Path

import geopandas as gpd
from lxml import etree
from shapely.geometry import Polygon, MultiPolygon

import numpy as np





def kml_to_gdf(kml_path):
    '''
    Parse a KML file containing polygons into a GeoDataFrame.

    Parameters
    ----------
    kml_path : str or Path
        Path to KML file

    Returns
    -------
    geopandas.GeoDataFrame
    '''
    kml_path = Path(kml_path)

    tree = etree.parse(str(kml_path))
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    polygons = tree.xpath('//kml:Polygon', namespaces=ns)

    geoms = []
    for poly in polygons:
        coords_text = poly.xpath(
            './/kml:coordinates',
            namespaces=ns
        )[0].text

        coords = [
            (float(x), float(y))
            for x, y, *_ in (
                c.split(',') for c in coords_text.strip().split()
            )
        ]

        geoms.append(Polygon(coords))

    return gpd.GeoDataFrame(geometry=geoms, crs='EPSG:4326')


def write_geojson(gdf, output_path):
    '''
    Write a GeoDataFrame to GeoJSON.
    '''
    output_path = Path(output_path)
    gdf.to_file(output_path, driver='GeoJSON')

    
    
    

'''
Polygon functions
''' 

def make_hex(center_x, center_y, r):
    '''Flat-top hexagon with circumradius r.'''
    angles = np.deg2rad([0, 60, 120, 180, 240, 300])
    return Polygon([
        (center_x + r * np.cos(a), center_y + r * np.sin(a))
        for a in angles
    ])

def clean_geom(g, min_area):
    '''Fix invalids, remove slivers, collapse multipolygons.'''
    if g.is_empty:
        return None

    # Fix invalid geometries (self-crossing, slivers, etc.)
    g = g.buffer(0)

    if g.is_empty:
        return None

    # If multipolygon, take largest solid piece
    if isinstance(g, MultiPolygon):
        g = max(g.geoms, key=lambda x: x.area)

    # Final sliver removal
    if g.area < min_area:
        return None

    return g


def subdivide_hexagonal(poly, min_area_m2):
    '''
    Subdivide a polygon into equal-area hexagons (flat top) with no gaps.
    Includes sliver removal & geometry cleanup.
    '''
    # Area of flat-top hex: A = (3√3 / 2) * r²
    r = np.sqrt((2 * min_area_m2) / (3 * np.sqrt(3)))

    # Hex spacing (flat-top geometry)
    horiz = 1.5 * r             # center-to-center horizontally
    vert  = np.sqrt(3) * r      # center-to-center vertically

    minx, miny, maxx, maxy = poly.bounds

    hexes = []
    y = miny
    row = 0

    while y <= maxy + vert:
        # offset every other row
        x_start = minx + (0.75 * r if row % 2 else 0)
        
        x = x_start
        while x <= maxx + horiz:
            h = make_hex(x, y, r)
            clipped = poly.intersection(h)

            # Clean + sliver removal injected HERE
            geom = clean_geom(clipped, min_area_m2 * 0.25)

            if geom is not None:
                hexes.append(geom)

            x += horiz
        
        y += vert
        row += 1

    return hexes

    

    

'''
Compute elevation zonal statistics for a gdf of polygons
'''
    
    
def calculate_elevation_statistics(gdf):
    # Compute zonal stats
    slope_stats = zonal_stats(gdf, slope_deg, affine=transform, nodata=np.nan,
                              stats=['mean', 'min', 'max'])
    aspect_stats = zonal_stats(gdf, aspect_deg, affine=transform, nodata=np.nan,
                               stats=['mean', 'min', 'max'])
    
    elev_stats = zonal_stats(gdf, dem, affine=transform, nodata=np.nan,
                             stats=['mean', 'min', 'max'])
    
    elev_dev_stats = zonal_stats(gdf, elev_dev, affine=transform, nodata=np.nan,
                             stats=['mean', 'min', 'max'])
    
    curv_stats = zonal_stats(gdf, curvature, affine=transform, nodata=np.nan,
                         stats=['mean', 'min', 'max'])
    
    profile_curv_stats = zonal_stats(gdf, profile_curv, affine=transform, nodata=np.nan,
                         stats=['mean', 'min', 'max'])

    
    plan_curv_stats = curv_stats = zonal_stats(gdf, plan_curv, affine=transform, nodata=np.nan,
                         stats=['mean', 'min', 'max'])


    # Combine into dataframe
    df_features = pd.DataFrame({
        'plot_id': [s for s in gdf['plot_id'].values],
        'slope_mean': [s['mean'] for s in slope_stats],
        'slope_min': [s['min'] for s in slope_stats],
        'slope_max': [s['max'] for s in slope_stats],
        
        'curve_mean': [s['mean'] for s in curv_stats],
        'curve_min': [s['min'] for s in curv_stats],
        'curve_max': [s['max'] for s in curv_stats],
        
        'pro_curve_mean': [s['mean'] for s in profile_curv_stats],
        'pro_curve_min': [s['min'] for s in profile_curv_stats],
        'pro_curve_max': [s['max'] for s in profile_curv_stats],
        
        'plan_curve_mean': [s['mean'] for s in plan_curv_stats],
        'plan_curve_min': [s['min'] for s in plan_curv_stats],
        'plan_curve_max': [s['max'] for s in plan_curv_stats],
        
        
        'aspect_mean': [s['mean'] for s in aspect_stats],
        'aspect_min': [s['min'] for s in aspect_stats],
        'aspect_max': [s['max'] for s in aspect_stats],
        'elev_min': [s['min'] for s in elev_stats],
        'elev_max': [s['max'] for s in elev_stats],
        'elev_mean': [s['mean'] for s in elev_stats],
        'elev_dev_min': [s['min'] for s in elev_dev_stats],
        'elev_dev_max': [s['max'] for s in elev_dev_stats],
        'elev_dev_mean': [s['mean'] for s in elev_dev_stats]
    })

    df_features = df_features.merge(gdf, how = 'inner', on = 'plot_id')
    df_features['total_relief'] = df_features['elev_max'] - df_features['elev_min']

    gdf_features = gpd.GeoDataFrame(df_features, geometry=gdf.geometry, crs=gdf.crs)
    return gdf_features






def unzip_file(zip_file_path, out_dir):
    with zipfile.ZipFile(zip_file_path, 'r') as z:
        # pick a representative file (e.g. the first in the archive)
        first_member = z.namelist()[0]
        out_path = os.path.join(out_dir, first_member)

        if not os.path.exists(out_path):
            z.extractall(out_dir)
            
        # get a list of files to delete later
        extracted_files = [os.path.join(out_dir, f) for f in z.namelist()]

    return extracted_files


def clip_raster(file_path, weather_value, polygon = vineyard):
    
    with rasterio.open(f) as src:
        for idx, row in vineyard.iterrows():
            geom = [row.geometry.__geo_interface__]

            # clip raster to polygon
            out_image, out_transform = mask(src, geom, crop=True)
            data = out_image[0]

            # ignore no-data values
            nodata = src.nodata if src.nodata is not None else -9999
            vals = data[data != nodata]

            if len(vals) > 0:
                n_val = len(vals)
                value = float(vals)
                value_mean = float(np.mean(vals))
            else:
                mean_val, min_val = np.nan, np.nan
            
            return {
                'date':date, 
                'n':n_val,
                f'{weather_value}':value,
                # f'{weather_value}_mean':value_mean,
                # f'{weather_value}_std':value_std
            }

        
def delete_extracted_files(file_list):
    for f in file_list:
        if os.path.exists(f):
            os.remove(f)