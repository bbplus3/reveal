# Reveal

An open-source Python library for intelligent harm detection and linguistic analysis in text.

Reveal combines Natural Language Processing, linguistic analysis, and cryptanalysis to identify harmful, coded, or anomalous language in text — helping researchers, platform moderators, and public safety professionals surface signals that standard tools miss.

## What Reveal Detects

- Propaganda and persuasion techniques (22 categories)
- Grooming and predatory language
- Self-harm coded language
- Help signals from victims of abuse or bullying
- Geographic location indicators
- Emotional distress and sentiment
- Manipulative and accusatory tone
- Passive voice and agency obscuring
- Point of view shifts
- Shannon entropy anomalies
- Unusual n-gram sequences
- Statistically anomalous words

## Installation
```bash
pip install reveal-nlp
```

## Quick Start
```python
from reveal.reasoning.reporter import analyze

text = "I feel so alone and trapped. Please someone help me."
result = analyze(text, fmt='text')
print(result)
```

## Output formats
```python
# Dictionary output for programmatic use
result = analyze(text)

# Formatted text report for human reading
result = analyze(text, fmt='text')
```

## Project Structure
```
reveal/
├── harm/           # Harm detection, sentiment, reporting
├── linguistic/     # Voice, tone, POV analysis
├── cryptanalysis/  # Entropy, n-grams, anomaly detection
├── reasoning/      # Unified scoring and reporting
└── dictionaries/   # Word lists (JSON, community editable)
```

## Contributing

Reveal is open source and actively seeking contributors — especially for expanding and validating the word lists in the `dictionaries/` folder. No coding required to contribute word lists.

See `docs/contributing.md` for guidelines.

## License

MIT License. See `LICENSE` for details.

## Disclaimer

Reveal is a research and analysis tool. Word lists require ongoing community validation. Results should be interpreted by qualified professionals in appropriate contexts.
```
