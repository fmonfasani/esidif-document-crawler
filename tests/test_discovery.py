from esidif_crawler.discovery import extract_links, looks_like_document, normalize_url


def test_normalize_url():
    assert normalize_url("https://example.com/a/", "../b") == "https://example.com/b"

def test_document_detection():
    assert looks_like_document("https://example.com/x/manual.PDF", [".pdf"])
    assert not looks_like_document("https://example.com/x/page", [".pdf"])

def test_extract_links():
    html='<html><a href="/e-sidif/manual.pdf">Descargar</a><a href="/e-sidif/presupuesto">Presupuesto</a></html>'
    links=extract_links(html,"https://www.argentina.gob.ar/economia/sechacienda/dgsiaf/e-sidif/",1,[".pdf"])
    assert len(links)==2 and links[0].is_document
