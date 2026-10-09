# Release evidence

Runtime: `agentcloud/localcloud@sha256:88e85b86b294e1e4f71b8c63ec43de79d170946ff39556f0e2709f66aa0d368c` (release tag 0.1.5).

## Local ARM64

The exact multi-architecture release image passed fresh action startup, generated SDK settings, Google Python SDK Cloud Storage upload/download, Pub/Sub publish/pull/acknowledgement and Firestore write/readback. Ownership-checked cleanup removed the action's container and anonymous volume; a second cleanup succeeded as a no-op. Ten Node 24 tests passed. No CLI was installed by the action.

## GitHub hosted AMD64

[Qualification run 37980659078](https://github.com/cloud-orbitor/setup-localcloud/actions/runs/37980659078) passed all four jobs on Ubuntu 24.04: unit, managed Docker SDK readback/owned cleanup, native service SDK readback/preservation, and rejected-service failure cleanup. Qualified action code commit: `c2add0415e1b2bfd3dc0e9a5858f35c8951222f0`.

The qualification used Python 3.12 with Storage 3.6.0, Pub/Sub 2.33.0 and Firestore 2.23.0. The local check used Python 3.13. Other SDK profiles, container-job consumers, same-container toolchains, Docker-backed workloads and runner-loss cleanup were not qualified for this release.

## Publication

Independent SHA/tag consumption and the public Marketplace page are recorded after their respective checks. A repository release is separate from Marketplace publication. GitHub requires the cloud-orbitor owner to accept its Marketplace Developer Agreement before listing.
