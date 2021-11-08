drone-databricks-repos
====================

* Author: `Florian Dambrine <florian@gumgum.com>`

A Drone plugin to sync a [Databricks repository](https://docs.databricks.com/repos.html) using the Databricks API

# :notebook: Usage

* Sync the Databricks repository `/Repos/production/repository-name` to be at commit `${DRONE_BRANCH}`

```yaml
---

kind: pipeline
name: databricks
steps:
  - name: databricks-repo-sync
    image: public.ecr.aws/gumgum-verity/ci/drone-databricks-repos:v1.0.0
    settings:
      workspace: https://<company>.cloud.databricks.com
      token:
        from_secret: databricks_token
      repo: /Repos/production/repository-name
      version: ${DRONE_BRANCH}

```

---

# :gear: Parameter Reference

| Parameter   | Description                        | Example                                  |
| ----------- | ---------------------------------- | ---------------------------------------- |
| `workspace` | The Databricks Workspace URL       | `https://<company>.cloud.databricks.com` |
| `token`     | A Databricks token                 | `dapic*******************************`   |
| `repo`      | Full path to Databricks repository | `/Repos/production/repository-name`      |
| `version`   | Either a Git tag or a branch name  | `v1.0.0` or `some-branch`                |

---

# :beginner: Development

* Run the plugin directly from a built Docker image:

```bash
docker run -i \
           -v $(pwd)/plugin:/opt/drone/plugin \
           -e PLUGIN_WORKSPACE=${DATABRICKS_WORKSPACE} \
           -e PLUGIN_TOKEN=${DATABRICKS_TOKEN} \
           -e PLUGIN_REPO=${DATABRICKS_REPO} \
           -e PLUGIN_VERSION=branch-name \
           public.ecr.aws/gumgum-verity/ci/drone-databricks-repos:v1.0.0
```
