// Exercise the shipped composer's actual event bindings without a browser or network.
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const {runInNewContext} = require('node:vm');
const source = readFileSync(process.env.COMPANION_JS || 'src/synth/companion/static/app.js','utf8');
const sent = [];
const nodes = {
  message: {value:'What is the monthly fee?', addEventListener(name,handler){this[name]=handler}},
  send: {disabled:false},
  composer: {requestSubmit(){this.onsubmit({preventDefault(){}})}}
};
runInNewContext(source.slice(source.indexOf("$('composer').onsubmit"),source.indexOf("$('new').onclick")),{
  $: id=>nodes[id], send: text=>sent.push(text), updateControls(){}
});
function key(options={}) {
  let prevented=false;
  nodes.message.keydown?.({key:'Enter',shiftKey:false,isComposing:false,keyCode:13,repeat:false,
    preventDefault(){prevented=true},...options});
  return prevented;
}
assert.equal(key(),true,'Enter must prevent a newline and submit');
assert.deepEqual(sent,['What is the monthly fee?']);
for (const options of [{shiftKey:true},{isComposing:true},{keyCode:229},{key:'a'}]) {
  assert.equal(key(options),false,'Multiline, composition and ordinary typing remain native');
}
assert.equal(sent.length,1);
key({repeat:true});
assert.equal(sent.length,1,'Holding Enter must not repeat submissions');
nodes.send.disabled=true;
key();
assert.equal(sent.length,1,'Unavailable or empty composer must not submit');
nodes.send.disabled=false;
nodes.message.value='Line one\nLine two';
nodes.composer.requestSubmit();
assert.equal(sent.at(-1),'Line one\nLine two','Button/form path retains multiline content');
assert.ok(source.includes("element('p','Thinking…','pending-inline')"));
assert.ok(!source.includes('Retrieving the managed production prompt'));
console.log('Composer passed: Enter, Shift+Enter, IME, repeats, disabled state, form submission and Thinking copy.');
