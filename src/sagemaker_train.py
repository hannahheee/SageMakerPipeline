from numpy import true_divide
import sagemaker
import boto3
import time

from sagemaker.analytics import TrainingJobAnalytics
from sagemaker.estimator import Estimator
import slack
from smexperiments.experiment import Experiment
from smexperiments.trial import Trial
from smexperiments.trial_component import TrialComponent
from smexperiments.tracker import Tracker

from time import strftime

from report import ResultReport
from slack_notify import SlackBot


sagemaker_session = sagemaker.Session(boto3.session.Session())

# Put the right role and input data
role = "arn:aws:iam::576788201127:role/github-workflow-action"

# Make sure the metric_definition and its regex
metric_definitions=[
                       {'Name':'Finish_running_top1_suggestion','Regex':'Finish_running_top1_suggestion=(.*?);'}
                   ]



create_date = strftime("%Y-%m-%d-%H-%M-%S")
    

experiment = Experiment.create(experiment_name = "EXPERIMENT-{}".format(create_date),
                               description = "Demo experiment",
                               tags = [{'Key': 'experiments', 'Value': 'Experiments'}])
    
    
trial = Trial.create(trial_name = "TRAIL-{}".format(create_date),
                     experiment_name = experiment.experiment_name,
                     tags = [{'Key': 'demo-trials', 'Value': 'demoTrail'}])



estimator = Estimator(image_uri='576788201127.dkr.ecr.us-west-1.amazonaws.com/demo:latest',
                     role=role,
                     instance_count=1,
                     instance_type="ml.m5.xlarge",
                     output_path = f"s3://demopipelineworkflow/",
                     enable_sagemaker_metrics=True,
                     metric_definitions=metric_definitions)

estimator.fit(experiment_config = {
                "ExperimentName": experiment.experiment_name,
                "TrialName" : trial.trial_name,
                "TrialComponentDisplayName" : "PipelineTrainingJob",
            }, job_name="PipelineTrainingJob-{}".format(create_date))

training_job_name = estimator.latest_training_job.name
    
# Get metric values
metric_names = [ metric['Name'] for metric in estimator.metric_definitions ] 
metrics_dataframe = TrainingJobAnalytics(training_job_name=training_job_name, metric_names=metric_names).dataframe()

# Report results
rr = ResultReport()
rr.report(estimator.model_data, metrics_dataframe)



slack_bot = SlackBot()
slack_bot.success_send("Model Data:" + estimator.model_data)
slack_bot.success_send("## Results\n" + metrics_dataframe.to_markdown())