## Using Kubernetes?

If you're using Kuberentes, I would strongly encourage you to read this [blog post](https://hkiang01.github.io/kubernetes/keycloak/) that describes how to use Keycloak in a manner that secures APIs independently of the application.
For code samples see https://github.com/hkiang01/keycloak-demo


## Quickstart

1. Log into keycloak admin console (see docker compose)
2. Create "Clients" realm (upper left)
3. Within "Clients" realm, create a client called "app" with the following URLs

    ![alt text](images/app_urls.png "app URLs")
4. Create a user with username and password set to "test"
5. `docker-compose down && docker-compose build && docker-compose up`
6. Navigate to `localhost:8000/login`
