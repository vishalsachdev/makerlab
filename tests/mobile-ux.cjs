// Setup: cd tests && npm ci && npx playwright install chromium && npm test
const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const { spawn } = require('node:child_process');
const { chromium } = require('playwright');
const path = require('node:path');
let browser, server, base;
before(async () => {
  server = spawn('python3', ['-u', '-m', 'http.server', '0', '--bind', '127.0.0.1'], {
    cwd: path.resolve(__dirname, '..'), stdio: ['ignore', 'pipe', 'ignore']
  });
  base = await new Promise((resolve, reject) => {
    server.stdout.on('data', b => { const m = b.toString().match(/port (\d+)/); if (m) resolve(`http://127.0.0.1:${m[1]}`); });
    server.on('error', reject);
  });
  browser = await chromium.launch({ headless: true, executablePath: process.env.CHROMIUM_EXECUTABLE_PATH || undefined });
});
after(async () => { if (browser) await browser.close(); if (server) server.kill(); });
async function pageFor(t, width = 390, options = {}) {
  const context = await browser.newContext({ viewport: { width, height: 844 }, ...options });
  // Exercise local code without analytics, live forms, or third-party dependencies.
  await context.route('**/*', route => new URL(route.request().url()).origin === base ? route.continue() : route.abort());
  const page = await context.newPage();
  t.after(() => context.close());
  await page.goto(`${base}/index.html`);
  return page;
}
async function expanded(locator, expected) {
  assert.equal(await locator.getAttribute('aria-expanded'), String(expected));
}
for (const width of [360, 390, 430]) {
  test(`mobile ${width}: taps, keyboard, focus, dismissal and resize`, async t => {
    const page = await pageFor(t, width, { isMobile: true, hasTouch: true });
    const hamburger = page.locator('.mobile-menu-toggle');
    const about = page.locator('.nav-dropdown > a').nth(0);
    const services = page.locator('.nav-dropdown > a').nth(1);
    const aboutMenu = page.locator('.dropdown-menu').nth(0);
    await hamburger.tap();
    await about.tap();
    await expanded(about, true);
    assert.equal(await aboutMenu.isVisible(), true);
    await services.tap();
    await expanded(services, true);
    await expanded(about, false);
    assert.equal(await aboutMenu.isVisible(), false);
    await services.press('Escape');
    await expanded(services, false);
    await about.press('ArrowDown');
    assert.equal(await page.locator(':focus').textContent(), 'About Us');
    assert.equal(await aboutMenu.isVisible(), true);
    await page.keyboard.press('End');
    assert.equal(await page.locator(':focus').textContent(), 'FAQ');
    await page.keyboard.press('Escape');
    await expanded(about, false);
    assert.equal(await aboutMenu.isVisible(), false);
    assert.equal(await about.evaluate(el => el === document.activeElement), true);
    await page.keyboard.press('Tab');
    assert.equal(await services.evaluate(el => el === document.activeElement), true);
    await page.keyboard.press('Escape');
    await expanded(hamburger, false);
    assert.equal(await hamburger.evaluate(el => el === document.activeElement), true);
    await hamburger.tap();
    await services.tap();
    await page.locator('h1').tap();
    await expanded(hamburger, false);
    await hamburger.tap();
    await about.tap();
    await page.setViewportSize({ width: 1280, height: 844 });
    await page.waitForFunction(() => document.querySelector('.mobile-menu-toggle').getAttribute('aria-expanded') === 'false');
    await expanded(about, false);
    assert.equal(await page.locator('.main-nav').isVisible(), true);
    await page.setViewportSize({ width, height: 844 });
    await page.waitForFunction(() => document.querySelector('.main-nav').hidden);
    assert.equal(await page.locator('.main-nav').isVisible(), false);
  });
}
test('desktop: hover, pointer traversal, click and keyboard use one state', async t => {
  const page = await pageFor(t, 1366);
  const about = page.locator('.nav-dropdown > a').nth(0);
  const services = page.locator('.nav-dropdown > a').nth(1);
  await about.hover();
  await expanded(about, true);
  await page.getByRole('menuitem', { name: 'FAQ', exact: true }).hover();
  await expanded(about, true);
  await page.mouse.move(10, 800);
  await expanded(about, false);
  await services.click();
  await expanded(services, true);
  await services.press('Escape');
  await expanded(services, false);
  assert.equal(await page.locator('.dropdown-menu').nth(1).isVisible(), false);
  await about.press(' ');
  await expanded(about, true);
  await page.keyboard.press('Escape');
  await about.press('Tab');
  assert.equal(await services.evaluate(el => el === document.activeElement), true);
});
for (const width of [320, 360, 390, 430, 768, 1024, 1366]) {
  test(`journeys at ${width}px: reflow, readable type, early actions and pricing`, async t => {
    const page = await pageFor(t, width);
    const quote = page.locator('.hero-content a[href="quote.html"]');
    assert.equal(await quote.isVisible(), true);
    assert.ok((await quote.boundingBox()).y < 700, 'Quote action should be near the top');
    assert.ok(await page.evaluate(() => parseFloat(getComputedStyle(document.body).fontSize)) >= 16);
    for (const name of ['index.html', 'online-ordering.html', 'pricingservices.html', 'lab-hours.html', 'contact.html', 'quote.html', 'summer.html']) {
      await page.goto(`${base}/${name}`);
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `${name} page overflow`);
      for (const table of await page.locator('.pricing-table').all()) {
        assert.ok(await table.evaluate(el => el.scrollWidth <= el.parentElement.clientWidth + 1), `${name} table needs sideways scrolling`);
      }
    }
    await page.goto(`${base}/online-ordering.html`);
    await page.getByRole('link', { name: 'Start your order', exact: true }).click();
    assert.equal(new URL(page.url()).hash, '#order-form');
    assert.equal(await page.locator('#order-form').isVisible(), true);
    assert.equal(await page.getByRole('link', { name: 'Open order form separately' }).isVisible(), true);
    await page.goto(`${base}/contact.html`);
    assert.equal(await page.getByRole('link', { name: 'uimakerlab@illinois.edu', exact: true }).isVisible(), true);
  });
}
test('nested-page destinations and no-JavaScript navigation fallback', async t => {
  const page = await pageFor(t, 390);
  await page.goto(`${base}/summer/minecraft-3d-printing.html`);
  await page.locator('.mobile-menu-toggle').click();
  await page.locator('.nav-dropdown > a').nth(1).click();
  await page.getByRole('menuitem', { name: 'Services & Pricing', exact: true }).click();
  assert.equal(new URL(page.url()).pathname, '/pricingservices.html');
  const noJs = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 844 } });
  t.after(() => noJs.close());
  await noJs.route('**/*', r => new URL(r.request().url()).origin === base ? r.continue() : r.abort());
  const fallback = await noJs.newPage();
  await fallback.goto(`${base}/index.html`);
  await fallback.locator('.nav-dropdown > a').nth(1).click();
  assert.equal(new URL(fallback.url()).pathname, '/pricingservices.html');
});

test('quote: one $4 order fee for multiple copies across every rate', async t => {
  const page = await pageFor(t, 390);
  // Use the same Three.js version as quote.html, served from a local npm package.
  const three = require('node:fs').readFileSync(process.env.THREE_JS_PATH || require.resolve('three'), 'utf8');
  await page.route('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js', r => r.fulfill({ contentType: 'application/javascript', body: three }));
  await page.goto(`${base}/pricingservices.html`);
  const publishedRates = await page.locator('.pricing-table').first().locator('tbody tr').evaluateAll(rows => rows.map(row => Array.from(row.cells).slice(1).map(cell => parseFloat(cell.textContent) / 100)));
  assert.deepEqual(publishedRates, [[.10, .12], [.25, .30], [.35, .42]]);
  await page.goto(`${base}/quote.html`);
  // A closed 10mm cube, volume 1cm³. Use the actual OBJ parser and upload UI.
  const cube = 'v 0 0 0\nv 10 0 0\nv 10 10 0\nv 0 10 0\nv 0 0 10\nv 10 0 10\nv 10 10 10\nv 0 10 10\nf 1 4 3 2\nf 5 6 7 8\nf 1 2 6 5\nf 4 8 7 3\nf 1 5 8 4\nf 2 3 7 6\n';
  await page.locator('#quote-file-input').setInputFiles({ name: 'cube.obj', mimeType: 'text/plain', buffer: Buffer.from(cube) });
  await page.locator('#quote-interface').waitFor({ state: 'visible' });
  await page.waitForFunction(() => document.querySelector('#quote-total-price').textContent !== '$0.00');
  for (const infill of [20, 100]) {
    await page.locator('#quote-infill').fill(String(infill));
    for (const [orderType, rates] of Object.entries({ walkin: { student: publishedRates[0][0], faculty: publishedRates[1][0], general: publishedRates[2][0], campus: publishedRates[1][0] }, online: { student: publishedRates[0][1], faculty: publishedRates[1][1], general: publishedRates[2][1], campus: publishedRates[1][1] } })) {
      await page.locator(`label:has(input[name="orderType"][value="${orderType}"])`).click();
      for (const [userType, rate] of Object.entries(rates)) {
        await page.locator(`label:has(input[name="userType"][value="${userType}"])`).click();
        for (const quantity of [1, 2, 10, 99]) {
          await page.locator('#quote-quantity').fill(String(quantity));
          const weightPerCopy = 1.24 * (.12 + .88 * infill / 100);
          const expected = '$' + Math.max(userType === 'campus' ? 10 : 0, 4 + weightPerCopy * rate * quantity).toFixed(2);
          assert.equal(await page.locator('#quote-total-price').textContent(), expected, `${quantity} copies, ${userType}/${orderType}, ${infill}% infill`);
        }
      }
    }
  }
});

test('resize keeps keyboard focus on a visible navigation control', async t => {
  const page = await pageFor(t, 390);
  await page.locator('.mobile-menu-toggle').click();
  const about = page.locator('.nav-dropdown > a').nth(0);
  await about.press('ArrowDown');
  await page.setViewportSize({ width: 1280, height: 844 });
  await page.waitForFunction(() => innerWidth === 1280 && !document.querySelector('.nav-dropdown').classList.contains('is-open'));
  assert.equal(await about.evaluate(el => el === document.activeElement), true);
});
