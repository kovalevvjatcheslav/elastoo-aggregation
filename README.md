![](https://github.com/kovalevvjatcheslav/elastoo-aggregation/workflows/Pipeline/badge.svg)

Run project (docker required to run the project):  
`echo <GITHUB_TOKEN> | docker login docker.pkg.github.com -u <LOGIN> --password-stdin`  
`docker run --rm --name elastoo -p 8000:8000 docker.pkg.github.com/kovalevvjatcheslav/elastoo-aggregation/elastoo:latest`  

The swagger specification:
https://app.swaggerhub.com/apis-docs/kovalevvjatcheslav/elastoo/1.0.0-oas3