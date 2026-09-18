from pathlib import Path
import zipfile, yaml
root=Path('/mnt/data/source-code-reading-skill-v0.5')
files=list(root.rglob('*'))
print('files', sum(p.is_file() for p in files))
print('lines', sum(sum(1 for _ in p.open(errors='ignore')) for p in files if p.is_file()))
with zipfile.ZipFile('/mnt/data/source-code-reading-skill-v0.5.zip') as z:
    bad=z.testzip()
    print('zip_test', bad)
print('size', Path('/mnt/data/source-code-reading-skill-v0.5.zip').stat().st_size)
