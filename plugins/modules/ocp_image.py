#!/usr/bin/python
# Copyright (c) 2023 Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: ocp_image
author:
  - "Sagi Shnaidman (@sshnaidm)"
short_description: Get OCP image URL according to version
notes: []
description:
  - Using given version of OCP, get URL to download it from
requirements:
  - requests
options:
  tag:
    description:
      - OCP version tag like 4.12, 4.13.1 etc. Mutually exclusive with C(full_tag).
    type: str
  release:
    description:
      - OCP release type. Choose from C(ci), C(nightly), C(stable), C(candidate), C(dev-preview).
        Mutually exclusive with C(full_tag).
    type: str
    choices:
      - 'ci'
      - 'nightly'
      - 'stable'
      - 'candidate'
      - 'dev-preview'
  full_tag:
    description:
      - Full OCP version like 4.12.0-0.nightly-2023-03-09-142909, 4.13.1-202003090116.p0-1, etc.
        Mutually exclusive with C(tag) and C(release).
    type: str
  validate_certs:
    description:
      - Whether to validate SSL certificates for HTTPS requests.
    default: True
    type: bool
"""

RETURN = r"""
container:
    description:
      - OCP image URL
    returned: always
    type: dict
    sample: '{
        "ocp_image": "registry.ci.openshift.org/ocp/release:4.12.0-0.nightly-2023-03-09-142909"
    }'
    """

EXAMPLES = r"""
- name: Get OCP image URL
  ocp_image:
    tag: 4.14
    release: candidate
  register: ocp_image

- name: Get OCP image URL
  ocp_image:
    tag: 4.15
    release: nightly
  register: ocp_image

- name: Get OCP image URL
  ocp_image:
    full_tag: 4.12.0-0.nightly-2023-03-09-142909
  register: ocp_image
"""

from ansible.module_utils.basic import AnsibleModule  # noqa: F402, E402
from ..module_utils.ocp_image_lib import OCPImage  # noqa: F402, E402


def main():
    module = AnsibleModule(
        argument_spec=dict(
            tag=dict(type='str'),
            release=dict(type='str', choices=['ci', 'nightly', 'stable', 'candidate', 'dev-preview']),
            full_tag=dict(type='str'),
            validate_certs=dict(type='bool', default=True),
        ),
        required_one_of=[['release', 'tag', 'full_tag']],
        required_together=[['release', 'tag']],
        mutually_exclusive=[['release', 'full_tag'], ['tag', 'full_tag']],
        supports_check_mode=True,
    )

    results = dict(
        changed=False,
        ocp_image='',
    )

    results['ocp_image'] = OCPImage(module, **module.params).resolve_tag()
    module.exit_json(**results)


if __name__ == '__main__':
    main()
