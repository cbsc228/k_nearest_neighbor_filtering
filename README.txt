K Nearest Neighbor Filtering

----DESCRIPTION----
This program implements k nearest neighbor collaborative filtering, holding k = 3 in project2.py,
and then performing cross validation for k values 1-5 in cross_val.py. The program attempts to match
people to movies that they will likely enjoy based on ratings they have provided. The included data sets are as follows:

1) u1-base.base: This is the training set. It contains data on the ratings that individual users gave to various movies.
It contains four columns that refer to a user ID, the index of the movie being rated, the rating given (on a scale of 1-5),
and when the rating was given (not important for this assignment), respectively. 
	
2) u1-test.test: This is the test set. It also contains data on the ratings that individual users gave to various movies;
however, IT SHOULD NOT BE USED FOR TRAINING! As with the training set, it contains four columns that refer to a user ID,
the index of the movie being rated, the rating given (on a scale of 1-5), and when the rating was given, respectively.