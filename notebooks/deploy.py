# Databricks notebook source
import azureml
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.model import InferenceConfig
from azureml.core.environment import Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.webservice import AciWebservice, Webservice
from azureml.exceptions import WebserviceException
from azureml.core.model import Model

def get_workspace(workspace_location, workspace_name, resource_group, subscription_id):
  svc_pr = ServicePrincipalAuthentication(
      tenant_id = dbutils.secrets.get(scope = "azure-key-vault", key = "tenant-id"),
      service_principal_id = dbutils.secrets.get(scope = "azure-key-vault", key = "client-id"),
      service_principal_password = dbutils.secrets.get(scope = "azure-key-vault", key = "client-secret"))

  workspace = Workspace.create(name = workspace_name,
                               location = workspace_location,
                               resource_group = resource_group,
                               subscription_id = subscription_id,
                               auth=svc_pr,
                               exist_ok=True)
  
  print('Workspace: {} disponibilizada com sucesso'.format(workspace_name))
  return workspace

def get_config(entry_script):
  # Create the environment
  env = Environment(name="tensorflow_env")

  conda_dep = CondaDependencies()

  # Define the packages needed by the model and scripts
  conda_dep.add_conda_package("tensorflow")

  # You must list azureml-defaults as a pip dependency
  conda_dep.add_pip_package("azureml-defaults")
  conda_dep.add_pip_package("keras")
  conda_dep.add_pip_package("pandas")

  # Adds dependencies to PythonSection of myenv
  env.python.conda_dependencies=conda_dep

  inference_config = InferenceConfig(entry_script=entry_script,
                                     environment=env)
  
  print('Configuração do Endpoint retornada')
  return inference_config

def register_model(workspace, model_path, model_name, model_description, tags={}):
  model_azure = Model.register(model_path = model_path,
                               model_name = model_name,
                               description = model_description,
                               workspace = workspace,
                               tags = tags)
  
  print('Modelo: {} registrado com sucesso'.format(model_name))

  return model_azure

def deploy_container_instance(workspace, endpoint_name, inference_config, model_azure):
  # Remove any existing service under the same name.
  try:
      Webservice(workspace, endpoint_name).delete()
  except WebserviceException:
      pass

  deployment_config = AciWebservice.deploy_configuration(cpu_cores = 1, memory_gb = 1)
  service = Model.deploy(workspace, endpoint_name, [model_azure], inference_config, deployment_config)
  service.wait_for_deployment(show_output = True)
  print('A API {} foi gerada no estado {}'.format(service.scoring_uri, service.state))
  return service.scoring_uri

def deploy(workspace_location, workspace_name, resource_group, subscription_id, model_name, model_path, model_description='',tags={}):
  workspace = get_workspace(workspace_location, workspace_name, resource_group, subscription_id)
  inference_config = get_config('/dbfs/models/model-regressao-tensorflow/score.py')
  model_azure = register_model(workspace, model_path, model_name, model_description, tags)
  scoring_uri = deploy_container_instance(workspace, endpoint_name, inference_config, model_azure)

# COMMAND ----------

workspace_location = "Central US"
workspace_name = dbutils.secrets.get(scope = "azure-key-vault", key = "workspace-name")
resource_group = dbutils.secrets.get(scope = "azure-key-vault", key = "resource-group")
subscription_id = dbutils.secrets.get(scope = "azure-key-vault", key = "subscription-id")

model_name = 'model-regressao-tensorflow'
model_path = '/dbfs/models'
model_description = 'Modelo de regressão utilizando tensorflow (keras)'
endpoint_name = 'car-regression-service-dev'

tags={'Framework': "Tensorflow", 'Tipo': "Regressão"}

deploy(workspace_location, workspace_name, resource_group, subscription_id, model_name, model_path, model_description, tags)

# COMMAND ----------

print('TESTS 4')