# Azure MLOps
This repository is used to demonstrate how to configure Azure Devops to create a MLOps flow using models created on Azure Machine Learning.

## Azure MLOps using [Azure Devops](https://dev.azure.com/) and [Azure Machine Learning](https://azure.microsoft.com/pt-br/services/machine-learning/)

First of all, install [Azure ML Template](https://marketplace.visualstudio.com/items?itemName=ms-air-aiagility.vss-services-azureml&targetId=09d19ee8-b94a-4f99-a763-11cc0fe1a111&utm_source=vstsproduct&utm_medium=ExtHubManageList) in your Azure Devops organization:  

![Azure ML Template](images/azureml-template.PNG?raw=true)

Now you will have to set up a service connection. In the [Marketplace Template Home](https://marketplace.visualstudio.com/items?itemName=ms-air-aiagility.vss-services-azureml&targetId=09d19ee8-b94a-4f99-a763-11cc0fe1a111&utm_source=vstsproduct&utm_medium=ExtHubManageList) you can see some instructions about how to complete this task.

With the service connection we are able to create a new Pipeline Release (in your Azure Devops project) to deploy the Azure ML models:

![New Release Pipeline](images/new-release-pipeline.PNG?raw=true)

In our case we have an Azure Devops project named as **MLOps-LAB**, please feel free to create the project of your choice.

Now we will add the model artifacts. We will use two sources: A repository source (can be Azure Devops Repos, Github, etc.) and an Azure ML Model Artifact (the model you have registered in your Azure ML Workspace):

![Artifacts](images/artifacts.PNG?raw=true)

The **Repository source** will contain your deployment configs (`aciDeploymentConfig.yml` or `aksDeploymentConfig.yml`, `conda_env_v_1_0_0.yml`, `inferenceConfig.yml` and `score.py`).In this [folder](https://github.com/lfbraz/azure-mlops/tree/master/azureml/config) we have some examples of these files.  

In the **Azure ML Model Artifact** we will connect the Azure Devops with our Azure ML Workspace using the `Service Connection`:

![AzureML Artifact](images/add-azureml-artifact.jpg?raw=true)

Now with the artifacts configured we can add the stages of this Release Pipeline. In this example we will create two stages: **QA** (pre-production stage) and **Production**:

![Stages](images/stages.PNG?raw=true)

In each stage we will configure an **Azure ML Model Deploy Task** using the `aciDeploymentConfig.yml` (for QA) or `aksDeploymentConfig.yml` (for production) config, and the `inferenceConfig.yml` file as well:

![Deploy Config](images/azureml-deploy-task.PNG?raw=true)

Finally, we can add a Pre-deployment condition to be able to request an approval before deploying to **Production** stage. It is useful to validade the **QA** endpoint before put it on **Production**.

Click on ![Add Pre-Deployment condition](images/add-pre-deployment-condition.PNG?raw=true) to open the options and define one (or many) approvers:

![Pre-Deployment condition config](images/pre-deployment-condition-config.PNG?raw=true)

All set up 😃. Now we can create a manual **Release**:

![Create Release](images/create-release.PNG?raw=true)

We can use a **Continuous deployment trigger** as well to create a new release every time a new AzureML model is registered:

![Continuous deployment trigger](images/continuous-deployment.PNG?raw=true)