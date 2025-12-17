#!/usr/bin/env python3
"""
PDF Analyzer Tool
A comprehensive tool for analyzing dense PDF documents (+150 pages).
Extracts text, performs statistical analysis, and summarizes key information.
"""

import sys
import os
import re
from collections import Counter
import argparse


def extract_text_from_pdf(pdf_path):
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        tuple: (extracted_text, total_pages) - Extracted text as a string and total page count
    """
    try:
        import PyPDF2
        
        text = []
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            print(f"Processing {total_pages} pages...")
            
            for page_num, page in enumerate(pdf_reader.pages):
                if (page_num + 1) % 10 == 0:
                    print(f"Processed {page_num + 1}/{total_pages} pages...")
                text.append(page.extract_text())
        
        return '\n'.join(text), total_pages
    except ImportError:
        print("Error: PyPDF2 not installed. Please install it with: pip install PyPDF2")
        sys.exit(1)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        sys.exit(1)


def analyze_text(text):
    """
    Perform comprehensive text analysis.
    
    Args:
        text: The text content to analyze
        
    Returns:
        Dictionary containing analysis results
    """
    # Basic statistics
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    char_count_no_spaces = len(text.replace(' ', ''))
    
    # Sentence count (approximate)
    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if s.strip()])
    
    # Paragraph count (approximate)
    paragraphs = text.split('\n\n')
    paragraph_count = len([p for p in paragraphs if p.strip()])
    
    # Word frequency analysis
    # Clean words and convert to lowercase
    clean_words = [re.sub(r'[^\w\s]', '', word).lower() for word in words if word.strip()]
    word_freq = Counter(clean_words)
    
    # Remove common stop words for more meaningful analysis
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                  'of', 'with', 'is', 'was', 'are', 'were', 'be', 'been', 'being',
                  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                  'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
                  'i', 'you', 'he', 'she', 'it', 'we', 'they', 'them', 'their',
                  'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all',
                  'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some',
                  'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
                  'too', 'very', 'as', 'from', 'by', ''}
    
    meaningful_words = {word: count for word, count in word_freq.items() 
                       if word not in stop_words and len(word) > 2}
    
    # Calculate average word length in a single pass
    total_word_length = sum(len(word) for word in clean_words)
    word_list_length = len(clean_words)
    
    return {
        'word_count': word_count,
        'char_count': char_count,
        'char_count_no_spaces': char_count_no_spaces,
        'sentence_count': sentence_count,
        'paragraph_count': paragraph_count,
        'unique_words': len(set(clean_words)),
        'top_words': Counter(meaningful_words).most_common(30),
        'avg_word_length': total_word_length / word_list_length if word_list_length > 0 else 0,
        'avg_sentence_length': word_count / sentence_count if sentence_count > 0 else 0
    }


def find_key_sections(text):
    """
    Identify key sections in the document based on common patterns.
    
    Args:
        text: The text content to analyze
        
    Returns:
        Dictionary containing identified sections
    """
    sections = {}
    
    # Common section headers patterns (ordered to avoid ambiguous matches)
    patterns = {
        'introduction': r'(?i)(introduction|overview|abstract)',
        'methodology': r'(?i)(method|methodology|approach|procedure)',
        'results': r'(?i)(results|findings|outcomes)',
        'conclusion': r'(?i)(conclusion|final remarks|closing)',
        'references': r'(?i)(references|bibliography|citations|works cited)',
        'acknowledgments': r'(?i)(acknowledgments?|acknowledgements?)'
    }
    
    for section_name, pattern in patterns.items():
        matches = re.finditer(pattern, text)
        positions = [match.start() for match in matches]
        if positions:
            sections[section_name] = {
                'found': True,
                'occurrences': len(positions),
                'first_position': positions[0]
            }
        else:
            sections[section_name] = {'found': False}
    
    return sections


def extract_numbers_and_dates(text):
    """
    Extract numerical data and dates from the text.
    
    Args:
        text: The text content to analyze
        
    Returns:
        Dictionary containing extracted numbers and dates
    """
    # Use a single pass with combined pattern for better performance on large documents
    # Pattern captures: numbers with optional decimals/percentages, dates, and years
    combined_pattern = r'\b\d+(?:\.\d+)?%?\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b'
    
    numbers = []
    dates = []
    years = set()
    
    for match in re.finditer(combined_pattern, text):
        matched_text = match.group()
        if '/' in matched_text or '-' in matched_text:
            dates.append(matched_text)
        else:
            numbers.append(matched_text)
            # Check if it's a year
            if len(matched_text) == 4 and matched_text.startswith(('19', '20')):
                years.add(matched_text)
    
    return {
        'numbers_count': len(numbers),
        'dates_count': len(dates),
        'years_found': list(years)[:20]  # Limit to 20 unique years
    }


def generate_report(pdf_path, text, pages, analysis, sections, numerical_data, output_file=None):
    """
    Generate a comprehensive analysis report.
    
    Args:
        pdf_path: Path to the analyzed PDF
        text: Extracted text
        pages: Number of pages
        analysis: Text analysis results
        sections: Identified sections
        numerical_data: Extracted numerical data
        output_file: Optional output file path
    """
    report = []
    report.append("=" * 80)
    report.append("PDF ANALYSIS REPORT")
    report.append("=" * 80)
    report.append(f"\nDocument: {os.path.basename(pdf_path)}")
    report.append(f"Location: {os.path.abspath(pdf_path)}")
    report.append(f"Total Pages: {pages}")
    report.append("\n" + "-" * 80)
    report.append("CONTENT STATISTICS")
    report.append("-" * 80)
    report.append(f"Total Words: {analysis['word_count']:,}")
    report.append(f"Unique Words: {analysis['unique_words']:,}")
    report.append(f"Total Characters: {analysis['char_count']:,}")
    report.append(f"Characters (no spaces): {analysis['char_count_no_spaces']:,}")
    report.append(f"Estimated Sentences: {analysis['sentence_count']:,}")
    report.append(f"Estimated Paragraphs: {analysis['paragraph_count']:,}")
    report.append(f"Average Word Length: {analysis['avg_word_length']:.2f} characters")
    report.append(f"Average Sentence Length: {analysis['avg_sentence_length']:.2f} words")
    
    report.append("\n" + "-" * 80)
    report.append("TOP 30 KEYWORDS (excluding common words)")
    report.append("-" * 80)
    for i, (word, count) in enumerate(analysis['top_words'], 1):
        report.append(f"{i:2d}. {word:20s} - {count:4d} occurrences")
    
    report.append("\n" + "-" * 80)
    report.append("DOCUMENT STRUCTURE")
    report.append("-" * 80)
    found_sections = [name for name, data in sections.items() if data['found']]
    if found_sections:
        report.append("Identified Sections:")
        for section_name, data in sections.items():
            if data['found']:
                report.append(f"  • {section_name.title()}: Found {data['occurrences']} time(s)")
    else:
        report.append("No standard section headers identified.")
    
    report.append("\n" + "-" * 80)
    report.append("NUMERICAL DATA")
    report.append("-" * 80)
    report.append(f"Numbers Found: {numerical_data['numbers_count']:,}")
    report.append(f"Dates Found: {numerical_data['dates_count']}")
    if numerical_data['years_found']:
        report.append(f"Years Mentioned: {', '.join(sorted(set(numerical_data['years_found'])))}")
    
    report.append("\n" + "-" * 80)
    report.append("TEXT PREVIEW (first 500 characters)")
    report.append("-" * 80)
    preview = text[:500].strip()
    report.append(preview)
    if len(text) > 500:
        report.append("...")
    
    report.append("\n" + "=" * 80)
    report.append("END OF REPORT")
    report.append("=" * 80)
    
    report_text = '\n'.join(report)
    
    # Print to console
    print(report_text)
    
    # Save to file if specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"\nReport saved to: {output_file}")


def save_extracted_text(text, output_file):
    """
    Save extracted text to a file.
    
    Args:
        text: The text to save
        output_file: Path to the output file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Extracted text saved to: {output_file}")


def main():
    """Main function to run the PDF analyzer."""
    parser = argparse.ArgumentParser(
        description='Analyze dense PDF documents and extract key information.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pdf_analyzer.py document.pdf
  python pdf_analyzer.py document.pdf --output report.txt
  python pdf_analyzer.py document.pdf --extract-text output.txt
  python pdf_analyzer.py document.pdf --output report.txt --extract-text text.txt
        """
    )
    
    parser.add_argument('pdf_file', help='Path to the PDF file to analyze')
    parser.add_argument('-o', '--output', help='Save analysis report to file')
    parser.add_argument('-e', '--extract-text', dest='extract_text', 
                       help='Save extracted text to file')
    
    args = parser.parse_args()
    
    # Check if PDF file exists
    if not os.path.exists(args.pdf_file):
        print(f"Error: PDF file not found: {args.pdf_file}")
        sys.exit(1)
    
    print(f"Analyzing PDF: {args.pdf_file}\n")
    
    # Extract text from PDF
    text, pages = extract_text_from_pdf(args.pdf_file)
    
    if not text.strip():
        print("Warning: No text could be extracted from the PDF.")
        print("The PDF might be image-based or encrypted.")
        sys.exit(1)
    
    # Perform analysis
    print("\nPerforming text analysis...")
    analysis = analyze_text(text)
    
    print("Identifying document structure...")
    sections = find_key_sections(text)
    
    print("Extracting numerical data...")
    numerical_data = extract_numbers_and_dates(text)
    
    # Generate report
    print("\n")
    generate_report(args.pdf_file, text, pages, analysis, sections, 
                   numerical_data, args.output)
    
    # Save extracted text if requested
    if args.extract_text:
        save_extracted_text(text, args.extract_text)


if __name__ == '__main__':
    main()
