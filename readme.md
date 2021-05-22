# Krikey Coding Challenge

## Contents:
1. Requirements
2. Steps to run the project

## Requirements

1. Docker Desktop 
2. Python3
3. PostgreSQL
4. Git

## Steps to run the project

### i. Create a new project in Google cloud platform and enable billing:

Sign in to the console and create a new project.
```
https://console.cloud.google.com
```
Make sure to enable billing by following the link down below.
```
https://cloud.google.com/billing/docs/how-to/modify-project?authuser=1
```

### ii. Install CloudSDK, Enable the Cloud SQL, and Compute Engine APIs:
> Install CloudSDK

Follow this link to install the required CloudSDK to your local system.
```
https://cloud.google.com/sdk/docs/install
```

> Installing the Cloud SQL Proxy

#### Download the Cloud SQL Auth proxy:

If you are using macOS 64-bit:
```
curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64
```
If you are using macOS 32-bit:
```
curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.386
```

If you are using linux 64-bit:
```
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
```

If you are using linux 32-bit:
```
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.386 -O cloud_sql_proxy
```

> Make the Cloud SQL Auth proxy executable:

```
chmod +x cloud_sql_proxy

```

### iii. Install PostgreSQL in your local system
If you use a Linux OS: 
```
sudo apt-get install postgresql

```
If you use a Mac OS:
```
brew install postgres

```
### iv. Start PostgreSQL server:

If you use a Linux OS: 
```
psql --host 127.0.0.1 --user postgres --password

```
If you use a Mac OS:
```
brew services start postgresql
```

### v. Clone the project
```
git clone https://github.com/vidhyasagar13/krikeyCodingChallenge.git
```

### vi. Initialize the image in the Google Clound Container Registry

> Open `cloudbuild.yaml` file and replace the project_id with your project id created in the google cloud. Also, change the TAG NAME to a name you want.

> After replacing, run the following command.

```
gcloud builds submit .
```
Please take a note of the '.' in the end. It is very important. 
This step builds and pushes the image to google cloud container registry.


> The above step will build the docker image first with the docker-compose file. If you need to change the username and password of the postgreSQL database, you can change either directly there or by replacing them and giving it in the environment variable.

### vii. Initialize the cluster for deploying our created image. 

Go to your Google Cloud console and take a note of your image tag. 

Like previous step, open `deployment.yml` and replace IMAGE TAG with the image tag that was displayed in your google cloud console.

> After replacing, run the following command

```
kubectl apply -f deployment.yml
```
The output will be similar to this
```
...... deployments created
```
### viii. Initialize the cluster for deploying our created image. 

The above step would have created the necessary pods and given some time the pods will show `STATUS : READY`

To check this,

```
kubectl get pods --watch
```
The output will be similar to this
```
POD NAME                    READY    UPDATE       MESSAGE
<PROJECT ID> - <some-hash>   1/1     Up-To-Date   ....
<PROJECT ID> - <some-hash>   1/1     Up-To-Date   ....
<PROJECT ID> - <some-hash>   1/1     Up-To-Date   ....
```

Go to your Google Cloud console and take a note of your image tag. 

Like previous step, open `service.yml` and replace PROJECT ID with the PROJECT ID that was displayed in your google cloud console.

> After replacing, run the following command

```
kubectl apply -f service.yml
```
The output will be similar to this
```
...... services created
```

To check our services,
```
kubectl get services
```
The output will be similar to this...

```
SERVICE NAME                INTERNAL IP   EXTERNAL IP  ....
<PROJECT ID> - <some-hash>  10.34.21.54.  <pending>    .... 
```

> Here the internal IP is just a dummy IP address and it will be same for you.

> Given some time, the IP address will be shown. Open a new browser, and hit the external IP. 

Voila, now you've successfully deployed the website to GCP kubernetes cluster.

