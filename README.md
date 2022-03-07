# Tools for generating LaTeX files from metadata

The main goal of this tool is to be able to easily produce latex files using different classes for submission of a paper to various conferences/journals. Mainly, I am targeting journals and conferences in theoretical computer science and mathematics.  Currently supported LaTeX classes are:

- `acmart`
- `lipics`
- `amsart`

## Usage

Everything is work in progress. I will soon provide an example metadata file. The command is run as

```
python3 thead.py -c (acmart|lipics|amsart) [-o outfile.tex] infile.yaml
```