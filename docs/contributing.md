# Contributing to Reveal

Thank you for your interest in contributing to Reveal! This project exists
to improve public safety by helping identify harmful, coded, or anomalous
language in text. Every contribution matters.

There are two ways to contribute -- adding code and adding to word lists.
You do not need to be a developer to contribute meaningfully to Reveal.

---

## Contributing Word Lists (No Coding Required)

The most impactful contributions right now are expansions and validations
of the word lists in the `reveal/dictionaries/` folder. These JSON files
are the foundation of Reveal's harm detection engine.

### Available dictionaries

| File | Purpose |
|------|---------|
| `prop_words.json` | Words associated with propaganda techniques |
| `prop_dict.json` | Propaganda types with example phrases |
| `harm_words.json` | Coded words associated with self-harm |
| `help_words.json` | Words used as calls for help |
| `groom_words.json` | Words used in grooming and predatory behavior |
| `geo_words.json` | Words that may indicate geographic location |

### How to propose new words

1. Fork the repository on GitHub
2. Edit the relevant JSON file in `reveal/dictionaries/`
3. Add your proposed words to the `words` array
4. Include a comment in your pull request explaining:
   - Why you are proposing this word or phrase
   - What source or research supports the addition
   - Any context about when the word is harmful vs innocent
5. Submit the pull request with the label `dictionary-review`

### Important notes on word list contributions

- Some words are not harmful on their own but become signals in context.
  Please include notes explaining this in your pull request.
- Coded language changes rapidly. Recent examples from documented cases,
  law enforcement reports, or academic research are especially valuable.
- If you have expertise in a relevant field (social work, law enforcement,
  child safety, mental health, linguistics) please mention it.
- All proposed additions will be reviewed before merging.

---

## Contributing Code

### Setting up your development environment
```bash
git clone https://github.com/bbplus3/reveal.git
cd reveal
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

### Running the tests
```bash
pytest tests/ -v
```

All 342 tests must pass before submitting a pull request.

### Project structure
```
reveal/
├── reveal/
│   ├── harm/           # Harm detection, sentiment, reporting
│   ├── linguistic/     # Voice, tone, POV analysis
│   ├── cryptanalysis/  # Entropy, n-grams, anomaly detection
│   ├── reasoning/      # Unified scoring and reporting
│   └── dictionaries/   # Word lists (JSON)
├── tests/              # Pytest test suite
└── docs/               # Documentation
```

### Adding a new module

1. Create your module in the appropriate layer folder
2. Follow the existing docstring and commenting style
3. Write tests in `tests/test_yourmodule.py`
4. Aim for at least 20 tests covering edge cases and empty inputs
5. All existing tests must still pass
6. Submit a pull request with a clear description of what the module does

### Code style guidelines

- Use descriptive function and variable names
- Write a docstring for every function explaining parameters and returns
- Handle empty and None inputs gracefully
- Return structured dictionaries from analysis functions
- Keep functions focused on a single responsibility

---

## Submitting a Pull Request

1. Fork the repository
2. Create a branch: `git checkout -b your-feature-name`
3. Make your changes
4. Run the full test suite: `pytest tests/ -v`
5. Commit with a clear message describing what you changed and why
6. Push to your fork and submit a pull request
7. Use one of these labels:
   - `dictionary-review` for word list additions
   - `new-module` for new analysis modules
   - `bug-fix` for bug fixes
   - `enhancement` for improvements to existing modules
   - `good first issue` for small well-defined tasks

---

## Reporting Issues

If you find a bug, have a false positive or false negative to report,
or want to suggest a new feature, please open a GitHub issue at:
https://github.com/bbplus3/reveal/issues

When reporting a bug please include:
- Your Python version
- The text that caused unexpected behavior
- What you expected to happen
- What actually happened

---

## Code of Conduct

Reveal exists to protect people. All contributors are expected to engage
respectfully and professionally. Contributions that undermine the safety
mission of this project will not be accepted.

---

## Questions

If you have questions about contributing, open a GitHub issue with the
label `question` and we will respond as soon as possible.

Thank you for helping make Reveal better.