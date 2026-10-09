import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { cleanup, docker } from '../src/runtime.mjs';

const id = process.env.LOCALCLOUD_CONTAINER_ID;
const container = JSON.parse(docker(['inspect', id]))[0];
const anonymousVolumes = container.Mounts.filter(m => m.Type === 'volume').map(m => m.Name);
cleanup({ id, owner: container.Config.Labels['cloud.local.setup-localcloud.owner'] });
assert.notEqual(spawnSync('docker',['inspect',id]).status,0,'owned container survived cleanup');
for (const name of anonymousVolumes) assert.notEqual(spawnSync('docker',['volume','inspect',name]).status,0,'anonymous test volume survived cleanup');
console.log('Owned container and anonymous volume removed; automatic post hook is idempotent');
