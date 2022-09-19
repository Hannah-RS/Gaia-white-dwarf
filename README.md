# Gaia-white-dwarfs
Simulation data and code for 'Can Gaia Find Planets Around White Dwarfs' H. Sanderson et al. 2022 (submitted to MNRAS)

This code can be downloaded along with the eDR3 white dwarf catalogue from Gentile Fusillo et al. (2021) https://doi.org/10.1093/mnras/stab2672 in order to reproduce all the calculations and figures in the paper. 

The code is organised as follows:

+ Catalogue
  + Code for importing and filtering the eDR3 white dwarf catalogue. 
  + Resulting filtered catalogues are in Data subfolder
  + Produces Figure 7
  + Data subfolder also contains a full version of the table in Appendix 3 (SN_1mj) that will also be uploaded to Vizier.
+ Detection_probability
  + Code for calculating $p_{ljk}$
  + Produces Figure 3
+ Distribution
  + Code for calculating $\frac{d^2N_{WD}}{da dlog M}$
  + Categorises simulated planets by their ability to pollute white dwarfs
  + Produces Figure 4, 5a and 5b (annotations added in Inkscape), 8
  + Appendix subfolder contains the code for A1 and A2
  + simulation_data subfolder contains the results of the simulations
+ Gaia
  + Calculates detection limits for a generic magnitude 15 white dwarf
  + Produces Figures 1 and 2
+ Gaia error - text file of Gaia error as a function of magnitude from https://www.cosmos.esa.int/web/gaia/science-performance - these values are equivalent to putting each magnitude into equation 4 and 5
+ Planet detections - Jupyter notebook for calculating $\frac{d^2N_{det}}{da dlogM}$ and calculating summary statistics
  + Produces Figure 6
+ Tides
  + Jupyter notebooks for computing survivability and final orbits of planets orbiting AGB stars (see 
Mustill & Villaver, 2012, ApJ, 761, 121)
  + AGB model files from Vassiliadis & Wood (1993, ApJ, 413, 641) required for above calculation
  + Results of this model are in Distribution/simulation_data

## I want to...

### Create a map of detection probability for a particular candidate
Go to Detection_probability and use the Candidate detection probability notebook. Enter your candidate distance and Gaia broadband magnitude in code cell 3 and run the whole notebook.

### Look at the planets that will be detected around a subset of white dwarfs

1. Download the eDR3 catalogue
2. Use Catalogue/import_data to get the subset of white dwarf parameters you are interested in
3. Use Catalogue/transform_data to filter your catalogue to get the subset you are interested
4. Run Detection_probability/total_detection_probability with your subset to get $p_{jk}$
5. Run the planet detections Jupyter notebook with your chosen $p_{jk}$ file

## Questions?
Contact H. Sanderson on the corresponding author address on H. Sanderson et al. (2022)

## Credits
If you use any part of this code in your work please cite Sanderson et al. (2022) (https://arxiv.org/abs/2206.02505). If you use the post-main sequence planet and stellar evolution model please cite Mustill & Villaver (2012) (https://doi.org/10.1088/0004-637X/761/2/121)

H. Sanderson wrote all the code in this repository except the post-main sequence planet and stellar evolution model in the Tides subdirectory written by A. J. Mustill and explained in Mustill, Alexander James, and Eva Villaver. 2012. ‘Foretellings of Ragnar\"ok: World-Engulfing Asymptotic Giants and the Inheritance of White Dwarfs’. The Astrophysical Journal 761 (2): 121. https://doi.org/10.1088/0004-637X/761/2/121.
The detection probabilities as a function of astrometric S/N and period come from Ranalli et al. (2018) ‘Astrometry and Exoplanets in the Gaia Era: A Bayesian Approach to Detection and Parameter Recovery’. Astronomy & Astrophysics 614 (June): A30. https://doi.org/10.1051/0004-6361/201730921 and were helpfully rebinned from hexagonal to rectangular bins by Piero Ranalli.

