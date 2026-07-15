"""Response builder for the Environment Secrets Store component."""

from typing import Dict

from sdks.novavision.src.helper.package import PackageHelper

from components.EnvironmentSecretsStore.src.models.PackageModel import (
    ConfigExecutor,
    EnvironmentSecretsStoreExecutor,
    PackageConfigs,
    PackageModel,
    PackageOutputs,
    PackageResponse,
    SecretsOutput,
)


def build_response(
    context,
    secrets: Dict[str, str],
):
    """Build a response containing one static ``secrets`` output."""

    outputs = PackageOutputs(
        secrets=SecretsOutput(
            value=secrets,
        )
    )

    package_response = PackageResponse(outputs=outputs)

    component_executor = EnvironmentSecretsStoreExecutor(
        value=package_response
    )

    executor = ConfigExecutor(
        value=component_executor
    )

    package_configs = PackageConfigs(
        executor=executor
    )

    package_helper = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs,
    )

    return package_helper.build_model(context)
