# dgcaio (DGC-All-In-One)
DGC-All-In-One: Most Customizable Package Installer

## dgcaio Repository File
```
{
  "last-updated": "0000000000000000000000001011100111111101000001010010001110010001",
  "packages": [
    {
      "id": "spaudio",
      "name": "Spaudio",
      "description": "Spatial Audio Simulation Tool",
      "default_version": "1.0",
      "alias": {"latest": "1.0"},
      "versions": {
        "1.0": {
          "download": "https.get.save(\"https://github.com/DiamondGotCat/Spaudio/archive/refs/heads/main.zip\", \"spaudio.zip\")\nexec.py(\"\"\"from zipfile import ZipFile\nwith ZipFile('spaudio.zip') as zf:\n    zf.extractall()\"\"\")"
        }
      }
    }
  ]
}
```

- `last-updated`: [DGC-Epoch](https://github.com/DiamondGotCat/DGC-Epoch) Time of Last Updated
- `packages`: All Packages
  - `id`: Package ID
  - `name`: Package Name (Currently Not Supported)
  - `description`: Package Description (Currently Not Supported)
  - `default_version`: Default Version of Package
  - `alias`: Alias of Version (Currently Not Supported)
  - `versions`: Versions and Actions
    - `1.0`: Version
      - `download`: Action ID
      - `https.get.save(\"htt...`: [Pylo](https://github.com/DiamondGotCat/Pylo) Script
