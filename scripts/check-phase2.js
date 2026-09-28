#!/usr/bin/env node
'use strict';

// Structural checks only. Each member adds their own contribution when ready.
const fs = require('node:fs');
const path = require('node:path');

const MEMBERS = [
  { name: 'Sultan', id: '100065654', file: '01-sultan-financial-schedule-risk.md', required: true },
  { name: 'Zayed', id: '100064657', file: '02-zayed-context-market-operational-legal.md', required: false },
  { name: 'Ghaith', id: '100066185', file: '03-ghaith-technical-data-ai.md', required: false },
];

const mask = text => text.replace(/[^\n]/g, ' ');

function proseOnly(text) {
  const withoutComments = text.replace(/<!--[\s\S]*?-->/g, mask);
  let fence = null;
  return withoutComments.split('\n').map(line => {
    const boundary = line.match(/^\s{0,3}(`{3,}|~{3,})(.*)$/);
    if (fence) {
      if (boundary && boundary[1][0] === fence[0] && boundary[1].length >= fence.length && !boundary[2].trim()) fence = null;
      return mask(line);
    }
    if (boundary) {
      fence = boundary[1];
      return mask(line);
    }
    return line.replace(/(`+)([^`]|(?!\1)`)*?\1/g, mask);
  }).join('\n');
}

function cells(line) {
  const value = line.trim();
  const result = [''];
  for (let i = 0; i < value.length; i++) {
    if (value[i] === '\\' && i + 1 < value.length) {
      result[result.length - 1] += value[i] + value[++i];
    } else if (value[i] === '|') {
      result.push('');
    } else {
      result[result.length - 1] += value[i];
    }
  }
  if (value.startsWith('|')) result.shift();
  if (result[result.length - 1] === '' && value.endsWith('|')) result.pop();
  return result.map(cell => cell.trim());
}

function destination(text, start) {
  let cursor = start;
  while (/\s/.test(text[cursor] || '') && cursor < text.length) cursor++;
  if (text[cursor] === '<') {
    const end = text.indexOf('>', cursor + 1);
    return end < 0 ? '' : text.slice(cursor + 1, end);
  }
  let value = '', depth = 0;
  while (cursor < text.length) {
    const char = text[cursor++];
    if (char === '\\' && cursor < text.length) value += text[cursor++];
    else if (char === '(') { depth++; value += char; }
    else if (char === ')') { if (!depth) break; depth--; value += char; }
    else if (/\s/.test(char) && !depth) break;
    else value += char;
  }
  return value;
}

function markdownLinks(text) {
  const links = [];
  // Check local paths only; external sources are reviewed by people, not fetched.
  for (const match of text.matchAll(/\]\(/g)) links.push({ target: destination(text, match.index + 2), index: match.index });
  for (const match of text.matchAll(/^\s{0,3}\[[^\]\n]+\]:[ \t]*/gm)) links.push({ target: destination(text, match.index + match[0].length), index: match.index });
  return links;
}

function checkMarkdown(file, repoRoot, errors, member) {
  const label = path.relative(repoRoot, file).split(path.sep).join('/');
  const report = (line, message) => errors.push(`${label}:${line}: ${message}`);
  let text;
  try { text = fs.readFileSync(file, 'utf8'); }
  catch (error) { report(1, `Cannot read file: ${error.message}`); return; }
  text.split(/\r?\n/).forEach((line, index) => {
    if (/^(?:<{7}(?:\s.*)?|={7}|>{7}(?:\s.*)?|\|{7}(?:\s.*)?)$/.test(line.trim())) report(index + 1, 'Unresolved Git conflict marker.');
  });

  const prose = proseOnly(text);
  if (member) {
    const studentId = prose.match(/^\s*\*\*Student ID:\*\*\s*(\d+)\s*$/m);
    if (!studentId || studentId[1] !== member.id) report(1, `Expected Student ID ${member.id} for ${member.name}.`);
    const references = new Set();
    for (const match of prose.matchAll(/^\s{0,3}#{1,6}\s+(S\d{2,})\b/gm)) {
      if (references.has(match[1])) report(prose.slice(0, match.index).split('\n').length, `Duplicate reference heading: ${match[1]}.`);
      references.add(match[1]);
    }
    // The member files use bracketed citations such as [S11, S14].
    for (const match of prose.matchAll(/\[((?:S\d{2,})(?:[\s,;]+S\d{2,})*)\]/g)) {
      for (const citation of match[1].matchAll(/S\d{2,}/g)) {
        if (!references.has(citation[0])) report(prose.slice(0, match.index).split('\n').length, `Citation ${citation[0]} has no reference heading in this member's file.`);
      }
    }
  }

  const lines = prose.split(/\r?\n/);
  for (let i = 0; i + 1 < lines.length; i++) {
    const separator = cells(lines[i + 1]);
    if (!lines[i].includes('|') || !separator.length || !separator.every(cell => /^:?-{2,}:?$/.test(cell))) continue;
    const width = cells(lines[i]).length;
    if (separator.length !== width) report(i + 2, `Table separator has ${separator.length} columns; header has ${width}.`);
    i += 2;
    while (i < lines.length && lines[i].trim() && lines[i].includes('|')) {
      const count = cells(lines[i]).length;
      if (count !== width) report(i + 1, `Table row has ${count} columns; header has ${width}.`);
      i++;
    }
    i--;
  }

  for (const { target, index } of markdownLinks(prose)) {
    if (!target || /^(?:[a-z][a-z\d+.-]*:|#|\/\/)/i.test(target)) continue;
    const line = prose.slice(0, index).split('\n').length;
    let local;
    try { local = decodeURIComponent(target.split(/[?#]/)[0]); }
    catch { report(line, `Invalid URL encoding in relative link: ${target}`); continue; }
    if (!local) continue;
    const resolved = local.startsWith('/')
      ? path.resolve(repoRoot, local.slice(1))
      : path.resolve(path.dirname(file), local);
    const relative = path.relative(repoRoot, resolved);
    if (relative === '..' || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) report(line, `Relative link leaves the repository: ${target}`);
    else if (!fs.existsSync(resolved)) report(line, `Broken relative link: ${target}`);
  }
}

function checkPhase2(repoRoot, { requireAll = false } = {}) {
  const root = path.resolve(repoRoot);
  const phase = path.join(root, 'docs', 'phase2');
  const sections = path.join(phase, 'sections');
  const errors = [], checked = [], awaiting = [];
  for (const member of MEMBERS) {
    const file = path.join(sections, member.file);
    if (!fs.existsSync(file)) {
      awaiting.push(member.name);
      if (requireAll) errors.push(`docs/phase2/sections/${member.file}: ${member.name}'s source file is required before integration into main.`);
      else if (member.required) errors.push(`docs/phase2/sections/${member.file}: Sultan's source file is required for this integration baseline.`);
      continue;
    }
    const before = errors.length;
    checkMarkdown(file, root, errors, member);
    if (errors.length === before) checked.push(member.name);
  }

  const calculationFile = path.join(phase, 'evidence-and-calculations.json');
  try {
    JSON.parse(fs.readFileSync(calculationFile, 'utf8'), (key, value) => {
      if (typeof value === 'number' && !Number.isFinite(value)) throw new Error(`Non-finite number at ${key || 'root'}`);
      return value;
    });
  } catch (error) {
    errors.push(`docs/phase2/evidence-and-calculations.json: Cannot read valid calculation input: ${error.message}`);
  }
  return { errors, checked, awaiting };
}

if (require.main === module) {
  const requireAll = process.argv.includes('--require-all');
  const { errors, checked, awaiting } = checkPhase2(path.join(__dirname, '..'), { requireAll });
  console.log(`Member structural checks complete: ${checked.join(', ') || 'none'}.`);
  if (awaiting.length) console.log(`Awaiting member contributions: ${awaiting.join(', ')}. ${requireAll ? 'All three members must contribute before integration into main.' : 'Other members may contribute in later PRs.'}`);
  if (errors.length) {
    console.error(`Phase 2 document checks failed (${errors.length}):\n${errors.map(error => `- ${error}`).join('\n')}`);
    process.exitCode = 1;
  } else {
    console.log('Phase 2 document checks passed. Evidence accuracy, real peer review and final document layout remain human checks.');
  }
}

module.exports = { checkPhase2, cells, markdownLinks, proseOnly, MEMBERS };
