import json
import os
import sys

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "../../../",
    )
)

from components.EnvironmentSecretsStore.src.models.PackageModel import (
    PackageModel,
)


schema = PackageModel.model_json_schema()

with open("data.json", "w", encoding="utf-8") as file:
    json.dump(schema, file, indent=2)