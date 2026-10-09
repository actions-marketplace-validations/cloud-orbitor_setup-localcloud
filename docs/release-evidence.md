# Release evidence

## Current release candidate 0.1.1

The selected/default profile is now `gcs,pubsub,bigquery`; Firestore is excluded from current examples and qualification. The pinned 0.1.5 image passed local ARM64 fresh action startup, generated endpoints, Storage object readback, Pub/Sub message readback, BigQuery dataset/table creation, row insertion, SQL readback, and automatic container/anonymous-volume cleanup. Python BigQuery 3.46.1 uses the generated endpoint through ClientOptions with AnonymousCredentials. Ten Node 24 tests pass. Hosted and public-consumer results for this corrected profile will be recorded after completion.

## Historical release 0.1.0

The evidence below describes the original 0.1.0 profile only. It is retained for provenance and is not a current Firestore support claim.

Runtime: `agentcloud/localcloud@sha256:88e85b86b294e1e4f71b8c63ec43de79d170946ff39556f0e2709f66aa0d368c` (release tag 0.1.5).

### Local ARM64 (0.1.0)

The exact multi-architecture release image passed fresh action startup, generated SDK settings, Google Python SDK Cloud Storage upload/download, Pub/Sub publish/pull/acknowledgement and Firestore write/readback. Ownership-checked cleanup removed the action's container and anonymous volume; a second cleanup succeeded as a no-op. Ten Node 24 tests passed. No CLI was installed by the action.

### GitHub hosted AMD64 (0.1.0)

[Qualification run 37980659078](https://github.com/cloud-orbitor/setup-localcloud/actions/runs/37980659078) passed all four jobs on Ubuntu 24.04: unit, managed Docker SDK readback/owned cleanup, native service SDK readback/preservation, and rejected-service failure cleanup. Qualified action code commit: `c2add0415e1b2bfd3dc0e9a5858f35c8951222f0`.

The qualification used Python 3.12 with Storage 3.6.0, Pub/Sub 2.33.0 and Firestore 2.23.0. The local check used Python 3.13. Other SDK profiles, container-job consumers, same-container toolchains, Docker-backed workloads and runner-loss cleanup were not qualified for this release.

### Publication (0.1.0)

[Independent public-SHA consumer run 37981540971](https://github.com/cloud-orbitor/setup-localcloud/actions/runs/37981540971) passed Cloud Storage, Pub/Sub and Firestore readback using `cloud-orbitor/setup-localcloud@c2add0415e1b2bfd3dc0e9a5858f35c8951222f0`. A checker registered before setup ran after the setup post hook and verified that the actual container and anonymous volume no longer existed. This verifies automatic cleanup, rather than only calling the cleanup function in a test step.

[v0.1.0 is publicly released](https://github.com/cloud-orbitor/setup-localcloud/releases/tag/v0.1.0), pinned to commit `de6d236db036be4c8b96879392d22a1feb5047c6`. [Release-tag consumer run 37982317639](https://github.com/cloud-orbitor/setup-localcloud/actions/runs/37982317639) passed all three SDK readbacks and actual automatic post cleanup using `cloud-orbitor/setup-localcloud@v0.1.0`.

A repository release is separate from Marketplace publication. The Marketplace checkbox remains disabled until the cloud-orbitor owner accepts GitHub Marketplace Developer Agreement v2.4. That acceptance is awaiting explicit human confirmation; no Marketplace listing is claimed yet.
