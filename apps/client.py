import os
import sys
import json
import requests

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "../../../",
    )
)

from components.EnvironmentSecretsStore.src.models.PackageModel import (
    VariablesStoringSecrets,
    PackageRequestConfigs,
    PackageRequest,
    EnvironmentSecretsStoreExecutor,
    ConfigExecutor,
    PackageConfigs,
    PackageModel,
)


ENDPOINT_URL = "http://127.0.0.1:8000/api"


def infer():
    variables = VariablesStoringSecrets(
        value=[
            "TEST_SECRET",
            "OPENAI_API_KEY",
        ]
    )

    request_configs = PackageRequestConfigs(
        variables_storing_secrets=variables
    )

    component_request = PackageRequest(
        configs=request_configs
    )

    component_executor = EnvironmentSecretsStoreExecutor(
        value=component_request
    )

    executor = ConfigExecutor(
        value=component_executor
    )

    package_configs = PackageConfigs(
        executor=executor
    )

    request = PackageModel(
        configs=package_configs,
        name="EnvironmentSecretsStore",
    )

    request_json = json.loads(request.json())

    response = requests.post(
        ENDPOINT_URL,
        json=request_json,
        timeout=30,
    )

    response.raise_for_status()

    print("Request completed successfully.")
    print(f"Status code: {response.status_code}")


if __name__ == "__main__":
    infer()