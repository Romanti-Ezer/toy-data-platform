# filesystem pipeline

Este projeto utiliza **DLT (Data Load Tool)** para ingerir e processar arquivos CSV localmente, salvando os dados em um bucket S3 (MinIO).  

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.10+**
- **pip** (gerenciador de pacotes do Python)
- **Docker** (caso deseje executar via container)
- **MinIO** (ou outro armazenamento S3 compatível)

## Setup

Crie um ambiente virtual

```
virtualenv venv
```

ative-o

* no linux / mac

```
source venv/bin/activate
```
* no windows

```
venv\Scripts\activate
```

Agora voce pode instalar as dependencias

```
pip install -r requirements.txt
```

Podemos agora substitur o arquivo .env.sample e criar o arquivo .env com base nele. Depois, preencha o arquivo .env com as variaveis do projeto.

Em seguida podemos exportar as variaveis de ambiente

no linux:
```
export $(grep -v '^#' .env | xargs)
```

no windows:
```
Get-Content .env | ForEach-Object {
    $name, $value = $_ -split '=', 2
    [System.Environment]::SetEnvironmentVariable($name, $value, "Process")
}

```

para rodar localmente:
```
python filesystem_pipeline.py -t netflix_titles 
```

para buildar a imagem local
```
docker build -t my-dlt-pipeline .
```

para rodar no container:

```
docker run --rm --env-file .env --network platform-net my-dlt-pipeline python filesystem_pipeline.py -t netflix_titles
```
