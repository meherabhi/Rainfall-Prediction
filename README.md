# Rainfall-Prediction
The RBF file works on any .nc file.

Specify the number of clusters you would like to use, by default it is set to 100.

The output is of 52x1 [ Assuming a unique temperature distribution for each of 52 weeks of a year ]  dimension which gives us the per-week distribution of the data.

Now the code is set to run.

Task-2:

For a random location in the grid if the data for that point is not present, the environmental conditions can be approximated by the known values around it within a radius of 10km.

Proof:

I have taken 4 coordinates around the location [latitide, longitude]=[ 27.315,91.4062], and plotted the data trend by joining the cluster centers.

No of clusters=50.

The correlation coefficient between the data of

1st-2nd point = 0.945, 2nd-3rd = 0.886, 3rd-4th = 0.992, 1st-4th = 0.916.

The plots are also available in combinedplot.png in the repository.

These high values of correlation coefficient is a clear indication of how strongly connected the data is, and hence can be approximated.
