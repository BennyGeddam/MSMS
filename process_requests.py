from pyspark.sql import SparkSession
#1.  This PySpark script processes customer request data stored in an S3 bucket:
# 2. Reads customer request data from a specified S3 bucket (CSV format) into a Spark DataFrame.
# 3. Filters the data to include only rows where the "status" column has the value "Pending."
# 4. Writes the filtered results back to a designated S3 bucket location in CSV format.
# 5. Overwrites any existing data in the output path, ensuring clean and updated results.
spark = SparkSession.builder \
    .appName("Customer Requests Processor") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
    .getOrCreate()

input_path = "s3a://x23328231-static/Pharma/customerrequests.csv"
df = spark.read.csv(input_path, header=True, inferSchema=True)


filtered_df = df.filter(df["status"] == "Pending")


output_path = "s3a://x23328231-static/Pharma/processed_data/"
filtered_df.write.mode("overwrite").csv(output_path, header=True)

spark.stop()
