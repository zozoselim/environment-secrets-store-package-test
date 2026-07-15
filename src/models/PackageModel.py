import re
from typing import List, Optional, Union, Literal

from pydantic import Field, validator

from sdks.novavision.src.base.model import (
    Package,
    Inputs,
    Configs,
    Outputs,
    Response,
    Request,
    Output,
    Config,
)


class EmptyInputs(Inputs):
    """Environment Secrets Store does not require workflow input."""

    pass


class VariablesStoringSecrets(Config):
    """
    Environment variable names containing secret values.

    Example:
    ["OPENAI_API_KEY", "DATABASE_PASSWORD"]
    """

    name: Literal["variables_storing_secrets"] = "variables_storing_secrets"
    value: List[str] = Field(min_length=1)
    type: Literal["list"] = "list"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal[
        '["OPENAI_API_KEY", "DATABASE_PASSWORD"]'
    ] = '["OPENAI_API_KEY", "DATABASE_PASSWORD"]'

    @validator("value")
    def validate_variable_names(cls, variable_names):
        cleaned_names = []
        generated_output_names = set()

        for variable_name in variable_names:
            if not isinstance(variable_name, str):
                raise ValueError(
                    "Environment variable names must be strings."
                )

            variable_name = variable_name.strip()

            if not variable_name:
                raise ValueError(
                    "Environment variable names cannot be empty."
                )

            if not re.fullmatch(
                r"[A-Za-z_][A-Za-z0-9_]*",
                variable_name,
            ):
                raise ValueError(
                    f"Invalid environment variable name: {variable_name}"
                )

            output_name = variable_name.lower()

            if output_name in generated_output_names:
                raise ValueError(
                    "Environment variable names must generate unique "
                    f"output names. Conflicting output: {output_name}"
                )

            generated_output_names.add(output_name)
            cleaned_names.append(variable_name)

        return cleaned_names

    class Config:
        title = "Variables Storing Secrets"


class SecretOutput(Output):
    """
    Represents one secret retrieved from an environment variable.

    The executor will create one SecretOutput for each requested variable.
    """

    name: str
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Secret"


class PackageRequestConfigs(Configs):
    variables_storing_secrets: VariablesStoringSecrets


class PackageOutputs(Outputs):
    """
    Allows outputs to be created dynamically.

    Example dynamic output names:
    - openai_api_key
    - database_password
    """

    diagnostic_secret: SecretOutput

    class Config:
        extra = "allow"


class PackageRequest(Request):
    inputs: Optional[EmptyInputs] = None
    configs: PackageRequestConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class PackageResponse(Response):
    outputs: PackageOutputs


class EnvironmentSecretsStoreExecutor(Config):
    name: Literal[
        "EnvironmentSecretsStore"
    ] = "EnvironmentSecretsStore"

    value: Union[
        PackageRequest,
        PackageResponse,
    ]

    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Environment Secrets Store"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[EnvironmentSecretsStoreExecutor]
    type: Literal["executor"] = "executor"
    field: Literal[
        "dependentDropdownlist"
    ] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal[
        "EnvironmentSecretsStore"
    ] = "EnvironmentSecretsStore"
