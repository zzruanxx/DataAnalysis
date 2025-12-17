# Quick Start Guide

Get started with PDF analysis in under 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Analyze Your PDF

Place your PDF file in this directory (or provide the full path), then run:

```bash
python pdf_analyzer.py your_document.pdf
```

## Step 3: View Results

The analysis report will be displayed in your terminal showing:
- Document statistics (word count, page count, etc.)
- Top 30 keywords
- Document structure and sections
- Numerical data found in the document

## Save Results to File

To save the analysis report:

```bash
python pdf_analyzer.py your_document.pdf --output analysis_report.txt
```

To also save the extracted text:

```bash
python pdf_analyzer.py your_document.pdf --output report.txt --extract-text text.txt
```

## Example Output Preview

```
================================================================================
PDF ANALYSIS REPORT
================================================================================

Document: research_paper.pdf
Total Pages: 157

--------------------------------------------------------------------------------
CONTENT STATISTICS
--------------------------------------------------------------------------------
Total Words: 45,234
Unique Words: 8,901
Average Sentence Length: 21.51 words

--------------------------------------------------------------------------------
TOP 30 KEYWORDS
--------------------------------------------------------------------------------
 1. research            -  234 occurrences
 2. data                -  198 occurrences
 3. analysis            -  176 occurrences
...
```

## Try the Examples

Run the example script to see various analysis capabilities:

```bash
python example_usage.py your_document.pdf
```

This will demonstrate:
- Basic analysis
- Keyword extraction
- Section detection
- Numerical data extraction
- File output options

## Need Help?

- Check the full documentation in [README.md](README.md)
- View available options: `python pdf_analyzer.py --help`
- See example usage: `python example_usage.py --help`

## Tips for Best Results

1. **Dense PDFs (150+ pages)**: The tool is optimized for large documents
2. **Text-based PDFs work best**: Image-based PDFs may need OCR first
3. **Save outputs**: Use `--output` and `--extract-text` to save your analysis
4. **Regular analysis**: Process multiple PDFs by running the script multiple times

---

Happy analyzing! 🎉
