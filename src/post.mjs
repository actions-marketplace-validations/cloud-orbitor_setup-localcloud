import { cleanup } from './runtime.mjs';
try {
  cleanup(process.env.STATE_localcloud_record ? JSON.parse(process.env.STATE_localcloud_record) : null);
  console.log('LocalCloud cleanup complete');
} catch (error) { console.error(error.message); process.exitCode = 1; }
