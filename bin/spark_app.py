import sys
from operator import add

from pyspark.sql import SparkSession


if __name__ == "__main__":

    spark = SparkSession\
        .builder\
        .appName("Ryan Airflow Test")\
        .getOrCreate()

    result = spark.sparkContext.parallelize([1,2,3,4]).glom().collect()
    print("result %s" % (str(result),))
