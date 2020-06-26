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
\

![Azure ML Template][images/azureml-template.PNG]



