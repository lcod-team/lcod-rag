## registry.load_manifest_records (0.1.0)

Resolve the absolute path of a registry manifest (typically exported from `lcod-components`) and parse it as a JSON array. The component first tries to download `metadata.manifestUrl` (or `manifestUrl` in the state) and falls back to a local lookup driven by `manifestPath`, `sourceRepo`, and the optional `repoRoots` mapping. It returns the parsed records along with non-fatal warnings when the manifest cannot be obtained or parsed.
