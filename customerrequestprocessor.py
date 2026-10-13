from pyspark.sql import SparkSession


spark = SparkSession.builder \
    .appName("Customer Requests Processor") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
    .getOrCreate()

input_path = "s3a://x23328231-static/Pharma/customerrequests.csv"
df = spark.read.csv(input_path, header=True, inferSchema=True)


filtered_df = df.filter(df["status"] == "Pending")


output_path = "s3a://x23328231-static/Pharma/processed_data/"
filtered_df.write.csv(output_path, header=True)


spark.stop()
