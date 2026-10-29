Promise.all([9099, 8180, 9199, 4400].map(port =>
  fetch(`http://127.0.0.1:${port}/`).then(() => true)
)).then(() => process.exit(0)).catch(() => process.exit(1));
