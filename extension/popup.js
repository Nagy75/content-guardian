const api = globalThis.chrome || globalThis.browser;
api.storage.local.get({blockedWords: [], replacement: '####', skipIntervals: []}).then ?
  api.storage.local.get({blockedWords: [], replacement: '####', skipIntervals: []}).then(console.log) : null;
