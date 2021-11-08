#!/usr/bin/env python

"""Update databricks repo."""

import json
import sys

import requests

from plugin import dronecli, logger


class DatabricksRepos:
    def __init__(self, workspace, repo, version, token):
        self._url = f"{workspace}/api/2.0/repos"
        self._repo = repo
        self._version = version

        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

    def __repr__(self):
        """Representation of an ECSAutoscaler object."""
        return "<{} 'url': {}>".format(self.__class__, self._url)

    def get_repos(self):
        logger.info("Retrieving databricks repos")

        r = requests.get(self._url, headers=self._headers)

        try:
            r.raise_for_status()
        except requests.HTTPError:
            logger.error(f"Databricks errored out: {r.json()}")
            raise
        return r.json()

    def update_repo(self, repo_id, version):
        logger.info(f"Updating databricks repo {repo_id}")

        payload = {}
        if "v" in version:
            payload = {"tag": version}
        else:
            payload = {"branch": version}

        r = requests.patch(
            f"{self._url}/{repo_id}", headers=self._headers, data=json.dumps(payload)
        )
        try:
            r.raise_for_status()
        except requests.HTTPError:
            logger.error(f"Databricks errored out: {r.json()}")
            raise
        return r.json()

    def run(self):
        """Main plugin logic."""
        repos = self.get_repos()
        repo = None

        try:
            repo = next(filter(lambda r: r["path"] == self._repo, repos["repos"]))
        except StopIteration:
            logger.error(
                f"Could not find repository matching {self._repo} in {repos['repos']}"
            )

        if repo is not None:
            logger.info(f"Found repo {self._repo} with {repo['id']}")
            response = self.update_repo(repo_id=repo["id"], version=self._version)
            logger.info(
                f"Repository {response['url']} has been updated to commit {response['head_commit_id']}"
            )


def main():
    """The main entrypoint for the plugin."""

    try:
        workspace = dronecli.get("PLUGIN_WORKSPACE")
        token = dronecli.get("PLUGIN_TOKEN")
        repo = dronecli.get("PLUGIN_REPO")
        version = dronecli.get("PLUGIN_VERSION")

        plugin = DatabricksRepos(  # isort:skip
            workspace=workspace, token=token, repo=repo, version=version
        )

        logger.info("The drone plugin has been initialized with: {}".format(plugin))

        plugin.run()

    except Exception as e:
        logger.error("Error while executing the plugin: {}".format(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
