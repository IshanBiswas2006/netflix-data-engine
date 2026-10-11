const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const http = require('http');

async function getWsUrl(port) {
  for (let i = 0; i < 30; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}/json/version`);
      if (res.ok) {
        const data = await res.json();
        return data.webSocketDebuggerUrl;
      }
    } catch (e) {}
    await new Promise(r => setTimeout(r, 200));
  }
  throw new Error('Chrome remote debugging did not become available');
}

class CDPClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.id = 1;
    this.pending = new Map();
    this.handlers = new Map();
  }

  async connect() {
    this.ws = new WebSocket(this.wsUrl);
    await new Promise((resolve, reject) => {
      this.ws.onopen = resolve;
      this.ws.onerror = reject;
    });

    this.ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) reject(msg.error);
        else resolve(msg.result);
      } else if (msg.method) {
        const handlers = this.handlers.get(msg.method) || [];
        for (const h of handlers) h(msg.params);
      }
    };
  }

  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = this.id++;
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  on(event, handler) {
    if (!this.handlers.has(event)) this.handlers.set(event, []);
    this.handlers.get(event).push(handler);
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

async function run() {
  const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const userDataDir = path.join(process.env.TEMP, 'chrome-scraper-' + Date.now());
  const port = 9225;

  console.log('Launching headless Chrome on port', port, '...');
  const chromeProc = spawn(chromePath, [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    '--disable-gpu',
    '--no-first-run',
    '--window-size=1920,1080',
    `--user-data-dir=${userDataDir}`
  ]);

  try {
    const wsUrl = await getWsUrl(port);
    console.log('Connected to Chrome DevTools Protocol at:', wsUrl);

    // Create a new target/tab
    const newTabRes = await fetch(`http://127.0.0.1:${port}/json/new?https://nehayadav.framer.website/`, { method: 'PUT' });
    const tabData = await newTabRes.json();
    const tabWsUrl = tabData.webSocketDebuggerUrl;

    const cdp = new CDPClient(tabWsUrl);
    await cdp.connect();

    const capturedUrls = new Set();
    const networkRequests = [];

    cdp.on('Network.requestWillBeSent', (params) => {
      const url = params.request.url;
      if (url.startsWith('http')) {
        capturedUrls.add(url);
        networkRequests.push({
          url,
          type: params.type,
          initiator: params.initiator?.type
        });
      }
    });

    cdp.on('Network.responseReceived', (params) => {
      const url = params.response.url;
      if (url.startsWith('http')) {
        capturedUrls.add(url);
      }
    });

    await cdp.send('Network.enable');
    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');

    const pagesToVisit = [
      'https://nehayadav.framer.website/',
      'https://nehayadav.framer.website/about'
    ];

    for (const targetUrl of pagesToVisit) {
      console.log(`\nNavigating to ${targetUrl} ...`);
      await cdp.send('Page.navigate', { url: targetUrl });

      // Wait for page load
      await new Promise(r => setTimeout(r, 4000));

      console.log('Scrolling page to trigger lazy-load assets & animations...');
      // Scroll smoothly down the page
      for (let s = 0; s <= 4000; s += 400) {
        await cdp.send('Runtime.evaluate', {
          expression: `window.scrollTo({ top: ${s}, behavior: 'smooth' });`
        });
        await new Promise(r => setTimeout(r, 250));
      }

      await cdp.send('Runtime.evaluate', {
        expression: `window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });`
      });
      await new Promise(r => setTimeout(r, 3000));

      // Scroll back up
      await cdp.send('Runtime.evaluate', {
        expression: `window.scrollTo({ top: 0, behavior: 'smooth' });`
      });
      await new Promise(r => setTimeout(r, 1000));
    }

    console.log(`\nCaptured ${capturedUrls.size} network URLs via Chrome DevTools.`);
    fs.writeFileSync('captured_network_urls.json', JSON.stringify({
      count: capturedUrls.size,
      urls: Array.from(capturedUrls),
      requests: networkRequests
    }, null, 2));

    cdp.close();
  } finally {
    chromeProc.kill();
    console.log('Chrome process stopped.');
  }
}

run().catch(err => {
  console.error('Crawler error:', err);
  process.exit(1);
});
