# MSWord‑Dictionary‑Extraction

A Python utility that parses the **Bailis** Syriac lexical database (Lift/XML format), extracts lexemes and definitions, and writes them to a Lift XML file suitable for importing into language‑learning tools.

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Key Scripts](#key-scripts)  
   - `convert.py` – Core processing pipeline  
   - `utils.py` – Helper functions  
3. [How `convert.py` Works](#how-convertpy-works)  
4. [Running the Extraction](#running-the-extraction)  
5. [Creating & Pushing a GitHub Remote](#creating--pushing-a-github-remote)  
6. [Dependencies](#dependencies)  
7. [License & Credits](#license--credits)

---

### Project Overview

The repository contains a small pipeline that:

1. **Parses** a Bailis Lift/XML dictionary (`BailisFullDictionary.lift`).  
2. **Extracts** each lexical entry, splits the Syriac string into “outside parts” (the visible word) and “inside elements” (morphological markers in parentheses).  
3. **Creates** a new Lift `<entry>` element for each lexeme using the `entry()` helper.  
4. **Writes** the generated entries to `./data/output.lift`.

The resulting file can be imported into tools such as **FieldWorks Language Explorer** or **Lexique Pro**.

---

## Key Scripts

| File | Purpose |
|------|---------|
| `convert.py` | Main driver: reads the source Lift file, builds a dictionary of arguments for each entry, selects the correct part‑of‑speech processor, and calls `entry()` for every lexeme. |
| `utils.py`   | Utility functions: UUID generation, timestamping, XML building (`entry()`), file‑writing (`write_entry_tofile()`), and text‑processing helpers (`remove_parentheses`, `extract_outside_and_inside`, etc.). |
| `to_flex.py` | Pluggable driver-based converter: transforms CSV dictionary data into well-formed FLEX/LIFT XML. |
| `collect_dups.py` | (Not covered here) – utilities for detecting duplicate entries. |
| `extract_text.py` | (Not covered here) – helper for extracting plain text from Word documents. |

---

## How `convert.py` Works

```python
def NP_Processor(x):
    print("NP Processor")
    print(x)
    en_definition = x["entry"]
    pos = x["pos"]
    trait_name = x["trait"]["name"]
    trait_value = x["trait"]["value"]
    sem_domain = x["sem_domain"]
    bib = "bailis"

    lexemes = x["lexemes"]               # list of JSON strings
    for item in lexemes:
        aii_lexeme = json.loads(item)["outside_parts"][0].strip()
        xx, my_tree = entry(
            aii_lexeme,
            en_definition,
            pos,
            bib,
            morph_type=trait_value,
            sem_domain=sem_domain,
        )
        write_entry_tofile(my_tree, file_path)
```

* **Input (`x`)** – a dictionary built in `parser()` containing the English definition, part‑of‑speech, trait info, semantic domain, and a list of lexeme JSON objects.
* **Processing** – for each lexeme it:
  1. Retrieves the Syriac word (`outside_parts[0]`).  
  2. Calls `entry()` (from `utils.py`) to create a full Lift `<entry>` XML element.  
  3. Appends the entry to `file_path` (`./data/output.lift`).

The `parser()` function iterates over every `<entry>` in the source Lift file, extracts the necessary fields, builds the `arg` dictionary, selects the appropriate processor (`NP_Processor`, `VP_Processor`, etc.) via `POS_Processor`, and finally calls `apply_function(arg)`.

---

## Running the Extraction

1. **Install dependencies** (run from the project root):

   ```bash
   pip install -r requirements.txt   # if a requirements file exists
   # otherwise you need at least: lxml, python-docx
   ```

2. **Execute the script**:

   ```bash
   python bailis-extraction/convert.py
   ```

   This will read `./data/BailisFullDictionary.lift` and produce `./data/output.lift`.

---

## CSV to LIFT Conversion (to_flex.py)

Convert CSV dictionary data into FLEX/LIFT XML format using pluggable drivers.

### Features

- **Pluggable drivers**: Abstract `InputDriver` + concrete implementations (e.g., `GADriver` for Giwargiz Aghassi CSV)
- **Pretty-printed output**: Generates a single well-formed XML document with `<dictionary>` wrapper and XML declaration
- **Raw mode**: Optional line-by-line entry output for streaming
- **CLI**: Command-line options for driver selection, input/output paths

### Usage

#### Default: Pretty-printed XML

```bash
python to_flex.py -d ga -i "data/Giwargiz Aghassi Small Dictionary.csv" -o data/output.lift
```

This produces a single file `data/output.lift` with all entries wrapped in `<dictionary>` and proper XML declaration.

#### Raw entries (line-delimited)

```bash
python to_flex.py -d ga -i "data/Giwargiz Aghassi Small Dictionary.csv" -o data/raw_entries.txt --raw
```

One XML entry per line (no wrapper, no declaration).

#### Show help

```bash
python to_flex.py --help
```

### Command-Line Options

- `--driver/-d {ga}`: Input driver type (default: `ga` = Giwargiz Aghassi CSV)
- `--input/-i PATH`: Input file path (default: `data/Giwargiz Aghassi Small Dictionary.csv`)
- `--output/-o PATH`: Output XML file path (default: `data/output.lift`)
- `--raw`: Write raw entries one-per-line instead of a single pretty XML document

### Adding a New Driver

1. Subclass `InputDriver`
2. Implement `generate_entries()` to yield `(xml_string, ElementTree)` tuples
3. Register in `main()` and add to `--driver` choices

#### Example

```python
class MyDriver(InputDriver):
    def __init__(self, input_path: str):
        self.input_path = input_path

    def generate_entries(self) -> Iterator[Tuple[str, object]]:
        # Read from input_path, yield entries
        for lexeme, definition in my_source():
            xml_string, tree = utils.entry(lexeme, definition, "noun", "source")
            yield xml_string, tree
```

Then update `main()`:

```python
if args.driver == "ga":
    driver = GADriver(args.input)
elif args.driver == "my":
    driver = MyDriver(args.input)
```

### Entry Format

All entries are created using `bailis_extraction.utils.entry()`, which generates FLEX/LIFT XML with:

- `<lexical-unit>` containing the Assyrian form
- `<sense>` with grammatical info, definition, and reversal
- `<note type="bibliography">` with source attribution

### Output Examples

#### Pretty XML (default)

```xml
<?xml version="1.0" encoding="utf-8"?>
<dictionary>
  <entry id="..." guid="..." dateCreated="..." dateModified="...">
    <lexical-unit>
      <form lang="aii">
        <text>ܠܦܝܦܐ</text>
      </form>
    </lexical-unit>
    <sense id="..." order="0">
      <grammatical-info value="noun"/>
      <definition>
        <form lang="en">
          <text>Example Word</text>
        </form>
      </definition>
      <reversal type="en">...</reversal>
      <note type="bibliography">...</note>
    </sense>
  </entry>
  <!-- more entries -->
</dictionary>
```

#### Raw entries (--raw)

One compact XML entry per line (suitable for streaming/piping).

---

## Creating & Pushing a GitHub Remote

If you don’t already have a remote repository:

1. **Create a new repo on GitHub** – go to GitHub, click **+ → New repository**, give it a name (e.g., `MSWord-Dictionary-Extraction`), and click **Create repository**. Copy the URL that GitHub shows, e.g.:

   ```
   https://github.com/your‑username/MSWord-Dictionary-Extraction.git
   ```

2. **Add the remote to your local repo** (run in the project root):

   ```bash
   git remote add origin https://github.com/your-username/MSWord-Dictionary-Extraction.git
   ```

3. **Push the current branch** (usually `main`):

   ```bash
   git push -u origin main
   ```

   Use `master` instead of `main` if that’s the name of your default branch.

4. **Future pushes** can be done simply with:

   ```bash
   git push
   ```

> **Note:** GitHub now requires a Personal Access Token (PAT) for authentication. Generate one in *GitHub → Settings → Developer settings → Personal access tokens* (grant `repo` scope) and use it when prompted for a password.

---

## Dependencies

- **Python 3.11+**
- `xml.etree.ElementTree` (standard library)
- `lxml` – for pretty‑printing XML (optional)
- `python-docx` – used elsewhere in the project for reading `.docx` files
- `re`, `json`, `uuid`, `datetime` – standard library modules

---

## License & Credits

This project is derived from the **Bailis Syriac dictionary** extraction scripts originally authored by the Bailis research team. The code here is released under the MIT License. See the `LICENSE` file for full terms.

---

*Happy extracting!*
