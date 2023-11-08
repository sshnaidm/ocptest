from __future__ import absolute_import, division, print_function

__metaclass__ = type

from urllib.parse import urljoin
import json
from .common.utils import get_url, Logger

API_URL = "https://amd64.ocp.releases.ci.openshift.org/api/v1/releasestream/%s.0-0.%s/latest"
STABLE_URL = "https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable-%s/"
CANDIDATE_URL = "https://mirror.openshift.com/pub/openshift-v4/clients/ocp/candidate-%s/"
DEV_PREVIEW_URL = "https://mirror.openshift.com/pub/openshift-v4/clients/ocp-dev-preview/latest-%s/"


class OCPImage:
    def __init__(self, module=None, tag=None, release=None, full_tag=None, **kwargs):
        self.tag = tag
        self.release = release
        self.full_tag = full_tag
        self.module = module
        self.log = Logger(module).log

    def resolve_tag(self):
        if self.full_tag:
            self.log.info(f"Using full tag {self.full_tag}")
            if "ci" in self.full_tag or "nightly" in self.full_tag:
                self.log.info(f"Using version registry.ci.openshift.org/ocp/release:{self.full_tag}")
                return f"registry.ci.openshift.org/ocp/release:{self.full_tag}"
            if not self.full_tag.endswith("-x86_64"):
                self.log.debug(f"Adding -x86_64 to {self.full_tag}")
                self.full_tag += "-x86_64"
            self.log.info(f"Using version quay.io/openshift-release-dev/ocp-release:{self.full_tag}")
            return f"quay.io/openshift-release-dev/ocp-release:{self.full_tag}"

        if self.release in ("ci", "nightly"):
            self.log.info(f"Finding {self.release} release for tag {self.tag}")
            url = API_URL % (self.tag, self.release)
            self.log.debug(f"Getting URL {url}")
            response = get_url(url, self.module)
            try:
                data = json.loads(response)
            except Exception:
                self.module.fail_json(f"Failed to parse {url} as JSON: {response}")
            self.log.info(f"Using {self.release} version {data['pullSpec']}")
            return data["pullSpec"]

        if self.release in ("stable", "candidate", "dev-preview"):
            self.log.info(f"Finding {self.release} release for tag {self.tag}")
            if self.release == "stable":
                release_url = urljoin(STABLE_URL % self.tag, "release.txt")
            elif self.release == "candidate":
                release_url = urljoin(CANDIDATE_URL % self.tag, "release.txt")
            elif self.release == "dev-preview":
                release_url = urljoin(DEV_PREVIEW_URL % self.tag, "release.txt")
            self.log.debug(f"Getting URL {release_url}")
            url_data = get_url(release_url, self.module)
            if "Pull From: " in url_data:
                for line in url_data.splitlines():
                    if "Pull From: " in line:
                        self.log.debug(f"Found {self.release} in line {line.strip()}")
                        result = line.split("Pull From: ")[1].strip()
                        self.log.info(f"Using {self.release} version {result}")
                        return result
            self.module.fail_json(f"Failed to parse {self.release} release.txt: {release_url}")
        if not self.tag and not self.release and not self.full_tag:
            self.module.fail_json("No tag or release or full_tag specified")
