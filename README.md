## Schema Management Using FAAS.

This repo provides a example of using FAAS for CRUD operations for managing schema on Openwhisk as platform and postgres as backend. Functions are written in python.

OpenWhisk is a cloud-first distributed event-based programming service. It provides a programming model to upload event handlers to a cloud service, and register the handlers to respond to various events. Learn more at http://openwhisk.apache.org.

#### Table of contents

1. [Enviornment Setup](#envsetup)
2. [Install OpenWhisk And Postgresql](#owinstall)
3. [Install Schema Actions](#actioninstall)
4. [REST API](#rest)
  * [Description](#desc)
  * [Usage Examples](#exp)
5. [Tutorial/Example](#tutorial)
6. [Logging](#logs)
7. [Testing](#testing)
8. [GIT](#git)
9. [RESOURCES](#resources)

### <a name="envsetup"></a> Environment Setup

This part talks about setting up local environment based on kubernetes using docker in docker cluster or dind-cluster.

Everything is downloaded and saved to repository, for more details refer to dind-cluster README. If you are not interested in details just run below command.

Ensure [prerequisites](#prereq) are installed.

#### Cluster clean, up, down

```bash
dind-cluster/dind-cluster-v1.15.sh clean
```

```bash
USE_HAIRPIN=true dind-cluster/dind-cluster-v1.15.sh up
```

```bash
dind-cluster/dind-cluster-v1.15.sh down
```

### <a name="owinstall"></a> Install OpenWhisk And Postgresql

To understand details study the script and check dind-cluster/README otherwise just run the script !

```bash
cd dind-cluster
./install_ow_and_pg_dind.sh
cd -
```
### <a name="actioninstall"></a> Install Schema Actions

Run the script to build and install the package in src.

```bash
./install_schema_actions.sh
```

This script does below things.
1. Build a zip package as per openwhisk specs
2. Get postgres connection information.
3. Install schema actions
4. Setup schema api's with the API gateway.
5. Run initialize db action.

### <a name="rest"></a> REST API

URL's are examples, may change with installation to installation.

#### <a name="desc"></a> Description

1. Action: /guest/schema_faas/get_schema
   - API Name: smAPI
   - Base path: /sm
   - Path: /schemas
   - Verb: get
   - URL: https://10.192.0.3:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/sm/schemas

1. Action: /guest/schema_faas/post_schema
   - API Name: smAPI
   - Base path: /sm
   - Path: /schemas
   - Verb: post
   - URL: https://10.192.0.3:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/sm/schemas

1. Action: /guest/schema_faas/get_schema
   - API Name: smAPI
   - Base path: /sm
   - Path: /schemas/{schemaName}
   - Verb: get
   - URL: https://10.192.0.3:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/sm/schemas/{schemaName}

1. Action: /guest/schema_faas/delete_schema
   - API Name: smAPI
   - Base path: /sm
   - Path: /schemas/{schemaName}
   - Verb: delete
   - URL: https://10.192.0.3:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/sm/schemas/{schemaName}

#### <a name="exp"></a> Usage examples

1. Get ALL Schema API example:
```bash
curl -k  -X GET https://10.192.0.3:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/sm/schemas
```

2. Get Specific schema:
```bash
curl -k  -X GET https://10.192.0.3:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/sm/schemas/pm
```
3. Delete schema example:
```bash
curl -k -X DELETE https://10.192.0.3:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/sm/schemas/pm
```

4. Post new schema example: (ALL form fields mandatory)
```bash
curl -k -F name=pm -F title="my schema" -F file=@./pm.json -X POST https://10.192.0.3:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/sm/schemas
```

### <a name="tutorial"></a> Tutorial/Example

To understand basic openwhsik framework understand the example.

After set up,

- Create action
```bash
wsk action create examplereturn examples/return_body_func.py --kind python:3 --web true -i
```

- Create url in api gateway for action
```bash
wsk api create -n myapi /example /hello post examplereturn --response-type json -i
```
- Get the created url
```bash
wsk api list -i
```

- Send a request, base64 decode the response to see the ow_body.
```bash
curl -k -X POST -F myfield="value" https://10.192.0.3:31001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/example/hello
```

- understand args parameter printed in logs

 Refer to src/README, if you understand this you have achieved competence in OpenWhisk ;-)

 - see checking the logs section below to understand how to check logs

### <a name="logs"></a> Logging
For every action execute OpenWhisk createas an activation id.

To list the all the activation.

```bash
wsk activation list -i
```
Find out your activation id in list copy the id and execute below command to print logs.
```bash
wsk activation logs <activation_id> -i
```

### <a name="testing"></a> Testing

Load test are done with python package called locust.

```bash
cd ./test
./start_test_server.sh
cd -
```
locust server runs on port 8089, open in browser and run tests

https://locust.io/

### <a name="resources"></a> RESOURCES

- [OpenWhisk]
- [kubernetes]
- [Helm]
- [Postgres]

### <a name="prereq"></a>Prerequisites

- Download dind-cluster(script), wsk(clinet), kubectl(client), helm(client)

- Untar packages and move binaries to /usr/bin for example.

- go to releases and install the version of your choice in each of below.

```bash
wget https://cdn.rawgit.com/kubernetes-sigs/kubeadm-dind-cluster/master/fixed/dind-cluster-v1.15.sh
```
```bash
wget https://github.com/apache/openwhisk-cli/releases/download/0.10.0-incubating/OpenWhisk_CLI-0.10.0-incubating-linux-amd64.tgz
```

```bash
curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.13.5/bin/linux/amd64/kubectl
```

```bash
curl https://kubernetes-helm.storage.googleapis.com/helm-v2.12.2-linux-amd64.tar.gz
```
