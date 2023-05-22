from presets import manifest

positive_manifest = manifest
duplication_manifest = manifest
no_manifest = manifest

positive_manifest.load("tests/manifest.positive.yaml")
duplication_manifest.load("manifest.urlduplication.yaml")
no_manifest.load("tests/manifest.nofile.yaml")

def test_file_parcer():
    assert positive_manifest.Config.use_presets

def test_router_generator():
    router = positive_manifest.generate_router()
    assert len(router.routes) == 2

def test_url_duplication():
    assert duplication_manifest.validate_presets() == False

def test_file_not_found():
    assert no_manifest.Config.use_presets == False