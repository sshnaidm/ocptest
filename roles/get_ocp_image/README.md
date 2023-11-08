# get_ocp_image

The role discovers OCP image from given parameters. It can be used for extracting an `openshift-install` binary from the specific image.

## Requirements

Ansible installed, `requirements.txt` of role.

## Role Variables

### Input variables

--------------
| Name           | Type | Default Value | Des cription                        | Example |
| -------------- | -----| ------------- | -----------------------------------|---------|
|**`get_ocp_image_tag`** | string | No default value | Major version of OCP. | `4.13` |
|**`get_ocp_image_release`** | string | No default value | Release type of OCP. Choose from: `ci`, `nightly`, `dev-preview`, `stable`, `candidate` | `nightly` |
|**`get_ocp_image_full_version`** | string | No default value | Full tag version of OCP image. | `4.15.0-0.ci-2023-11-07-184920` |

### Output variables

--------------
| Name           | Type | Default Value | Des cription                        | Example |
| -------------- | -----| ------------- | -----------------------------------|---------|
|**`get_ocp_image_url`** | string | No default value | Discovered OCP image container URL | `registry.ci.openshift.org/ocp/release:4.12.0-0.nightly-2023-11-08-101917` |

## Dependencies

`requests` library for module `ocp_image`

## Example Playbook

Example of getting OCP image for last stable release of 4.13:

```yaml
    - hosts: servers
      tasks:
          - name: Get OCP version
            import_role:
                name: sshnaidm.ocptest.get_ocp_image
            vars:
                get_ocp_image_tag: 4.13
                get_ocp_image_release: stable
```

Example of getting OCP image for specific nightly release `4.14.0-0.nightly-2023-11-08-004805`:

```yaml
    - hosts: servers
      tasks:
          - name: Get OCP version
            import_role:
                name: sshnaidm.ocptest.get_ocp_image
            vars:
                get_ocp_image_full_version: "4.14.0-0.nightly-2023-11-08-004805"
```

## License

Apache 2

## Author Information

Telco team
