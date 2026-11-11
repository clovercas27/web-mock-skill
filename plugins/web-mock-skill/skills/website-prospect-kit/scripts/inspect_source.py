#!/usr/bin/env python3
"""Inventory supplied HTML without fetching resources or executing page scripts."""
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit


class SourceInventory(HTMLParser):
    def __init__(self, base_url):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.page_title = []
        self.meta = {}
        self.canonical = []
        self.headings = []
        self.images = []
        self.links = []
        self.stylesheets = []
        self.fonts = []
        self.script_sources = []
        self.structured_data = []
        self.warnings = []
        self.colors = Counter()
        self._title = False
        self._heading = None
        self._style = False
        self._script = None

    def safe_url(self, value):
        value = (value or '').strip()
        if not value or len(value) > 5000:
            return None
        try:
            resolved = urljoin(self.base_url, value)
            parsed = urlsplit(resolved)
            if parsed.scheme not in ('http', 'https') or not parsed.netloc:
                return None
            if parsed.username or parsed.password:
                return None
            return resolved
        except ValueError:
            return None

    def add_colors(self, text):
        self.colors.update(c.lower() for c in re.findall(
            r'#[0-9a-fA-F]{8}\b|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{4}\b|#[0-9a-fA-F]{3}\b', text))

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        line = self.getpos()[0]
        if self._script is not None:
            return
        if tag == 'title':
            self._title = True
        elif re.fullmatch(r'h[1-6]', tag):
            self._heading = {'level': int(tag[1]), 'text': '', 'line': line}
        elif tag == 'meta':
            key = (d.get('name') or d.get('property') or '').lower()
            if key in ('description', 'robots', 'googlebot', 'theme-color',
                       'og:title', 'og:description', 'og:image', 'twitter:card'):
                self.meta[key] = (d.get('content') or '')[:1000]
        elif tag == 'link':
            url = self.safe_url(d.get('href'))
            rel = (d.get('rel') or '').lower().split()
            if url and 'canonical' in rel:
                self.canonical.append(url)
            if url and 'stylesheet' in rel:
                self.stylesheets.append(url)
            if url and d.get('as') == 'font':
                self.fonts.append(url)
        elif tag == 'img':
            candidates = []
            for key in ('src', 'data-src', 'data-original'):
                url = self.safe_url(d.get(key))
                if url:
                    candidates.append({'attribute': key, 'url': url})
            for key in ('srcset', 'data-srcset'):
                for item in (d.get(key) or '').split(','):
                    parts = item.strip().split()
                    if parts:
                        url = self.safe_url(parts[0])
                        if url:
                            candidates.append({'attribute': key, 'url': url,
                                               'descriptor': ' '.join(parts[1:])})
            self.images.append({'alt': d.get('alt'), 'width': d.get('width'),
                                'height': d.get('height'), 'line': line,
                                'candidates': candidates})
        elif tag == 'a':
            url = self.safe_url(d.get('href'))
            if url:
                self.links.append({'url': url, 'line': line})
        elif tag == 'script':
            url = self.safe_url(d.get('src'))
            if url:
                self.script_sources.append(url)
            self._script = {'jsonld': (d.get('type') or '').lower() == 'application/ld+json',
                            'text': [], 'line': line}
        elif tag == 'style':
            self._style = True
        if d.get('style'):
            self.add_colors(d['style'])

    def handle_data(self, text):
        if self._script is not None:
            if self._script['jsonld']:
                self._script['text'].append(text)
            return
        if self._style:
            self.add_colors(text)
        if self._title:
            self.page_title.append(text)
        if self._heading is not None:
            self._heading['text'] += text

    def handle_endtag(self, tag):
        if self._script is not None:
            if tag == 'script':
                if self._script['jsonld']:
                    try:
                        value = json.loads(''.join(self._script['text']))
                        types = set()
                        def visit(node):
                            if isinstance(node, dict):
                                t = node.get('@type', [])
                                types.update([t] if isinstance(t, str) else
                                             [v for v in t if isinstance(v, str)] if isinstance(t, list) else [])
                                for child in node.values():
                                    visit(child)
                            elif isinstance(node, list):
                                for child in node:
                                    visit(child)
                        visit(value)
                        self.structured_data.append({'line': self._script['line'],
                                                     'types': sorted(types)})
                    except (ValueError, RecursionError):
                        self.warnings.append('Unparseable JSON-LD at line ' + str(self._script['line']))
                self._script = None
            return
        if tag == 'title':
            self._title = False
        elif re.fullmatch(r'h[1-6]', tag) and self._heading is not None:
            self._heading['text'] = ' '.join(self._heading['text'].split())[:1000]
            self.headings.append(self._heading)
            self._heading = None
        elif tag == 'style':
            self._style = False

    def result(self):
        return {
            'base_url': self.base_url,
            'scope': 'Supplied HTML only; no requests, rendering, performance or indexing tests.',
            'title': ' '.join(''.join(self.page_title).split())[:1000],
            'meta': self.meta, 'canonical': self.canonical,
            'headings': self.headings, 'images': self.images,
            'links': self.links, 'stylesheets': self.stylesheets,
            'font_preloads': self.fonts, 'script_sources': self.script_sources,
            'inline_css_hex_colors': dict(self.colors.most_common(24)),
            'structured_data_types': self.structured_data,
            'warnings': self.warnings,
        }


def inspect(path, base_url):
    raw = Path(path).read_bytes()
    encoding = 'utf-16' if raw.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8-sig'
    parser = SourceInventory(base_url)
    parser.feed(raw.decode(encoding, errors='replace'))
    parser.close()
    return parser.result()


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('source', type=Path)
    cli.add_argument('--base-url', required=True)
    cli.add_argument('--out', type=Path)
    args = cli.parse_args()
    parsed = urlsplit(args.base_url)
    if parsed.scheme not in ('http', 'https') or not parsed.netloc or parsed.username or parsed.password:
        cli.error('--base-url must be an HTTP(S) URL without credentials')
    try:
        result = json.dumps(inspect(args.source, args.base_url), indent=2, ensure_ascii=False)
    except OSError as exc:
        cli.error(str(exc))
    if args.out:
        args.out.write_text(result + '\n', encoding='utf-8')
    else:
        print(result)


if __name__ == '__main__':
    main()
