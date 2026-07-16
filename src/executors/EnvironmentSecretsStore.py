"""Runtime executor for the Environment Secrets Store component."""

import os
import sys
from typing import Dict, List

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../",
    )
)

from sdks.novavision.src.base.component import Component

from components.EnvironmentSecretsStore.src.models.PackageModel import (
    PackageModel,
)
from components.EnvironmentSecretsStore.src.utils.response import (
    build_response,
)


class EnvironmentSecretsStore(Component):
    """Reads configured secrets from environment variables."""

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)

        self.request.model = PackageModel(**self.request.data)

        variable_names = self.request.get_param(
            "variables_storing_secrets"
        )

        self.variable_names: List[str] = list(
            variable_names or []
        )

    @staticmethod
    def bootstrap(config: dict) -> dict:
        """No model or external resource needs to be loaded."""

        return {}

    def read_secrets(self) -> Dict[str, str]:
        """Read secrets without logging their values."""

        if not self.variable_names:
            raise ValueError(
                "At least one environment variable name is required."
            )

        secrets: Dict[str, str] = {}

        for variable_name in self.variable_names:
            secret_value = os.getenv(variable_name)

            if secret_value is None:
                raise RuntimeError(
                    "Required environment variable was not found: "
                    f"{variable_name}"
                )

            secrets[variable_name] = secret_value

        return secrets

    def run(self):
        """Read secrets and build the NovaVision response."""

        secrets = self.read_secrets()

        return build_response(
            context=self,
            secrets=secrets,
        )


if __name__ == "__main__":
    from sdks.novavision.src.helper.executor import Executor

    if len(sys.argv) < 2:
        raise RuntimeError(
            "Executor request argument is required."
        )

    Executor(sys.argv[1]).run()
