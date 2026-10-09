# Setup LocalCloud

Run Google Cloud integration tests against a LocalCloud Docker environment in GitHub Actions. This action starts the image directly, waits for the selected services, prepares a local project, and exports SDK settings to subsequent steps. It does not install the LocalCloud CLI or require Google Cloud credentials.

The first release targets Ubuntu 24.04 x64 VM runners and Python Cloud Storage, Pub/Sub and Firestore workflows. Service compatibility is operation-specific; tests against an emulator do not replace final Google Cloud validation.

## Quickstart

```yaml
permissions:
  contents: read
jobs:
  integration:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
      - uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065
        with:
          python-version: '3.12'
      - uses: cloud-orbitor/setup-localcloud@v0.1.0
      - run: pip install -r requirements.txt
      - run: python -m pytest
```

Use the release's full commit SHA for immutable action pinning. The default runtime image is pinned by digest. SDK packages remain under your project's control; the [qualification example](examples/python-smoke.py) uses exact versions in [requirements.txt](examples/requirements.txt).

## Direct Docker and native GitHub services

LocalCloud also runs independently of this action and the CLI. A native service declaration owns its lifecycle; this action only prepares and configures it:

```yaml
services:
  localcloud:
    image: agentcloud/localcloud@sha256:88e85b86b294e1e4f71b8c63ec43de79d170946ff39556f0e2709f66aa0d368c
    env:
      LOCALCLOUD_SERVICES: gcs,pubsub,firestore
      LOCALCLOUD_PROJECT: localcloud-ci
      LOCALCLOUD_TELEMETRY: 'false'
      LOCALCLOUD_DOCKER_ACCESS: 'false'
    ports:
      - 5380:5380
      - 5382:5382
      - 5383:5383
      - 5384:5384
    options: --memory 4g
steps:
  - uses: cloud-orbitor/setup-localcloud@v0.1.0
    with:
      runtime-url: http://127.0.0.1:5380
```

The complete tested workflow is [.github/workflows/qualify.yml](.github/workflows/qualify.yml). Host consumers use loopback published ports. In a container job, the service address is `http://localcloud:5380` and SDK endpoints use that hostname with internal ports. Container-job use still needs separate qualification.

For plain Docker, follow the [runtime image instructions](https://local.cloud/docs/), then use its `/readiness` and `/env` endpoints. Installing the CLI is an optional convenience. Running tests inside the runtime image requires a compatible application toolchain and preservation of its startup entrypoint; this setup action leaves tests on the runner or in your own test image.

## Inputs and outputs

| Input | Default | Meaning |
| --- | --- | --- |
| `image` | Public LocalCloud 0.1.5 image digest | Immutable runtime image; used only when this action starts Docker |
| `services` | `gcs,pubsub,firestore` | Exact enabled-service list |
| `project-id` | `localcloud-ci` | Local project to create/select |
| `runtime-url` | empty | Existing `http://host:5380` gateway with canonical service ports; no Docker lifecycle changes |
| `timeout` | `120` | Readiness timeout in seconds, from 1 to 1800 |

Outputs are `runtime-url`, `container-id` (empty for an existing runtime), and `project-id`. The job summary records the selected project/services and action-owned image digest.

The action exports the runtime's supported emulator/project/local-auth variables to subsequent steps in the same job. Automatic Docker mode publishes image TCP listeners on unique loopback ports and rewrites SDK endpoints accordingly. Existing-runtime mode requires canonical ports; custom external host-port mappings are not supported by that mode yet.

## Isolation and limits

- Each automatic setup creates its own container and anonymous data volume. The post hook verifies its ownership label and removes only those resources. Existing runtimes and developer volumes are retained.
- The image receives a 4 GiB limit. Docker and adequate runner memory/disk must be available; slim, hosted macOS and hosted Windows runners are outside this release's Docker support.
- Docker socket access is disabled in automatic mode. Docker-backed compute/cluster workloads need a separately configured and qualified runtime.
- Other service IDs can be evaluated, but only the documented Python profile is release-qualified. Unsupported services, env formats or unready runtimes fail setup.
- Emulator environment support varies by language. Java Pub/Sub requires explicit transport/credentials setup; there is no universal zero-code guarantee for all SDKs.
- This action validates generated local targets; it is not an egress firewall and cannot stop application code using hardcoded Google endpoints. Never supply production credentials for these local tests.
- The post hook is best effort if the runner disappears. Persistent/self-hosted agents need an ownership-scoped orphan policy.
- MCP is available from the runtime for optional agent workflows; ordinary SDK tests do not require it. This action does not install global MCP configuration or enable management writes.

## Licensing, privacy and support

This small action is MIT-licensed. It downloads a separately distributed proprietary runtime; the image's [LocalCloud Public Preview License](https://local.cloud/license/) governs that runtime. Image 0.1.5 declares `LicenseRef-LocalCloud-Public-Preview-2.0` and carries the agreement at `/opt/localcloud/LICENSE`. The preview permits internal development/testing/CI; production hosting, redistribution and managed-service use have separate restrictions.

Automatic mode sets the runtime telemetry preference to false and supplies no real cloud credentials. Consult [LocalCloud privacy and outbound behavior](https://local.cloud/privacy/) for the runtime's boundaries; no offline or zero-egress guarantee is made. Existing-runtime preferences remain with its owner.

Report action issues in this repository. Product information and contact details: [local.cloud](https://local.cloud/).

## Development and evidence

Use Node 24 and `node --test test/runtime.test.mjs`. There are no npm runtime dependencies or generated bundles. The qualification workflow checks standard SDK readback, existing-runtime preservation, owned cleanup, and failed-setup cleanup. Public release evidence is recorded in [docs/release-evidence.md](docs/release-evidence.md).
