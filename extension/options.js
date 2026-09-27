const api = globalThis.chrome || globalThis.browser;
const get = (defaults) => new Promise(resolve => api.storage.local.get(defaults, resolve));
const set = (value) => new Promise(resolve => api.storage.local.set(value, resolve));
(async () => {
  const value = await get({blockedWords: [], replacement: '####', skipIntervals: []});
  words.value = value.blockedWords.join('\n'); replacement.value = value.replacement;
  intervals.value = value.skipIntervals.join('\n');
})();
save.onclick = async () => {
  const blockedWords = words.value.split(/\r?\n/).map(x => x.trim().toLowerCase()).filter(Boolean);
  const skipIntervals = intervals.value.split(/\r?\n/).map(x => x.trim()).filter(Boolean);
  await set({blockedWords, replacement: replacement.value || '####', skipIntervals});
  saved.textContent = ' Saved'; setTimeout(() => saved.textContent = '', 1500);
};
