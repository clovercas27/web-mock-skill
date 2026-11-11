"""Behavior checks for source extraction, using synthetic source only."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'plugins/web-mock-skill/skills/website-prospect-kit/scripts/inspect_source.py'
spec = importlib.util.spec_from_file_location('source_inventory', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SourceInventoryTests(unittest.TestCase):
    def parse(self, html):
        p = module.SourceInventory('https://example.com/shop/')
        p.feed(html)
        p.close()
        return p.result()

    def test_assets_resolve_and_high_resolution_candidates_survive(self):
        result = self.parse('<img src="/tiny.jpg?width=20" data-src="//cdn.example.com/full.jpg" '
                            'srcset="small.jpg 320w, large.jpg 1600w" alt="A real product">')
        image = result['images'][0]
        self.assertEqual(image['alt'], 'A real product')
        self.assertIn({'attribute': 'srcset', 'url': 'https://example.com/shop/large.jpg',
                       'descriptor': '1600w'}, image['candidates'])
        self.assertEqual(image['candidates'][1]['url'], 'https://cdn.example.com/full.jpg')

    def test_does_not_emit_active_schemes_or_credentials(self):
        result = self.parse('<img src="javascript:alert(1)"><a href="data:text/html,test">x</a>'
                            '<a href="https://user:secret@example.com/">private</a>')
        self.assertEqual(result['links'], [])
        self.assertEqual(result['images'][0]['candidates'], [])

    def test_nested_heading_text_and_metadata(self):
        result = self.parse('<title>Example &amp; Co</title><h1>Find <em>your</em> fit</h1>'
                            '<meta name="description" content="An actual description">'
                            '<link rel="canonical" href="/products/example">')
        self.assertEqual(result['title'], 'Example & Co')
        self.assertEqual(result['headings'][0]['text'], 'Find your fit')
        self.assertEqual(result['meta']['description'], 'An actual description')
        self.assertEqual(result['canonical'], ['https://example.com/products/example'])

    def test_jsonld_types_without_copying_raw_records(self):
        result = self.parse('<script type="application/ld+json">'
                            '{"@graph":[{"@type":"Product","private":"do not copy"},'
                            '{"@type":["Organization","Brand"]}]}</script>')
        self.assertEqual(result['structured_data_types'][0]['types'], ['Brand', 'Organization', 'Product'])
        self.assertNotIn('do not copy', str(result))

    def test_invalid_jsonld_reports_limitation(self):
        result = self.parse('<script type="application/ld+json">not json</script>')
        self.assertEqual(len(result['warnings']), 1)

    def test_script_content_is_not_page_text_or_palette(self):
        result = self.parse('<script>document.write("<h1>Fake</h1>");var color="#fff";</script>'
                            '<style>body{color:#152547}</style><h2 style="color:#007e83">Real</h2>')
        self.assertEqual([h['text'] for h in result['headings']], ['Real'])
        self.assertNotIn('#fff', result['inline_css_hex_colors'])
        self.assertEqual(result['inline_css_hex_colors']['#152547'], 1)

    def test_reads_utf16_attachment(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'source.txt'
            path.write_text('<h1>Brand name</h1>', encoding='utf-16')
            self.assertEqual(module.inspect(path, 'https://example.com')['headings'][0]['text'], 'Brand name')


if __name__ == '__main__':
    unittest.main()
