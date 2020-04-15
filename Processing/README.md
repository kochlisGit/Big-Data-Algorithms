# Fast Processing Methods

In this project, I'd like to introduce some fast and effective methods for processing big data in python. As You know, Python offers many ways and libraries to help You code and process data fast, such as pandas, dask, etc. However, in this project, we will do it with the simpliest way possible to mine data pretty fast, using standard python libraries only.

1. Reading the data

This article does a pretty good job testing all popular methods for reading csv data: https://medium.com/casual-inference/the-most-time-efficient-ways-to-import-csv-data-in-python-cc159b44063d

It turns out, python's CSV library is the fastest way to do it, no matter how large is the dataset. However, it comes with a drawback. CSV **returns data in lines, as strings**. Other libraries also guess the data types of each column. However, You can read data pretty fast, without having to load all the data in the memory.

2. Memory usage

When working with big data, the most often problem You encounter is the memory. If the data exceeds 1GB, then in a normal computer it becomes impossible to load all the data at once. Even If your computer has enough memory to fit in all the data, then the process becomes slow. One way to deal with it is process the data as you read them (Line - By Line).

In this project, we have a users-movies-ratings dataset from kaggle. I have uploaded a smaller dataset, so that You can test the code, but You could also download the whole dataset (700MB) from kaggle: https://www.kaggle.com/rounakbanik/the-movies-dataset

We would like to count the average rating that leaves every user. Also, we would like to find the average rating of every movie. In my program, You can see how easily it easy to do it and It's actually pretty fast.
