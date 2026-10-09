import { main } from './runtime.mjs';
try { await main(); }
catch (error) { console.error(error.message); process.exitCode = 1; }
