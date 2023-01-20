# spurs_dataset

#### **1. Create table script:** https://github.com/ninanguyen24/spurs_dataset/blob/main/Tables_DDL.sql

Indexes can be created on columns that are frequently searched or joined. For example, gameid from games table, teamid from teams table, or playerid from players table.

I separated teams and players so they can be used in other queries as well because there's only 30 NBA teams and the players table can be maintained separately.

#### **2. Upload script:** https://github.com/ninanguyen24/spurs_dataset/blob/main/LoadData.py 

Parameter can be introduced to take in file name instead of hardcoding. And right now duplicate keys is just being ignored, code can be enhanced to update the data by using merge or deleting the row and re-inserting.

#### **3. If traditional database is having issues, describe how you would you go about processing and storing this type of data for easy access/use by our data scientists.**

I reccommend taking advantage of big data technologies like Apache Hadoop or Apache Spark. They are designed to handle and process large amount of data in a distributed and parallel manner. 

- Steps I would take to process and store the data:
    1. I would start by loading the data into a distributed file system such as HDFS (Hadoop Distributed File System) or S3 (Simple Storage Service). This will allow for easy access to the data by the data processing tools. THis mainly supports OLAP big data design. Given this, the tradeoff here will be ACID properties and referrial integrity which we otherwise benefit from OLTP but are not strictly enforced in OLAP
    
    <br>
    
    2. I would use Apache Spark to process the data and extract the relevant features. Spark allows for easy and efficient data processing using its DataFrame and SQL API's. I can use Spark SQL to perform the filtering, cleaning, and transformation of the data.
    
    <br>
    
    3. Once the data is cleaned and transformed, I would use Apache Parquet to store the data. Parquet is a columnar storage format that is optimized for big data processing and provides great performance improvements when compared to row-based storage formats like CSV or JSON.
    
    <br>
    
    4. To access the data, I would use a data processing and querying tool like Apache Hive, Presto, or Impala. These tools provide SQL-like interface to query the data stored in the parquet format, making it easy for data scientists to analyze and process the data.
    
    <br>
    
    5. To visualize the data and create dashboards, I would use a tool like Apache Superset, Tableau or Looker. These tools are designed to work with big data and provide an easy-to-use interface for data exploration and visualization.
    
    <br>
    
    6. For further optimization, if data arrives momementarily within each day. I'd design stream processing for data ingestion using Apache Kafka and micro-batch processing using Spark Streaming. Some potential pitfalls for stream are data loss and recovery for each stream. Will need to use checkpoint to recover data loss. Reprocessing and backfill can be complex with stream, which require additional mechaism within processing logic to handle.
 

#### **Are there any potential pitfalls or complications that you'd want to plan ahead of time for?**

Potential pitfalls or complications that I would want to plan ahead of time for include data quality and data privacy issues. I would need to ensure that the data is cleaned and transformed properly to avoid errors and inconsistencies in the final data set. It's also important to communicate with the Analysts and Scientists that will use the data to agree on the structure of the data. Additionally, I would need to ensure that the data is stored and processed in compliance with data privacy regulations. All the while keeping in mind the storage and processing cost.

In summary, I would use big data technologies such as Hadoop, Spark and Parquet to handle and process the large volume of data, and data processing and querying tools like Hive, Presto or Impala to access the data. Along with that, I would use visualization tools like Superset, Tableau, or PowerBI to visualize the data and create dashboards for data scientists.


#### Pandas example

Code: https://github.com/ninanguyen24/spurs_dataset/blob/main/PandasExample.py

- Output:
    1. This grab the timestamp and seconds of when the ball cross the half-court. The seconds is sorted from largest to smallest and when the ball x coordinate goes from >50 to <50 or <50 to >50, it means the ball crossed the half-court
    https://github.com/ninanguyen24/spurs_dataset/blob/main/half-court.json  
    <br>
    2. This group data by timestamp and sum up all the coordinates of the players
    https://github.com/ninanguyen24/spurs_dataset/blob/main/sum-location.json
    
     <br>
     
School Repo using pyspark: https://github.com/ninanguyen24/CPSC5330-Big-Data-Analytics/blob/main/Assignment2/TFIDFDataFrameFinal.ipynb
