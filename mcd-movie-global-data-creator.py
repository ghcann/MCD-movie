# This python program illustrates how the Mars Climate Database can be used to produce 
# global videos of the Martian climate over the entire Ls

from fmcd import call_mcd,julian
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp
import bokeh.plotting
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColorMapper, Ticker, ColorBar
from io import StringIO

# 1. Inputs:
dset = ' ' # default to 'MCD_DATA'
perturkey = 1 # default to no perturbation
seedin = 0 # perturbation seed (unused if perturkey=1)
gwlength = 0 # Gravity Wave length for perturbations (unused if perturkey=1)

# 1.1 Dates
choice_date=raw_input('Use Earth date (e) or Mars date (m)?')
if (choice_date == "e") :
  datekey=0 # Earth date
  loct=0 # local time must then also be set to zero
  day,month,year,hour,minute,second = \
  raw_input("Enter date: day/month/year/hour/minute/second: ").split('/')
  day=int(day)
  month=int(month)
  year=int(year)
  hour=int(hour)
  minute=int(minute)
  second=int(second)
  # now call Julian routine to convert to julian date
  (ier,xdate)=julian(month,day,year,hour,minute,second)
  print(" Julian date %16.8f" % xdate)
else :
  datekey=1 # Mars date
  xdate=float(raw_input("Enter solar longitude Ls (deg.):"))
  loct=float(raw_input("Local time (0 < time < 24)?"))

# 1.2 Vertical coordinate
zkey=int(raw_input("Select verical coordinate type (1: distance to center of planet, 2: height above areoid, 3: height above surface, 4: Pressure) "))
if (zkey == 1) :
  xz=float(raw_input("Enter distance to planet center (m) "))
if (zkey == 2) :
  xz=float(raw_input("Enter altitude above areoid (m) "))
if (zkey == 3) :
  xz=float(raw_input("Enter altitude above surface (m) "))
if (zkey == 4) :
  xz=float(raw_input("Enter pressure value (Pa) "))

# high resolution mode
hrkey=int(raw_input("High resolution? (1: yes, 0: no) "))

# 1.3 Position
lat = float(raw_input('Latitude (deg)?'))
lon = float(raw_input('Longitude (deg)?'))

# 1.4 Dust and solar scenario
print("Dust scenario?")
print("1= Climatology       typical Mars year dust scenario")
print("                     average solar EUV conditions")
print("2= Climatology       typical Mars year dust scenario")
print("                     minimum solar EUV conditions")
print("3= Climatology       typical Mars year dust scenario")
print("                     maximum solar EUV conditions")
print("4= dust storm        constant dust opacity = 5 (dark dust)")
print("                     minimum solar EUV conditions")
print("5= dust storm        constant dust opacity = 5 (dark dust)")
print("                     average solar EUV conditions")
print("6= dust storm        constant dust opacity = 5 (dark dust)")
print("                     maximum solar EUV conditions")
print("7= warm scenario     dustier than Climatology scenario")
print("                     maximum solar EUV conditions")
print("8= cold scenario     clearer than Climatology scenario")
print("                     minimum solar EUV conditions")
dust=int(raw_input(''))

# 1.5 perturbations
perturkey=int(raw_input("Perturbation? (1:none, 2: large scale, 3: small scale, 4: small+large, 5: n sigmas) "))
if (perturkey > 1) :
  seedin=int(raw_input("seedin? (only matters if adding perturbations) "))
if ((perturkey == 3) or (perturkey == 4)) :
  gwlength=float(raw_input("Gravity wave length? (for small scale perturbations) "))

# 1.6 extra outputs
# here we only implement an all-or-nothing case
extvarkey=int(raw_input("Output the extra variables? (yes==1; no==0) "))
if (extvarkey == 0) :
  extvarkeys = np.zeros(100)
else :
  extvarkeys = np.ones(100)

# 2. Perform calls to MCD

# 2.1 Set the number of latitude and longitude points 
longitude_points = int(360/lon)
latitude_points = int(180/lat)

# 2.2 Print out the temperature at 1000 m above the surface 
 
# Initialise call_mcd ls loop
k=0

# Set Martian map grid
delta = 1.0
x = np.arange(0.0, 360.0, delta)
y = np.arange(-90.0, 90.0, delta)
X, Y = np.meshgrid(x, y)

# Set figure font size, note with every incremental increase in Ls change local time by 1 hour
mpl.rcParams.update({'font.size': 25})

# Set the background to be black (like space)
plt.style.use('dark_background')

for l in range(1):
    print("\n")
    print("Mars Hour %d running." % l)
    print("\n")
    text_file = open("mcd_spherical_temp%d.txt" % l, "w")
    text_file_alt = open("mcd_spherical_alt_%d.txt" % l, "w")
    row = np.zeros((1,1))
    altitude_row = np.zeros((1,1))
    i = 0
    j = 0
    for j in range(latitude_points):
        for i in range(longitude_points):
            (pres, dens, temp, zonwind, merwind, \
            meanvar, extvar, seedout, ierr) \
            = \
            call_mcd(zkey,xz,lon*i,(lat*j)-90,hrkey, \
            datekey,xdate*l,((((i*24.0)/360.0) +(l%24.0))%24.0),dset,dust, \
            perturkey,seedin,gwlength,extvarkeys)
            new_row = np.array([temp])
            row = np.vstack([row, new_row])
            new_row_altitude = np.array([extvar[3]])
            altitude_row = np.vstack([altitude_row, new_row_altitude])
            text_file.write("%e" % temp)
            text_file.write("\n")
            text_file_alt.write("%e" % extvar[3])
            text_file_alt.write("\n")
    # Print out the completion of the lth iteration
    print("\n")
    print("Mars Hour %d complete." % l)
    print("\n")
    
    # Reshape rows for plotting
    #temp_array = np.reshape(row[1:,0], (180,360))
    #altitude_row = np.reshape(altitude_row[1:,0], (180,360))
    '''
    pres_array = np.reshape(row[1:,1], (180,360))
    co2_array = np.reshape(row[1:,2], (180,360))
    n2_array = np.reshape(row[1:,3], (180,360))
    ar_array = np.reshape(row[1:,4], (180,360))
    h2o_array = np.reshape(row[1:,5], (180,360))
    co_array = np.reshape(row[1:,6], (180,360))
    o_array = np.reshape(row[1:,7], (180,360))
    o2_array = np.reshape(row[1:,8], (180,360))
    o3_array = np.reshape(row[1:,9], (180,360))
    h2_array = np.reshape(row[1:,10], (180,360))
    h2o_ice_array = np.reshape(row[1:,11], (180,360))
    dust_effrad_array = np.reshape(row[1:,12], (180,360))
    h2o_ice_effrad_array = np.reshape(row[1:,13], (180,360))
    surface_temp_array = np.reshape(row[1:,14], (180,360))
    solar_flux_to_space_array = np.reshape(row[1:,15], (180,360))
    thermal_ir_flux_to_surface_array = np.reshape(row[1:,16], (180,360))
    solar_flux_to_surface_array = np.reshape(row[1:,17], (180,360))
    thermal_ir_flux_to_space_array = np.reshape(row[1:,18], (180,360))
    h2o_ice_seasonal_frost_layer = np.reshape(row[1:,19], (180,360))
    co2_ice_layer = np.reshape(row[1:,20], (180,360))
    dust_optdep_array = np.reshape(row[1:,21], (180,360))
    

    # random data, this probably needs to change using MCD data
    nrows, ncols = (180,360)
    lon, lat = np.meshgrid(np.linspace(0,360,ncols), np.linspace(-90,90,nrows))
    print("lon shape")
    print(np.shape(lon))
    print("lat shape")
    print(np.shape(lat))
    xg,yg,zg = sph2cart(lon,lat)

    # set up map projection
    # Change this line to change the viewing angle of the planet
    for m in range(360):
        plt.figure(figsize=(30, 14))
        map = Basemap(projection='ortho', lat_0=45, lon_0=m)
        # draw lat/lon grid lines every 30 degrees.
        map.drawmeridians(np.arange(0, 360, 30))
        map.drawparallels(np.arange(-90, 90, 10))
        # compute native map projection coordinates of lat/lon grid.
        x, y = map(lon, lat)
        # contour data over the map. Change the last number for a smoother "heatmap" atmosphere
        cs = map.contourf(x, y, temp_array, 50)
        plt.title('Contours of T')
        plt.savefig("mcd_heatmap_%d.png" % m)
        print("heatmap %d" % m)

    
    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot temperature 
    CS = plt.contour(X, Y, temp_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, temp_array, cmap=plt.cm.get_cmap('jet'))
    plt.colorbar(label='Temperature (K)')
    plt.clim(140,260)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian atmospheric temperature (K) at 1 m above the local surface at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_temp_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot pressure
    CS = plt.contour(X, Y, pres_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, pres_array, cmap=plt.cm.get_cmap('jet'))
    plt.colorbar(label='Pressure (Pa)')
    plt.clim(0,1300)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian atmospheric pressure (Pa) at 1 m above the local surface at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_pres_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot CO2 VMR
    CS = plt.contour(X, Y, co2_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, co2_array, cmap=plt.cm.get_cmap('Greys'))
    plt.colorbar(label='CO2 VMR (ppmv)')
    plt.clim(960000,969000)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian atmospheric CO2 VMR (ppmv) at 1m above the local surface at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_co2_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot N2 VMR
    CS = plt.contour(X, Y, n2_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, n2_array, cmap=plt.cm.get_cmap('Greens'))
    plt.colorbar(label='N2 VMR (ppmv)')
    plt.clim(10000,19000)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian atmospheric N2 VMR (ppmv) at 1m above the local surface at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_n2_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

     # Plot Ar VMR
    CS = plt.contour(X, Y, ar_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, ar_array, cmap=plt.cm.get_cmap('copper_r'))
    plt.colorbar(label='Ar VMR (ppmv)')
    plt.clim(15000,20000)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian atmospheric Ar VMR (ppmv) at 1m above the local surface at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_ar_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot H20 VMR
    CS = plt.contour(X, Y, h2o_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, h2o_array, cmap=plt.cm.get_cmap('Blues'))
    plt.colorbar(label='H20 VMR (ppmv)')
    plt.clim(0,210)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian atmospheric H20 VMR (ppmv) at 1m above the local surface at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_h2o_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot C0 VMR
    CS = plt.contour(X, Y, co_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, co_array, cmap=plt.cm.get_cmap('spring_r'))
    plt.colorbar(label='CO VMR (ppmv)')
    plt.clim(500,710)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian atmospheric CO VMR (ppmv) at 1m above the local surface at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_co_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot 0 VMR
    CS = plt.contour(X, Y, o_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, o_array, cmap=plt.cm.get_cmap('Purples'))
    plt.colorbar(label='O VMR (ppmv)')
    plt.clim(0,0.0015)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian atmospheric O VMR (ppmv) at 1m above the local surface at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_o_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot 02 VMR
    CS = plt.contour(X, Y, o2_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, o2_array, cmap=plt.cm.get_cmap('plasma'))
    plt.colorbar(label='O2 VMR (ppmv)')
    plt.clim(1000,1500)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian atmospheric O2 VMR (ppmv) at 1m above the local surface at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_o2_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot 03 VMR
    CS = plt.contour(X, Y, o3_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, o3_array, cmap=plt.cm.get_cmap('summer'))
    plt.colorbar(label='O3 VMR (ppmv)')
    plt.clim(0,0.35)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian atmospheric O3 VMR (ppmv) at 1m above the local surface at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_o3_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot H2 VMR
    CS = plt.contour(X, Y, h2_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, h2_array, cmap=plt.cm.get_cmap('winter'))
    plt.colorbar(label='H2 VMR (ppmv)')
    plt.clim(13,18)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian atmospheric H2 VMR (ppmv) at 1m above the local surface at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_h2_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot H20 ice VMR
    CS = plt.contour(X, Y, h2o_ice_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, h2o_ice_array, cmap=plt.cm.get_cmap('bone'))
    plt.colorbar(label='H2O ice VMR (ppmv)')
    plt.clim(0,200)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian atmospheric H2O ice VMR (ppmv) at 1m above the local surface at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_h2o_ice_%d_1m.png" % k, bbox_inches='tight')


    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot H2O Ice Effective Radius
    CS = plt.contour(X, Y, h2o_ice_effrad_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, h2o_ice_effrad_array, cmap=plt.cm.get_cmap('PuBu_r'))
    plt.colorbar(label='H20 Ice Effective Radius ($\mu$m)')
    plt.clim(0,120)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian atmospheric H2O ice effective radius ($\mu$m) at 1m above the local surface at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_h2o_ice_effrad_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot Mars surface temperature 
    CS = plt.contour(X, Y, surface_temp_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, surface_temp_array, cmap=plt.cm.get_cmap('jet'))
    plt.colorbar(label='Surface Temperature (K)')
    plt.clim(100,300)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian surface temperature (K) at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_surface_temp_%d_1m.png" % k, bbox_inches='tight')

    ##### Radiative transfer quantities of interest #####

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot Mars thermal ir flux to surface 
    CS = plt.contour(X, Y, thermal_ir_flux_to_surface_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, thermal_ir_flux_to_surface_array, cmap=plt.cm.get_cmap('afmhot'))
    plt.colorbar(label='Thermal IR flux to surface (W/m2)')
    plt.clim(0,70)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian thermal IR flux to surface (W/m2) at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_thermal_ir_flux_to_surface_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot Mars thermal ir flux to space 
    CS = plt.contour(X, Y, thermal_ir_flux_to_space_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, thermal_ir_flux_to_space_array, cmap=plt.cm.get_cmap('afmhot'))
    plt.colorbar(label='Thermal IR flux to space (W/m2)')
    plt.clim(0,350)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian thermal IR flux to space (W/m2) at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_thermal_ir_flux_to_space_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot Mars solar flux to surface 
    CS = plt.contour(X, Y, solar_flux_to_surface_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, solar_flux_to_surface_array, cmap=plt.cm.get_cmap('afmhot'))
    plt.colorbar(label='Solar flux to surface (W/m2)')
    plt.clim(0,650)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian solar flux to surface (W/m2) at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_solar_flux_to_surface_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot Mars solar flux reflected to space 
    CS = plt.contour(X, Y, solar_flux_to_space_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, solar_flux_to_space_array, cmap=plt.cm.get_cmap('afmhot'))
    plt.colorbar(label='Solar flux reflected to space (W/m2)')
    plt.clim(0,180)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian solar flux reflected to space (W/m2) at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_solar_flux_to_space_%d_1m.png" % k, bbox_inches='tight')

    ##### Dust quantities of interest #####

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot Dust Effective Radius
    CS = plt.contour(X, Y, dust_effrad_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, dust_effrad_array, cmap=plt.cm.get_cmap('pink_r'))
    plt.colorbar(label='Dust Effective Radius ($\mu$m)')
    plt.clim(1,2)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian atmospheric dust effective radius ($\mu$m) at 10km above the local surface at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_dust_effrad_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot dust column visible optical depth.
    CS = plt.contour(X, Y, dust_optdep_array, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, dust_optdep_array, cmap=plt.cm.get_cmap('YlOrBr'))
    plt.colorbar(label='Dust column visible optical depth')
    plt.clim(0,1)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian dust column visible optical depth from local surface to the top of the atmosphere \n at Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_dust_optdep_%d_1m.png" % k, bbox_inches='tight')
    
    ##### Glaciology quantities of interest #####

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot surface H2O ice (seasonal frost) layer
    CS = plt.contour(X, Y, h2o_ice_seasonal_frost_layer, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, h2o_ice_seasonal_frost_layer, cmap=plt.cm.get_cmap('rainbow'))
    plt.colorbar(label='Surface H2O ice (seasonal frost) layer (kg/m2)')
    plt.clim(0,0.5)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian surface H2O ice (seasonal frost) layer (kg/m2) at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars_h2o_ice_seasonal_frost_layer_%d_1m.png" % k, bbox_inches='tight')

    # Plot Mars surface altitude contours 
    plt.figure(figsize=(40.01, 18))
    CS_altitude = plt.contour(X, Y, altitude_row, 20, colors='grey')
    plt.clabel(CS_altitude, inline=1, fontsize=10)

    # Plot surface CO2 ice (seasonal frost) layer
    CS = plt.contour(X, Y, co2_ice_layer, 20, colors='w')
    plt.clabel(CS, inline=1, fontsize=10)
    plt.xlabel('\n Longitude $^\circ$', fontsize=25)
    plt.ylabel('\n Latitude $^\circ$', fontsize=25)
    plt.pcolormesh(X, Y, co2_ice_layer, cmap=plt.cm.get_cmap('gnuplot2'))
    plt.colorbar(label='Surface CO2 ice layer (kg/m2)')
    plt.clim(0,1700)
    plt.grid()
    x = np.array(np.arange(0, 360, 30))
    y = np.array(np.arange(-90, 90, 15))
    lon_xticks = ['0$^\circ$E','30$^\circ$E','60$^\circ$E','90$^\circ$E','120$^\circ$E','150$^\circ$E','180$^\circ$E','210$^\circ$E','240$^\circ$E','270$^\circ$E','300$^\circ$E','330$^\circ$E']
    lat_yticks = ['90$^\circ$S','75$^\circ$S','60$^\circ$S','45$^\circ$S','30$^\circ$S','15$^\circ$S','0$^\circ$','15$^\circ$N','30$^\circ$N','45$^\circ$N','60$^\circ$N','75$^\circ$N']
    plt.xticks(x, lon_xticks)
    plt.yticks(y, lat_yticks)
    plt.title('A global map of Martian surface CO2 ice layer (kg/m2) at \n Ls = %f $^\circ$ MCDv5.2 with average solar scenario climatology. Credit: LMD\OU\IAA\ESA\CNES\GeorgeCann. \n' % (xdate*k), fontsize=30)
    plt.savefig("global_mars__co2_ice_layer_%d_1m.png" % k, bbox_inches='tight')
    '''





