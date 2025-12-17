#!/usr/bin/env python3
"""
Example Usage Script for PDF Analyzer

This script demonstrates how to use the PDF analyzer tool programmatically.
"""

import sys
import os

# Import the PDF analyzer functions
from pdf_analyzer import (
    extract_text_from_pdf,
    analyze_text,
    find_key_sections,
    extract_numbers_and_dates,
    generate_report
)


def example_basic_analysis(pdf_path):
    """
    Example 1: Basic PDF analysis
    """
    print("Example 1: Basic Analysis")
    print("-" * 50)
    
    # Extract text from PDF
    text, pages = extract_text_from_pdf(pdf_path)
    
    # Get basic statistics
    analysis = analyze_text(text)
    
    print(f"Document has {pages} pages")
    print(f"Total words: {analysis['word_count']:,}")
    print(f"Unique words: {analysis['unique_words']:,}")
    print(f"Average sentence length: {analysis['avg_sentence_length']:.2f} words")
    print()


def example_keyword_analysis(pdf_path):
    """
    Example 2: Keyword analysis
    """
    print("Example 2: Keyword Analysis")
    print("-" * 50)
    
    # Extract and analyze text
    text, _ = extract_text_from_pdf(pdf_path)
    analysis = analyze_text(text)
    
    # Display top 10 keywords
    print("Top 10 Keywords:")
    for i, (word, count) in enumerate(analysis['top_words'][:10], 1):
        print(f"{i:2d}. {word:15s} - {count:4d} occurrences")
    print()


def example_section_detection(pdf_path):
    """
    Example 3: Section detection
    """
    print("Example 3: Section Detection")
    print("-" * 50)
    
    # Extract text and find sections
    text, _ = extract_text_from_pdf(pdf_path)
    sections = find_key_sections(text)
    
    # Display found sections
    print("Document Sections:")
    for section_name, data in sections.items():
        if data['found']:
            print(f"✓ {section_name.title()}: Found {data['occurrences']} time(s)")
        else:
            print(f"✗ {section_name.title()}: Not found")
    print()


def example_numerical_extraction(pdf_path):
    """
    Example 4: Extract numerical data
    """
    print("Example 4: Numerical Data Extraction")
    print("-" * 50)
    
    # Extract text and numerical data
    text, _ = extract_text_from_pdf(pdf_path)
    numerical_data = extract_numbers_and_dates(text)
    
    print(f"Numbers found: {numerical_data['numbers_count']:,}")
    print(f"Dates found: {numerical_data['dates_count']}")
    if numerical_data['years_found']:
        years = sorted(set(numerical_data['years_found']))
        print(f"Years mentioned: {', '.join(years[:10])}", end="")
        if len(years) > 10:
            print(f" ... and {len(years) - 10} more")
        else:
            print()
    print()


def example_full_report(pdf_path):
    """
    Example 5: Generate full report
    """
    print("Example 5: Full Report Generation")
    print("-" * 50)
    
    # Extract and analyze
    text, pages = extract_text_from_pdf(pdf_path)
    analysis = analyze_text(text)
    sections = find_key_sections(text)
    numerical_data = extract_numbers_and_dates(text)
    
    # Generate report (will print to console)
    generate_report(pdf_path, text, pages, analysis, sections, numerical_data)


def example_save_to_files(pdf_path):
    """
    Example 6: Save analysis to files
    """
    print("Example 6: Save Analysis to Files")
    print("-" * 50)
    
    # Create output directory if it doesn't exist
    output_dir = "analysis_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Extract and analyze
    text, pages = extract_text_from_pdf(pdf_path)
    analysis = analyze_text(text)
    sections = find_key_sections(text)
    numerical_data = extract_numbers_and_dates(text)
    
    # Generate output filenames
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    report_file = os.path.join(output_dir, f"{base_name}_report.txt")
    text_file = os.path.join(output_dir, f"{base_name}_text.txt")
    
    # Save report
    generate_report(pdf_path, text, pages, analysis, sections, 
                   numerical_data, report_file)
    
    # Save extracted text
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"\nFiles saved to {output_dir}/")
    print(f"  - {os.path.basename(report_file)}")
    print(f"  - {os.path.basename(text_file)}")
    print()


def main():
    """Run all examples"""
    # Check if a PDF file is provided
    if len(sys.argv) < 2:
        print("Usage: python example_usage.py <pdf_file>")
        print("\nThis script demonstrates various ways to use the PDF analyzer.")
        print("Please provide a PDF file to analyze.")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("PDF ANALYZER - EXAMPLE USAGE DEMONSTRATIONS")
    print("=" * 60)
    print(f"\nAnalyzing: {pdf_path}\n")
    
    # Run examples
    try:
        example_basic_analysis(pdf_path)
        example_keyword_analysis(pdf_path)
        example_section_detection(pdf_path)
        example_numerical_extraction(pdf_path)
        example_save_to_files(pdf_path)
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError during analysis: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
