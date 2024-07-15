<div align="center">

# Serverless Azure OpenAI Quick Start with LlamaIndex <br> (Python)

[![Open project in GitHub Codespaces](https://img.shields.io/badge/Codespaces-Open-blue?style=flat-square&logo=github)](https://codespaces.new/Azure-Samples/llama-index-python?hide_repo_select=true&ref=main&quickstart=true)
[![License](https://img.shields.io/badge/License-MIT-pink?style=flat-square)](LICENSE)

This sample shows how to quickly get started with [LlamaIndex.ai](https://www.llamaindex.ai/) on Azure. The application is hosted on [Azure Container Apps](https://learn.microsoft.com/azure/container-apps/). You can use it as a starting point for building more complex RAG applications.

(Like and fork this sample to receive lastest changes and updates)

[![Features](https://img.shields.io/badge/🚀%20Features-blue?style=flat-square)](#features)
[![Architecture Diagram](https://img.shields.io/badge/🏗️%20Architecture%20Diagram-blue?style=flat-square)](#architecture-diagram)
[![Getting Started](https://img.shields.io/badge/🚦%20Getting%20Started-blue?style=flat-square)](#getting-started)
[![Guidance](https://img.shields.io/badge/📚%20Guidance-blue?style=flat-square)](#guidance)
[![Resources](https://img.shields.io/badge/📚%20Resources-blue?style=flat-square)](#resources)
[![Troubleshooting](https://img.shields.io/badge/🛠️%20Troubleshooting-blue?style=flat-square)](#troubleshooting)
[![Contributing](https://img.shields.io/badge/🤝%20Contributing-blue?style=flat-square)](#contributing)
[![Trademarks](https://img.shields.io/badge/™%20Trademarks-blue?style=flat-square)](#trademarks)
[![License](https://img.shields.io/badge/📜%20License-blue?style=flat-square)](LICENSE)
[![Give us a star](https://img.shields.io/badge/⭐%20Give%20us%20a%20star-blue?style=flat-square)](https://github.com/Azure-Samples/llama-index-python/stargazers)

  <img src="./docs/llama-index-python.png" alt="Screenshot showing the LlamaIndex app in action" width="640px" />

</div>

## Features

This project demonstrates how to build a simple LlamaIndex application using Azure OpenAI. The app is set up as a chat interface that can answer questions about your data. You can add arbitrary data sources to your chat, like local files, websites, or data retrieved from a database. The app will ingest any supported files you put in `./data/` directory. This sample app includes an example pdf in the data folder that contains information about standards for sending letters, cards, flats, and parcels in the mail. The app also uses LlamaIndex.TS that is able to ingest any PDF, text, CSV, Markdown, Word and HTML files. 

## Architecture Diagram

<div align="center">
  <img src="./docs/architecture-diagram-llama-index-python.png" alt="Screenshot showing the chatgpt app high level diagram" width="640px" />
</div>

- This application has two main components:

  1. A Python backend built using FastAPI 
  2. A Javascript frontend built with Next.js 

  It is hosted on [Azure Container Apps](https://learn.microsoft.com/azure/container-apps/) in just a few commands. 

- The app uses [Azure OpenAI](https://learn.microsoft.com/azure/ai-services/openai/overview) to answer questions about the data you provide. The app is set up to use the `gpt-35-turbo` model and embeddings to provide the best and fastest answers to your questions.

## Getting Started

You have a few options for getting started with this template. The quickest way to get started is [GitHub Codespaces](#github-codespaces), since it will setup all the tools for you, but you can also [set it up locally](#local-environment). You can also use a [VS Code dev container](#vs-code-dev-containers)

This template uses `gpt-35-turbo` version `1106`  which may not be available in all Azure regions. Check for [up-to-date region availability](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#standard-deployment-model-availability) and select a region during deployment accordingly. We recommend using `swedencentral`.

### GitHub Codespaces

You can run this template virtually by using GitHub Codespaces. The button will open a web-based VS Code instance in your browser:

1. Open the template (this may take several minutes)
    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Azure-Samples/llama-index-python?hide_repo_select=true&ref&quickstart=true)
2. Open a terminal window
3. Sign into your Azure account:

    ```shell
     azd auth login
    ```
4. Provision the Azure resources and deploy your code:

    ```shell
     azd up
    ```
   
    Once your deployment is complete you can begin to set up your python environment. 
    
5. Create a python virtual environment and install the python dependencies:

    ```bash
     cd backend 
     python3 -m venv venv
     source venv/bin/activate
     poetry install
    ```

    You will also need to ensure the environment variables are accessible. You can do this by running the following command: 
    
    ```bash
    azd env get-values > .env
    ```
    Confirm that this step has happened successfuly by checking if a `.env` file has been added to the `backend` folder. 

6. We can now generate the embeddings of the documents in the `./data` directory. In this sample it contains a pdf file with mail standards. 

    ```bash
    poetry run generate
    ```

7. Next, we can install the frontend dependencies:

    ```bash
     cd ../frontend
     npm install
    ```


✅ The app is now ready to run! To test it, run the following commands:

1. First start the Flask server
  ```bash
  cd ../backend
  python main.py
  ```
  (If you see a Traceloop error ignore it as we will not be using it for this example.)

> [!IMPORTANT] 
>  Because the Flask server and the frontend web app server are running on different ports, **you will need to
use public ports in codespaces.** To do this look for the `ports` tab at the top of your terminal in vscode. If the port
> visibilities of the available ports are already public skip this step. If they are private look for port 8000, 
right click on it, select Port Visibility and set it to public. Do the same for port 3000.

<img src="./docs/port-visibility.png" alt="Screenshot showing setting port-visibility" width="800px" />

2. Next open a **new terminal** and launch the web app

  ```bash
  cd frontend
  npm run dev
  ```

Open the URL `http://localhost:3000` in your browser to interact with the bot.

Congratulations! Your RAG app is now working. An example question to ask is 'Can you tell me how much it costs to send a large parcel to France?'

### VS Code Dev Containers

A related option is VS Code Dev Containers, which will open the project in your local VS Code using the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers):

1. Start Docker Desktop (install it if not already installed)
2. Open the project:
    [![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/llama-index-python)
3. In the VS Code window that opens, once the project files show up (this may take several minutes), open a terminal window.
4. Sign into your Azure account:

    ```shell
     azd auth login
    ```
5. Provision the Azure resources and deploy your code:

    ```shell
     azd up
    ```

  Once your deployment is complete, you should see a `.env` file in the `.azure\env_name` folder. This file contains the environment variables needed to run the   application using Azure resources. Move this file to the `backend\app` folder for the variables to be loaded into the correct enivornment. 
    
6. Create a python virtual environment and install the python dependencies:

    ```bash
     cd backend 
     python3 -m venv venv
     source venv/bin/activate
     poetry install
    ```

    You will also need to ensure the environment variables are accessible. You can do this by running the following command: 
    
    ```bash
    azd env get-values > .env
    ```
    Confirm that this step has happened successfuly by checking if a `.env` file has been added to the `backend` folder. 

7. We can now generate the embeddings of the documents in the `./data` directory. In this sample it contains a pdf file with mail standards. 
  
    ```bash
    poetry run generate
    ```

8. Install the frontend dependencies:

    ```bash
     cd ..
     cd frontend 
     npm install
    ```
9. Configure a CI/CD pipeline:

    ```shell
    azd pipeline config
    ```

The app is now ready to run! To test it, run the following commands:

1. First run the Flask development server
```bash
cd ../backend
python main.py
```

2. Next open a **new terminal** and launch the web app

```bash
cd frontend
npm run dev
```

Open the URL `http://localhost:3000` in your browser to interact with the bot.
An example question to ask is 'Can you tell me how much it costs to send a large parcel to France?'


### Local Environment

#### Prerequisites

You need to install following tools to work on your local machine:

- [Python 3.9, 3.10, or 3.11](https://www.python.org/downloads/)
- [Poetry](https://pypi.org/project/poetry/)
- [Node.js LTS](https://nodejs.org/download/)
- [Azure Developer CLI](https://aka.ms/azure-dev/install)
- [Git](https://git-scm.com/downloads)
- [PowerShell 7+](https://github.com/powershell/powershell) _(for Windows users only)_
  - **Important**: Ensure you can run `pwsh.exe` from a PowerShell command. If this fails, you likely need to upgrade PowerShell.
  - Instead of Powershell, you can also use Git Bash or WSL to run the Azure Developer CLI commands.
- This template uses `gpt-35-turbo` version `1106` which may not be available in all Azure regions. Check for [up-to-date region availability](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#standard-deployment-model-availability) and select a region during deployment accordingly
  * We recommend using `swedencentral`

Then you can get the project code:

1. [**Fork**](https://github.com/Azure-Samples/llama-index-python/fork) the project to create your own copy of this repository.
2. On your forked repository, select the **Code** button, then the **Local** tab, and copy the URL of your forked repository.
3. Open a terminal and run this command to clone the repo: <code> git clone &lt;your-repo-url&gt; </code>

#### Using the template locally

1. Bring down the template code:

    ```shell
    azd init --template llama-index-python
    ```

    This will perform a git clone

2. Sign into your Azure account:

    ```shell
     azd auth login
    ```

3. Create a python virtual environment and install the python dependencies:

    ```bash
     cd backend 
     python3 -m venv venv
     source venv/bin/activate
     poetry install
    ```

4. Install the frontend dependencies:

    ```bash
     cd ..
     cd frontend 
     npm install
    ```
    
5. Provision and deploy the project to Azure:

    ```shell
    azd up
    ```
    You will also need to ensure the environment variables are accessible. You can do this by running the following command: 
    
    ```bash
    azd env get-values > .env
    ```
    Confirm that this step has happened successfuly by checking if a `.env` file has been added to the `backend` folder. 

6. We can now generate the embeddings of the documents in the `./data` directory. In this sample it contains a pdf file with mail standards. 

    ```bash
    poetry run generate
    ```
7. Configure a CI/CD pipeline:

    ```shell
    azd pipeline config
    ```

The app is now ready to run! To test it, run the following commands:

1. First run the Flask development server
  ```bash
  cd ../backend
  python main.py
  ```

2. Next open a **new terminal** and launch the web app

  ```bash
  cd frontend
  npm run dev
  ```

Open the URL `http://localhost:3000` in your browser to interact with the bot.
An example question to ask is 'Can you tell me how much it costs to send a large parcel to France?'

## Guidance

### Region Availability

This template uses `gpt-35-turbo` version `1106` which may not be available in all Azure regions. Check for [up-to-date region availability](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#standard-deployment-model-availability) and select a region during deployment accordingly
  * We recommend using `swedencentral`

### Costs

Pricing varies per region and usage, so it isn't possible to predict exact costs for your usage.
However, you can use the [Azure pricing calculator](https://azure.com/e/bf51ef20b57a4da08e47511938ad5415) for the resources below to get an estimate.

- Azure Container Apps: Consumption plan, Free for the first 2M executions. Pricing per execution and memory used. [Pricing](https://azure.microsoft.com/en-us/pricing/details/container-apps/)
- Azure OpenAI: Standard tier, GPT and Ada models. Pricing per 1K tokens used, and at least 1K tokens are used per question. [Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)

> [!WARNING]
> To avoid unnecessary costs, remember to take down your app if it's no longer in use, either by deleting the resource group in the Portal or running `azd down --purge`.

### Security

> [!NOTE]
> When implementing this template please specify whether the template uses Managed Identity or Key Vault

This template has either [Managed Identity](https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview) or Key Vault built in to eliminate the need for developers to manage these credentials. Applications can use managed identities to obtain Microsoft Entra tokens without having to manage any credentials. Additionally, we have added a [GitHub Action tool](https://github.com/microsoft/security-devops-action) that scans the infrastructure-as-code files and generates a report containing any detected issues. To ensure best practices in your repo we recommend anyone creating solutions based on our templates ensure that the [Github secret scanning](https://docs.github.com/code-security/secret-scanning/about-secret-scanning) setting is enabled in your repos.


## Resources

Here are some resources to learn more about the technologies used in this sample:

- [LlamaIndexTS Documentation](https://ts.llamaindex.ai) - learn about LlamaIndex (Typescript features).
- [Generative AI For Beginners](https://github.com/microsoft/generative-ai-for-beginners)
- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/overview)
- [Azure OpenAI Assistant Builder](https://github.com/Azure-Samples/azure-openai-assistant-builder)
- [Chat + Enterprise data with Azure OpenAI and Azure AI Search](https://github.com/Azure-Samples/azure-search-openai-python)

You can also find [more Azure AI samples here](https://github.com/Azure-Samples/azureai-samples).

## Troubleshooting

If you can't find a solution to your problem, please [open an issue](https://github.com/Azure-Samples/llama-index-python/issues) in this repository.

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
