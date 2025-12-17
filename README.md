# DataAnalysis

A comprehensive tool for analyzing dense PDF documents (+150 pages). Extract text, perform statistical analysis, identify key sections, and generate detailed reports from your PDF files.

## Features

- **Text Extraction**: Extract all text content from PDF files
- **Statistical Analysis**: Get detailed statistics including word count, sentence count, character count, and more
- **Keyword Analysis**: Identify the most frequently used words (excluding common stop words)
- **Document Structure**: Automatically identify key sections like Introduction, Methodology, Results, Conclusion, etc.
- **Numerical Data Extraction**: Find numbers, dates, and years mentioned in the document
- **Comprehensive Reports**: Generate detailed analysis reports
- **Export Options**: Save extracted text and analysis reports to files

## Requirements

- Python 3.6 or higher
- PyPDF2 library

## Installation

1. Clone this repository:
```bash
git clone https://github.com/zzruanxx/DataAnalysis.git
cd DataAnalysis
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Or install PyPDF2 directly:
```bash
pip install PyPDF2
```

## Usage

### Basic Usage

Analyze a PDF file and display the report in the console:

```bash
python pdf_analyzer.py your_document.pdf
```

### Save Analysis Report

Save the analysis report to a text file:

```bash
python pdf_analyzer.py your_document.pdf --output analysis_report.txt
```

### Extract Text Content

Extract and save all text content from the PDF:

```bash
python pdf_analyzer.py your_document.pdf --extract-text extracted_text.txt
```

### Complete Analysis with All Outputs

Generate both the analysis report and extracted text:

```bash
python pdf_analyzer.py your_document.pdf --output report.txt --extract-text text.txt
```

## Analysis Report Contents

The tool generates a comprehensive report including:

### 1. Content Statistics
- Total words, unique words, characters
- Estimated sentence and paragraph counts
- Average word and sentence length

### 2. Top Keywords
- 30 most frequently used meaningful words
- Common stop words are automatically filtered out
- Helps identify main topics and themes

### 3. Document Structure
- Automatically identifies common sections:
  - Introduction/Overview/Abstract
  - Methodology/Approach
  - Results/Findings
  - Conclusion/Summary
  - References/Bibliography
  - Acknowledgments

### 4. Numerical Data
- Count of numbers and dates found
- Years mentioned in the document

### 5. Text Preview
- First 500 characters of the extracted text

## Example Output

```
================================================================================
PDF ANALYSIS REPORT
================================================================================

Document: research_paper.pdf
Location: /path/to/research_paper.pdf
Total Pages: 157

--------------------------------------------------------------------------------
CONTENT STATISTICS
--------------------------------------------------------------------------------
Total Words: 45,234
Unique Words: 8,901
Total Characters: 289,456
Characters (no spaces): 245,678
Estimated Sentences: 2,103
Estimated Paragraphs: 567
Average Word Length: 5.42 characters
Average Sentence Length: 21.51 words

--------------------------------------------------------------------------------
TOP 30 KEYWORDS (excluding common words)
--------------------------------------------------------------------------------
 1. research            -  234 occurrences
 2. data                -  198 occurrences
 3. analysis            -  176 occurrences
...
```

## Use Cases

- **Academic Research**: Analyze research papers, theses, and dissertations
- **Legal Documents**: Review contracts, legal briefs, and case files
- **Business Reports**: Analyze annual reports, white papers, and market research
- **Technical Documentation**: Review manuals, specifications, and technical guides
- **Book Analysis**: Study textbooks, reference materials, and literature

## Troubleshooting

### "No text could be extracted"
- The PDF might be image-based (scanned document). Consider using OCR tools first.
- The PDF might be encrypted or password-protected.

### "PyPDF2 not installed"
- Run: `pip install PyPDF2`

### Permission Errors
- Ensure you have read permissions for the PDF file
- Check that the output directory is writable

## Advanced Usage

### Programmatic Usage

You can also import and use the analyzer in your own Python scripts:

```python
from pdf_analyzer import extract_text_from_pdf, analyze_text

# Extract text
text, pages = extract_text_from_pdf('document.pdf')

# Analyze text
analysis = analyze_text(text)

# Access results
print(f"Word count: {analysis['word_count']}")
print(f"Top words: {analysis['top_words'][:10]}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.