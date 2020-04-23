import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib as mpl

# Set the background to be black (like space)
plt.style.use('dark_background')
mpl.rcParams.update({'font.size': 25})

nrows, ncols = (180,360)
lon, lat = np.meshgrid(np.linspace(0,360,ncols), np.linspace(-90,90,nrows))
print("lon shape")
print(np.shape(lon))
print("lat shape")
print(np.shape(lat))
xg,yg,zg = sph2cart(lon,lat)

# Open mcd_spherical_temp files
for l in range(360):
    print("Open mcd_spherical_%d \n" % (l%24))
    print("Mars Hour %d running." % (l%24))
    print("\n")
    row = np.genfromtxt("mcd_spherical_%d.txt" % (l%24))
    altitude_row = np.genfromtxt("mcd_spherical_alt_0.txt")

    # Include
    temp_array = np.reshape(row[0:,8], (180,360))
    alt_array = np.reshape(altitude_row, (180,360))
    #radius_to_planet = np.reshape(row[1:,0], (180,360))
    #mars_hour = np.reshape(row[1:,3], (180,360))
    #altitude_above_aeroid = np.reshape(row[1:,5], (180,360))
    ls = np.reshape(row[0:,6], (180,360))
    #ltst = np.reshape(row[1:,7], (180,360))
    pres_array = np.reshape(row[0:,9], (180,360))
    co2_array = np.reshape(row[0:,10], (180,360))
    n2_array = np.reshape(row[0:,11], (180,360))
    ar_array = np.reshape(row[0:,12], (180,360))
    h2o_array = np.reshape(row[0:,13], (180,360))
    co_array = np.reshape(row[0:,14], (180,360))
    o_array = np.reshape(row[0:,15], (180,360))
    o2_array = np.reshape(row[0:,16], (180,360))
    o3_array = np.reshape(row[0:,17], (180,360))
    h2_array = np.reshape(row[0:,18], (180,360))
    h2o_ice_array = np.reshape(row[0:,19], (180,360))
    dust_effrad_array = np.reshape(row[0:,20], (180,360))
    h2o_ice_effrad_array = np.reshape(row[0:,21], (180,360))
    surface_temp_array = np.reshape(row[0:,22], (180,360))
    solar_flux_to_space_array = np.reshape(row[0:,23], (180,360))
    thermal_ir_flux_to_surface_array = np.reshape(row[0:,24], (180,360))
    solar_flux_to_surface_array = np.reshape(row[0:,25], (180,360))
    thermal_ir_flux_to_space_array = np.reshape(row[0:,26], (180,360))
    h2o_ice_seasonal_frost_layer = np.reshape(row[0:,27], (180,360))
    co2_ice_layer = np.reshape(row[0:,28], (180,360))
    
    # create a 4K resolution figure
    plt.figure(figsize=(38.4, 21.6))
    map = Basemap(projection='ortho', lat_0=45, lon_0=l)
    # draw lat/lon grid lines every 30 degrees.
    map.drawmeridians(np.arange(0, 360, 30))
    map.drawparallels(np.arange(-90, 90, 10))
    # compute native map projection coordinates of lat/lon grid.
    x, y = map(lon, lat)
    levels_alt = np.linspace(-8000, 21000, 30)
    levels_temp = np.linspace(140, 270, 130)
    # contour data over the map. Change the last number for a smoother "heatmap" atmosphere
    cs = map.contourf(x, y, temp_array, levels_temp, cmap=plt.cm.get_cmap('jet'))
    plt.colorbar(label='Temperature (K)')
    plt.clim(140,270)
    cs_alt = map.contour(x, y, alt_array, levels_alt, colors='grey')
    plt.title('A global map of Martian atmospheric temperature (K) at 1000 m altitude above the local surface, local time %d.0 Mars hour (at longitude 0), Ls %f, \n sub-viewing latitude and longitude (45S,%dE),MCDv5.2 with average solar scenario climatology. Credit: /LMD/OU/IAA/ESA/CNES/UCL. \n' % ((l%24),ls[1,1],l), fontsize=30)
    plt.savefig("mcd_spherical_temp_lon_0_%d.png" % l)
    print("mcd_spherical_temp %d" % l)

    # create a 4K resolution figure
    plt.figure(figsize=(38.4, 21.6))
    map = Basemap(projection='ortho', lat_0=45, lon_0=l)
    # draw lat/lon grid lines every 30 degrees.
    map.drawmeridians(np.arange(0, 360, 30))
    map.drawparallels(np.arange(-90, 90, 10))
    # compute native map projection coordinates of lat/lon grid.
    x, y = map(lon, lat)
    levels_alt = np.linspace(-8000, 21000, 30)
    levels_h2o = np.linspace(0, 200, 100)
    # contour data over the map. Change the last number for a smoother "heatmap" atmosphere
    cs = map.contourf(x, y, h2o_array, levels_h2o, cmap=plt.cm.get_cmap('jet'))
    plt.colorbar(label='H2O Volume Mixing Ratio (ppmv)')
    plt.clim(0,200)
    cs_alt = map.contour(x, y, alt_array, levels_alt, colors='grey')
    plt.title('A global map of Martian atmospheric H2O VMR (ppmv) at 1000 m altitude above the local surface, local time %d.0 Mars hour (at longitude 0), Ls %f, \n sub-viewing latitude and longitude (45N,%dE), MCDv5.2 with average solar scenario climatology. Credit: /LMD/OU/IAA/ESA/CNES/UCL. \n' % ((l%24),ls[1,1],l), fontsize=30)
    plt.savefig("mcd_spherical_h2o_lon_0_%d.png" % l)
    print("mcd_spherical_h2o %d" % l)

    # create a 4K resolution figure
    plt.figure(figsize=(38.4, 21.6))
    map = Basemap(projection='ortho', lat_0=45, lon_0=l)
    # draw lat/lon grid lines every 30 degrees.
    map.drawmeridians(np.arange(0, 360, 30))
    map.drawparallels(np.arange(-90, 90, 10))
    # compute native map projection coordinates of lat/lon grid.
    x, y = map(lon, lat)
    levels_alt = np.linspace(-8000, 21000, 30)
    levels_pres = np.linspace(0, 1200, 200)
    # contour data over the map. Change the last number for a smoother "heatmap" atmosphere
    cs = map.contourf(x, y, pres_array, levels_pres, cmap=plt.cm.get_cmap('jet'))
    plt.colorbar(label='Pressure (Pa)')
    plt.clim(0,1200)
    cs_alt = map.contour(x, y, alt_array, levels_alt, colors='grey')
    plt.title('A global map of Martian atmospheric pressure (Pa) at 1000 m altitude above the local surface, local time %d.0 Mars hour (at longitude 0), Ls %f, \n sub-viewing latitude and longitude (45N,%dE), MCDv5.2 with average solar scenario climatology. Credit: /LMD/OU/IAA/ESA/CNES/UCL. \n' % ((l%24),ls[1,1],l), fontsize=30)
    plt.savefig("mcd_spherical_pres_lon_0_%d.png" % l)
    print("mcd_spherical_pres %d" % l)


