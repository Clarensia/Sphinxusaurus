import os
import sys
from typing import List
from src.dataclasses.Attribute import Attribute
from src.dataclasses.ExceptionModel import ExceptionModel
from src.dataclasses.Model import Model

from src.dataclasses.Project import Project
from src.dataclasses.main_class.MainClass import MainClass
from src.dataclasses.main_class.MainClassMethod import MainClassMethod
from src.utils import create_folder_name


class Writer:

    def __init__(self, dest_path: str):
        self._dest_path = dest_path
        self._verify_folder()

    def _verify_folder(self):
        if os.path.exists(self._dest_path):
            print(f"Destination path: {self._dest_path} exists, can't run the program")
            sys.exit(1)

    def _create_folder_in_dest(self, folder: str):
        os.mkdir(os.path.join(self._dest_path, folder))

    def _create_dest_folder(self):
        os.mkdir(self._dest_path)
        self._create_folder_in_dest("models")
        self._create_folder_in_dest("exceptions")

    def _get_metadata(self, title: str, description: str, sidebar_position: int, sidebar_class_name: str | None = None) -> str:
        """Create the metadata header for the given file

        :param title: The title of the file
        :type title: str
        :param description: The short description
        :type description: str
        :param sidebar_position: The index inside of the tab list, this way we keep the index
        :type sidebar_position: int
        :param sidebar_class_name: If we are in a description of th main file, we put the
                                   class name here. If not, then we create a normal header
        :type sidebar_class_name: str | None
        :return: The metadata that we wrote
        :rtype: str
        """
        ret = "---\n"
        ret += f"title: {title}\n"
        ret += f"description: {description}\n"
        ret += f"sidebar_position: {sidebar_position}\n"
        if sidebar_class_name is not None:
            ret += f"sidebar_class_name: {sidebar_class_name}\n"
        ret += "---\n"
        
        return ret

    def _create_module_main_file(self, folder_name: str, class_name: str, short_description: str, folder_sidebar_position: int, long_description: str):
        to_write = self._get_metadata(class_name, short_description, folder_sidebar_position, f"sidebar-{folder_name}")
        to_write += "\n"

        to_write += long_description

        with open(os.path.join(self._dest_path, folder_name, f"{folder_name}.md"), "w+") as f:
            f.write(to_write)

    def _get_usage(self, method: MainClassMethod, main_class_name: str) -> str:
        """Get the usage of a method. Example return value:

        ```py
        import asyncio

        from blockchainapis import BlockchainAPIs

        async def print_amount_out():
            # Create the BlockchainAPIs instance
            # You can additionaly add an API key if needed
            blockchain_apis = BlockchainAPIs()
            # Get the amount of tokenOut that you will get after selling amountIn tokenIn
            amount_out = await blockchain_apis.amount_out(
                blockchain="ethereum", # The id of the blockchain on which this exchange take place
                tokenIn="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", # The address of the token that you sell
                tokenOut="0xdAC17F958D2ee523a2206206994597C13D831ec7", # The address of the token that you buy
                amountIn=1000000000000000000, # The amount of token0 that you sell
                exchange="uniswapv2" # The exchange on which you want to do the trade (optional)
            )
            print(amount_out)
            # We need to close our instance once we are done with BlockchainAPIs
            await blockchain_apis.close()

        asyncio.run(print_amount_out())
        ```

        :param method: The method that we have to use
        :type method: MainClassMethod
        :return: The usage string
        :rtype: str
        """
        instance_name = create_folder_name(main_class_name).replace("-", "_")
        ret = f'''```py
import asyncio

from {main_class_name} import {main_class_name}

async def print_{method.name}():
    # Create the {main_class_name} instance
    # You can additionaly add an API key if you want
    {instance_name} = {main_class_name}()
    # {method.short_description}
    {method.name} = await {instance_name}.{method.name}('''
        if len(method.parameters) > 0:
            ret += "\n"
            for param in method.parameters:
                example = f'"{param.example}"' if param.param_type == "str" else param.example
                ret += f"        {param.name}={example}\n"

            ret += f'    )\n'
        else:
            ret += ")\n"
        ret += f'''    print({method.name})
    # We need to close our instance once we are done with BlockchainAPIs
    await {main_class_name}.close()

asyncio.run(print_{method.name}())
```
'''

        return ret

    def _write_object(self, object_to_write: str) -> str:
        to_write = '<CodeBlock language="python">\n'
        if "List" in object_to_write:
            list_object = object_to_write.replace("List[", "")
            list_object = list_object.replace("]", "")
            link_to_return_type = f'<a href="/docs/python-sdk/models/{list_object}">{list_object}</a>'
            to_write += f'    List[{link_to_return_type}]\n'
        else:
            to_write += f'    <a href="/docs/python-sdk/models/{object_to_write}">{object_to_write}</a>'
            to_write += "\n"
        
        to_write += '</CodeBlock>\n\n'
        return to_write

    def _write_method(self, folder_name: str, method: MainClassMethod, main_class_name: str, sidebar_position: int):
        to_write = self._get_metadata(method.name, method.short_description, sidebar_position)
        to_write += "\n"
        to_write += "import CodeBlock from '@theme/CodeBlock';\n\n"
        to_write += "```py\n"
        to_write += method.definition
        to_write += "\n```\n"
        to_write += method.long_description
        if len(method.parameters) > 0:
            to_write += "\n\n## Parameters\n\n"
            for parameter in method.parameters:
                to_write += f" - [{parameter.name}](#{parameter.name}): {parameter.description}\n"
        if method.return_type is not None:
            to_write += "\n## Returns\n\n"
            to_write += self._write_object(method.return_type)
            to_write += method.return_description
        else:
            to_write += "\n"

        if method.example_response is not None:
            to_write += "## Example\n\n"
            to_write += "### Usage\n\n"
            to_write += self._get_usage(method, main_class_name)
            to_write += "\n"
            to_write += "### Example response\n\n"
            to_write += method.example_response
            if len(method.exceptions) > 0:
                to_write += "\n## Exceptions\n\n"
                for exception in method.exceptions:
                    to_write += f'- [{exception.exception}](/docs/python-sdk/exceptions/{exception.exception}): {exception.description}\n'
        if len(method.parameters) > 0:
            to_write += "\n## Parameters detailed"
            to_write += "\n"
            for parameter in method.parameters:
                to_write += f"### {parameter.name}\n\n"
                to_write += parameter.description
                to_write += "\n"
                to_write += f'- type: `{parameter.param_type}`\n'
                to_write += f'- example: `{parameter.example}`\n'
                to_write += "\n"

        if method.name == "__init__":
            filename = "init"
        else:
            filename = method.name.replace('_', '-')
        with open(os.path.join(self._dest_path, folder_name, f"{filename}.mdx"), "w+") as f:
            f.write(to_write)

    def _write_main_class(self, main_class: MainClass, folder_sidebar_position: int):
        folder_name = create_folder_name(main_class.name)
        self._create_folder_in_dest(folder_name)
        self._create_module_main_file(folder_name,
                                      main_class.name,
                                      main_class.short_description,
                                      folder_sidebar_position,
                                      main_class.long_description)
        sidebar_position = 1
        for method in main_class.methods:
            self._write_method(folder_name, method, main_class.name, sidebar_position)
            sidebar_position += 1

    def _add_attributes(self, attributes: List[Attribute]) -> str:
        ret = ""
        for attribute in attributes:
            ret += f"### {attribute.name}\n\n"
            ret += attribute.attribute_description
            ret += "\n"
            if "List" in attribute.attribute_type:
                ret += "#### Type\n\n"
                ret += self._write_object(attribute.attribute_type)
                ret += "\n"
                ret += "#### Example\n\n"
                ret += "```json"
                ret += attribute.example
                ret += "```\n\n"
            else:
                ret += f'- type: `{attribute.attribute_type}`\n'
                ret += f'- example: `{attribute.example}`\n\n'

        return ret

    def _write_model(self, model: Model, sidebar_index: int):
        file_name = create_folder_name(model.name)
        to_write = self._get_metadata(model.name, model.short_description, sidebar_index)
        to_write += "\n"
        to_write += "import CodeBlock from '@theme/CodeBlock';\n\n"
        to_write += "```py\n"
        to_write += "@dataclass(slots=True, frozen=True)\n"
        to_write += model.class_definition
        to_write += "\n"
        for attribute in model.attributes:
            to_write += f"    {attribute.name}: {attribute.attribute_type}\n"
        to_write += "```\n\n"
        to_write += model.long_description
        to_write += "\n## Attributes\n\n"
        to_write += self._add_attributes(model.attributes)

        with open(os.path.join(self._dest_path, "models", file_name + ".mdx"), "w+") as f:
            f.write(to_write)

    def _write_exception(self, exception: ExceptionModel, sidebar_index: int):
        file_name = create_folder_name(exception.name)
        to_write = self._get_metadata(exception.name, exception.short_description, sidebar_index)
        to_write += "\n"
        to_write += "```py\n"
        to_write += exception.definition
        to_write += "\n```\n\n"
        to_write += exception.long_description
        to_write += "\n\n"
        to_write += "## Params\n\n"
        to_write += self._add_attributes(exception.attributes)

        with open(os.path.join(self._dest_path, "exceptions", file_name + ".md"), "w+") as f:
            f.write(to_write)

    def write(self, project: Project):
        self._create_dest_folder()
        folder_sidebar_position = 1
        for main_class in project.main_classes:
            self._write_main_class(main_class, folder_sidebar_position)
            folder_sidebar_position += 1

        model_sidebar_index = 1
        for model in project.models:
            self._write_model(model, model_sidebar_index)
            model_sidebar_index += 1

        exception_sidebar_index = 1
        for exception in project.exceptions:
            curr_index = exception_sidebar_index
            # I want a special position for Unauthorized and TooManyRequest because
            # these exceptions are not related to the other
            if exception.name == "UnauthorizedException":
                curr_index = len(project.exceptions) - 1
            elif exception.name == "TooManyRequestsException":
                curr_index = len(project.exceptions) - 2
            else:
                exception_sidebar_index += 1
            self._write_exception(exception, curr_index)
