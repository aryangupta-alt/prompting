# Structured Invoice Extraction using Gemini

## Overview

This project demonstrates structured information extraction from B2B invoices using Gemini 2.5 Flash and Pydantic schemas.

## Features

* Structured JSON output
* Response schema enforcement
* Pydantic validation
* Field-level accuracy evaluation

## Project Structure

extractor/

* schema.py
* main.py
* evaluate.py
* samples/
* ground_truth.jsonl
* field_accuracy.csv
* accuracy_summary.md

## Installation

pip install google-genai pydantic python-dotenv

## Environment Variable

export GEMINI_API_KEY="YOUR_API_KEY"

## Run Extraction

python main.py samples/invoice_1.txt

## Run Evaluation

python evaluate.py

## Output

* field_accuracy.csv
* accuracy_summary.md

## Model

Gemini 2.5 Flash
