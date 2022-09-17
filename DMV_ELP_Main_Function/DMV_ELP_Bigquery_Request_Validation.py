from google.cloud import bigquery
import pandas as pd
import datetime
# Bigquery insert function needs to be implemented



def GetCurrentDateRequestCount():
    vAR_client = bigquery.Client()
    vAR_query_job = vAR_client.query(
        """
       SELECT count(1) as cnt FROM `elp-2022-352222.DMV_ELP.DMV_ELP_REQUEST`
where date(created_dt) = current_date()
"""
    )

    vAR_results = vAR_query_job.result()  # Waits for job to complete.
    print('Current Date Request Count - ',vAR_results)
    for row in vAR_results:
        vAR_request_count = row.get('cnt')
    return vAR_request_count

def ReadNotProcessedRequestData():
    vAR_client = bigquery.Client()
    vAR_sql =(
        """
       select * from `elp-2022-352222.DMV_ELP.DMV_ELP_REQUEST` where CONFIGURATION not in
(select CONFIGURATION from `elp-2022-352222.DMV_ELP.DMV_ELP_MLOPS_RESPONSE_COPY` where date(created_dt) = current_date())
        """
    )

    vAR_df = vAR_client.query(vAR_sql).to_dataframe()
    return vAR_df


def InsertRequesResponseMetaData(vAR_number_of_configuration):
   vAR_df = pd.DataFrame()
   vAR_rownum = 1
   if GetMetadatarownum() is not None:
      if GetMetadatarownum()>0:
         vAR_df['ROWNUM'] = 1*[vAR_rownum+1]
   else:
      vAR_df['ROWNUM'] = 1*[vAR_rownum]
   vAR_df['TOTAL_NUMBER_OF_ORDERS'] = 1*[vAR_number_of_configuration]
   vAR_df['CREATED_DT'] = 1*[datetime.datetime.utcnow()]
   vAR_df['CREATED_USER'] = 1*['AWS_LAMBDA_USER']
   client = bigquery.Client(project='elp-2022-352222')

   # Define table name, in format dataset.table_name
   table = 'DMV_ELP.DMV_ELP_REQUEST_RESPONSE_METADATA'
   job_config = bigquery.LoadJobConfig(autodetect=True,write_disposition="WRITE_APPEND",)
   job = client.load_table_from_dataframe(vAR_df, table,job_config=job_config)

   job.result()  # Wait for the job to complete.
   table_id = 'elp-2022-352222.DMV_ELP.DMV_ELP_REQUEST_RESPONSE_METADATA'
   table = client.get_table(table_id)  # Make an API request.
   print(
         "Loaded {} rows and {} columns to {}".format(
               table.num_rows, len(table.schema), table_id
         )
      )
   

def GetMetadatarownum():
    vAR_client = bigquery.Client()
    vAR_query_job = vAR_client.query(
        """
       SELECT max(ROWNUM) as rownumber FROM `elp-2022-352222.DMV_ELP.DMV_ELP_REQUEST_RESPONSE_METADATA` """
    )

    vAR_results = vAR_query_job.result()  # Waits for job to complete.
    print('Current Date Request Count - ',vAR_results)
    for row in vAR_results:
        vAR_request_count = row.get('rownumber')
    return vAR_request_count


