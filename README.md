# MCDMovie (Mars Climate Database Movie) 

MCDMovie utilises the Mars Climate Database full version 5.3 to generate global visualisations of Mars and the Martian atmosphere. 

1. MCDMovie example images.
![Teaser image](./images/test0.jpg)

2. MCDMovie example images. 
![Teaser image](./images/test1.jpg)

The goal of MCDMovie is to generate visualisations of the Martian atmosphere. The above example shows... COVID-19 chest x-ray imagery is sparse, whilst the 'COVID-19 image data collection' is invaluable, it is a relatively small dataset. MCDMovie , through the MCD, offers the possibility generating a very large synthetic database of Martian atmospheric imagery, which could be linked to MSSS MRO MARCI weather imagery, http://www.msss.com/msss_images/subject/weather_reports.html. 

the data used to create the visualisations is from the Mars Climate Database (MCD) (Version 5.2). The Mars Climate Database is a database which contains the output of a Global Climate Model. The GCM was developed predominately by the LMD with contributions from the OU, Oxford, ESA and CNES and the Instituto de Astrofisica de Andalucia and is validated using observational data. 

# MCD Documentation

The MCD User Manual and the MCD Detailed Design Document can be found on the following documentation page: http://www-mars.lmd.jussieu.fr/mars/info_web/. 

The full version includes a basic python script that allows one to just select a particular atmospheric property, at one height, at a particular longitude and latitude point, at a particular solar longitude, at a particular local time. Generating global visualisations requires modifying the basic script to loop over a latitude-longitude grid to select an atmospheric property at a particular height. Furthermore, modifying the script to take into account that each different longitude will have a different local time and each longitude must also update its local time correctly each timestep. Furthermore, as time increases the solar longitude of Mars increases. These are not inbuilt to the basic script. Then the latitude-longitude grid has to be mapped from cartesian coordinates into spherical coordinates. 

# Requirements

1. The MCD 5.3 Full version. In order to obtain a copy of the MCD v5.3 contact forget@lmd.jussieu.fr or millour@lmd.jussieu.fr.
2. ffmpeg. 
3. numpy.
4. Basemap.
5. matplotlib.

# Colab
The following notebook MCDMovie.ipynb run on Colab provides access to the MCDMovie.

# Contact
George Cann, Department of Space and Climate Physics (Mullard Space Science Laboratory), University College London.
Email: george.cann.15@ucl.ac.uk. 

# Citation
```
1. George Cann
MCDMovie, (2020)
https://github.com/ghcann/MCDMovie
```

```
@article{cann_mcd_movie
  title={MCDMovie},
  author={George Cann},
  journal={arXiv TBC},
  url={https://github.com/ghcann/MCDMovie},
  year={2020}
}
```

# Acknowledgements

The author would like to thank University College London, Open University, University of Oxford, European Space Agency and CNES and the Instituto de Astrofisica de Andalucia. 
