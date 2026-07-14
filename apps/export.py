import os
import sys

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "../../../",
    )
)

from components.EnvironmentSecretsStore.src.models.PackageModel import (
    PackageModel as Package,
)


with open("data.json", "w", encoding="utf-8") as file:
    file.write(Package.schema_json(indent=2))