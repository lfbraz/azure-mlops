# Azure MLOps
This repository is used for MLOps using models created on Azure Databricks and Azure Machine Learning.

## azureml
In this folder we have the configs to be used in [Pipelines of Azure Devops](https://azure.microsoft.com/pt-br/services/devops/pipelines/). 

`aciDeploymentConfig.yml`: [Azure Container Instance](https://azure.microsoft.com/en-us/services/container-instances/) configs \
\
`aksDeploymentConfig.yml`: [Azure Kubernetes Services](https://docs.microsoft.com/en-us/azure/aks/) configs\
\
`conda_env_v_1_0_0.yml`: [Conda Environment](https://docs.microsoft.com/en-us/azure/devops/pipelines/ecosystems/anaconda?view=azure-devops&tabs=ubuntu-16-04) Environment config to be used in the inference cluster. All the libs and packages required must be consider here. Conda and PyPi can be used.\
\
`inferenceConfig.yml`: In this config we must indicate which environment must be used and other configs like the entry script that will coordinate the prediction task.\
\
`score.py`: The [entry script(scoring code)](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-and-where#script) that will coordinate the prediction task.\

This configurations can be added in Azure Devops to build a MLOps flow. I suggest to use Azure ML template (in the Azure Devops) to simplify the deployment task. Bellow I will show how to do it:

First of all, install [Azure ML Template](https://marketplace.visualstudio.com/items?itemName=ms-air-aiagility.vss-services-azureml&targetId=09d19ee8-b94a-4f99-a763-11cc0fe1a111&utm_source=vstsproduct&utm_medium=ExtHubManageList) in your Azure Devops organization:\

![Azure ML Template](images/azureml-template.PNG?raw=true)

Now you will have to set up a service connection. In the [Marketplace Home](https://marketplace.visualstudio.com/items?itemName=ms-air-aiagility.vss-services-azureml&targetId=09d19ee8-b94a-4f99-a763-11cc0fe1a111&utm_source=vstsproduct&utm_medium=ExtHubManageList)of the template you can see some instructions about how to complete this task.

With the service connection we are able to create a new Pipeline Release (in your Azure Devops project) to deploy the Azure ML models:

![New Release Pipeline](images/new-release-pipeline.PNG?raw=true)

In our case we have an Azure Devops project named as **MLOps-LAB**, please feel free to create the project of your choice.

Now we will add the model artifacts. We will use two sources: A repository source (can be Azure Devops Repos, Github, etc.) and an Azure ML Model Artifact (the model you have registered in your Azure ML Workspace):

![Artifacts](images/artifacts.PNG?raw=true)

The **repository source** will contain your deployment configs (`aciDeploymentConfig.yml` or `aksDeploymentConfig.yml`, `conda_env_v_1_0_0.yml`, `inferenceConfig.yml` and `score.py`).In this [folder](https://github.com/lfbraz/azure-mlops/tree/master/azureml/config) we have some examples of these files. In the **Azure ML Model Artifact** we will connect tha Azure Devops with our Azure ML Workspace using the `Service Connection`:

![AzureML Artifact](images/add-azureml-artifact.PNG?raw=true)
