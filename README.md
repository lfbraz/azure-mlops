# Azure MLOps
This repository is used for MLOps using models created on Azure Databricks and Azure Machine Learning.


## azureml
In this folder we have the configs to be used in Pipelines of Azure Devops. 

`aciDeploymentConfig.yml`: [Azure Container Instance](https://azure.microsoft.com/en-us/services/container-instances/) configs\
`aksDeploymentConfig.yml`: [Azure Kubernetes Services](https://docs.microsoft.com/en-us/azure/aks/) configs\
`conda_env_v_1_0_0.yml`: [Conda Environment](https://docs.microsoft.com/en-us/azure/devops/pipelines/ecosystems/anaconda?view=azure-devops&tabs=ubuntu-16-04) Environment config to be used in the inference cluster. All the libs and packages required must be consider here. Conda and PyPi can be used.\
`inferenceConfig.yml`: In this config we must indicate which environment must be used and other configs like the entry script that will coordinate the prediction task.\
`score.py`: The [entry script(scoring code)](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-and-where#script) that will coordinate the prediction task.\

