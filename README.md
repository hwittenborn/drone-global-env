<div align=center><h1>drone-global-env</h1></div>

## Introduction
drone-global-env is an [environment extension](https://docs.drone.io/extensions/environment/) for Drone CI, allowing you to specify environment variables that will be passed to all of your CI builds.

## Installing
The only supported way for running is through the official Docker image which can be pulled from the following repository:

```
proget.hunterwittenborn.com/docker/hwittenborn/drone-global-env
```

## Running
First create a file named `config.yaml` with the following content:

```yaml
- name: "key" # Specifies the name of the environment variable.
  value: "key_value" # Specified the value of the environment variable.
  mask: true # Specifies if the environment variable's value is hidden from Drone CI's logs.
```

And just repeat for every environment variable you want to add.

```yaml
- name: "key1"
  value: "key_value1"
  mask: true

- name: "key2"
  value: "key_value2"
  mask: false
  ```

Next, set the `DRONE_ENV_PLUGIN_ENDPOINT` and `DRONE_ENV_PLUGIN_TOKEN` environment variables under the config of your runner (the service that runs builds under Docker, Kubernetes, SSH, etc).

After, create the `drone-global-env` container, configured as follows:

- Mount `config.yaml` at `/data/config.yaml`

- Pass the `DRONE_ENV_PLUGIN_TOKEN` variable, with its value set the same as that set under your runner's config.

- Bind a public port to the container's internal port `8080`.

For example:

```sh
docker run -v "./config.yaml:/data/config.yaml" \
           -p "8080:8080" \
           -e "DRONE_ENV_PLUGIN_TOKEN=your_token_here" \
           proget.hunterwittenborn.com/docker/hwittenborn/drone-global-env
```

## Support
Issues and questions regarding usage should be posted under the issue tracker.
