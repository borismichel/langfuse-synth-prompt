// Offline safety regression for the browser renderer; no requests or browser state.
const {readFileSync} = require('node:fs');
const {runInNewContext} = require('node:vm');
const assert = require('node:assert/strict');
class Node {
  constructor(tag, text = '') { this.tag = tag; this.children = []; this.value = text; }
  set textContent(text) { this.value = text; this.children = []; }
  get textContent() { return this.value + this.children.map(child => child.textContent).join(''); }
  set innerHTML(_) { throw new Error('HTML parsing is forbidden'); }
  append(...children) { this.children.push(...children); }
}
const context = {
  document: {body: {dataset: {}}, createElement: tag => new Node(tag), createTextNode: text => new Node('#text', text)},
  location: {search: ''}, URLSearchParams,
};
const source = readFileSync(new URL('../src/synth/companion/static/app.js', `file://${__filename}`), 'utf8');
runInNewContext(source.slice(0, source.indexOf('async function api')), context);
const render = context.replyContent;
const all = node => [node, ...node.children.flatMap(all)];
const sample = '## Withdrawal Fee Explanation\n\n| Withdrawals | Status |\n|---|---|\n| 1st withdrawal | Included |\n\n**Fee: €1.50**\n\n---\n\n- Separate from monthly fee.\n- Resets each month.';
const result = render(sample);
assert.deepEqual(result.children.map(node => node.tag), ['h3', 'div', 'p', 'hr', 'ul']);
assert.deepEqual(all(result).filter(node => node.tag === 'th').map(node => node.textContent), ['Withdrawals', 'Status']);
assert.deepEqual(all(result).filter(node => node.tag === 'td').map(node => node.textContent), ['1st withdrawal', 'Included']);
assert.equal(all(result).find(node => node.tag === 'strong').textContent, 'Fee: €1.50');
assert.equal(all(result).filter(node => node.tag === 'li').length, 2);
assert.deepEqual(render('First line\nSecond line\n\nThird paragraph').children.map(node => node.textContent), ['First line\nSecond line', 'Third paragraph']);
assert.equal(render('First\r\nSecond').children[0].textContent, 'First\nSecond');
assert.equal(render('#### Detail').children[0].tag, 'h4');
assert.deepEqual(render('3. Third\n5. Fifth').children[0].children.map(node => node.value), [3, 5]);
assert.deepEqual(render('`<script>` and **bold**').children[0].children.filter(node => node.tag !== '#text').map(node => node.tag), ['code', 'strong']);
const hostile = render('## <img src=x onerror=alert(1)>\n\n| Name | Value |\n|---|---|\n| **<script>alert(1)</script>** | [click](javascript:alert(1)) |\n\n- <svg onload=alert(1)>\n\n`<iframe>`');
const allowed = new Set(['#text', 'div', 'p', 'h3', 'h4', 'ul', 'ol', 'li', 'strong', 'code', 'hr', 'table', 'thead', 'tbody', 'tr', 'th', 'td']);
assert.ok(all(hostile).every(node => allowed.has(node.tag)));
for (const text of ['<img src=x onerror=alert(1)>', '<script>alert(1)</script>', '[click](javascript:alert(1))', '<svg onload=alert(1)>', '<iframe>']) assert.ok(hostile.textContent.includes(text));
for (const malformed of ['| A | B |\n|---|\n| one | two |', '| A | B |\n|oops|---|']) {
  const output = render(malformed);
  assert.equal(output.textContent, malformed);
  assert.ok(all(output).every(node => node.tag !== 'table'));
}
const malformedRow = render('| A | B |\n|---|---|\n| one | two | three |');
assert.equal(malformedRow.children[1].textContent, '| one | two | three |');
assert.equal(render('An unmatched **marker').textContent, 'An unmatched **marker');
assert.equal(context.element('p', '**user text**').textContent, '**user text**');
assert.equal(render('reply', 'error-message').className, 'reply-content error-message');
console.log('Reply renderer checks passed: blocks, newlines, inert HTML/links, malformed tables, plaintext user content.');
