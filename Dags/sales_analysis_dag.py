from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import month, year, sum, avg, lit, lag
from pyspark.sql.window import Window

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 5, 14),
    'retries': 1,
}

dag = DAG('sales_analysis_dag32',
          default_args=default_args,
          description='A simple DAG to run Spark job and load data into SQL table',
          schedule_interval=None)

def run_spark_job():
    spark = SparkSession.builder \
        .appName("Monthly Sales Analysis") \
        .config("spark.driver.extraClassPath", "/home/user1/Desktop/airflow/dags/mysql-connector-java-8.0.28.jar") \
        .config("spark.executor.extraClassPath", "/home/user1/Desktop/airflow/dags/mysql-connector-java-8.0.28.jar") \
        .getOrCreate()

    transactions = spark.read.csv("file:///home/user1/Desktop/airflow/transaction_data.csv", header=True, inferSchema=True)

    transactions = transactions.withColumn("year", year(transactions.Date))
    transactions = transactions.withColumn("month", month(transactions.Date))

    monthly_sales = transactions.groupBy("year", "month").agg(
        sum("Amount").alias("total_sales"),
        sum(lit(1)).alias("total_products_sold")
    )

    average_sales = transactions.groupBy("year", "month").agg(
        avg("Amount").alias("average_sales")
    )

    windowSpec = Window.orderBy("year", "month")
    monthly_sales = monthly_sales.withColumn("prev_month_sales", lag("total_sales").over(windowSpec))

    monthly_sales = monthly_sales.withColumn("sales_diff_prev_month", monthly_sales["total_sales"] - monthly_sales["prev_month_sales"])

    # Write the DataFrame directly to MySQL table
    monthly_sales.write \
        .format("jdbc") \
        .option("url", "jdbc:mysql://localhost:3306/airflow_db") \
        .option("driver", "com.mysql.jdbc.Driver") \
        .option("dbtable", "transaction_data") \
        .option("user", "airflow_user_new") \
        .option("password", "airflow_pass_new") \
        .mode("overwrite") \
        .save()

    spark.stop()

run_spark_job_task = PythonOperator(
    task_id='run_spark_job',
    python_callable=run_spark_job,
    dag=dag,
)

run_spark_job_task
