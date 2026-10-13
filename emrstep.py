import boto3


emr_client = boto3.client('emr', region_name='eu-west-1')


cluster_id = 'j-BZJHT5DD0MU5'


script_path = 's3://x23328231-static/Pharma/process_requests.py'


response = emr_client.add_job_flow_steps(
    JobFlowId=cluster_id,
    Steps=[
        {
            'Name': 'CustomerRequestProcessing',
            'ActionOnFailure': 'CONTINUE',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': [
                    'spark-submit',
                    script_path
                ]
            }
        }
    ]
)

print("Step submitted successfully.")
print("Step IDs:", response['StepIds'])
