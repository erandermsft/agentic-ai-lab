# Azure AI Content Understanding - Classifier and Analyzer Lab  

## Overview  

This lab demonstrates how to use Azure AI Content Understanding to automate the classification and extraction of information from bundled document files (such as insurance claims, statements, bills, and receipts). Students will learn to:  

- Build a classifier to categorize documents within a single PDF bundle.  
- Create custom analyzers to extract specific fields from different document types.  
- Combine classifiers and analyzers for enhanced document processing.  
- Process a sample PDF bundle, split it into logical documents, and extract structured data.  

## Prerequisites  

- An active Azure subscription.  
- An AI Foundry Resource in Azure (supported regions: westus, swedencentral, australiaeast).  
- The provided sample PDF file (sample claim submission.pdf).  
- The AzureContentUnderstandingClient.py file in your working directory.  
- A .env file with the required environment variables.  

## Lab Instructions  

### 0. Setup  

**Before you begin:**  

1. Ensure you have all prerequisites.  
2. Update your .env file with:  

SERVICE_FOR_CU: Endpoint of your Azure Content Understanding service.  
SERVICE_API_FOR_CU: API version (e.g., 2025-05-01-preview).  
SAMPLE_CLAIMS_BUNDLE: Path to your sample PDF.  

### 1. Import Required Libraries  

**Cell Purpose:**  

Import all necessary Python libraries for the lab.  

**Instructions:**

1. Run the cell to import libraries such as json, os, uuid, and Azure identity modules.  
2. Confirm you see "Libraries imported successfully!"  

### 2. Import Azure Content Understanding Client  

**Cell Purpose:**  

Import the custom client class for interacting with Azure AI Content Understanding.  

**Instructions:**  

1. Ensure AzureContentUnderstandingClient.py is in your directory.  
2. Run the cell. If you see an import error, check the file location.  

### 3. Load Environment Variables and Set Credentials

**Cell Purpose:**  

Load credentials and configuration from your .env file.  

**Instructions:**  

1. Edit your .env file as described above.  
2. Run the cell to load variables and set up authentication.  
3. Confirm the configuration summary prints your endpoint, API version, and sample file.  

### 4. Define a Classifier Schema

**Cell Purpose:**  

Define the schema for classifying document types within the PDF bundle.  

**Instructions:**  

1. Review the schema categories (e.g., Completed_Claim_Form, HIPAA_Release, etc.).  
2. Understand the splitMode options:  

- "auto": Split based on content.  
- "none": Treat the bundle as a single document.  
- "perPage": Split by page.  

3. Run the cell to set up the classifier schema.  

### 5. Initialize Content Understanding Client

**Cell Purpose:**  

Create the client instance to communicate with Azure AI services.  

**Instructions:**

1. Run the cell to initialize the client.  
2. Confirm you see "Content Understanding client initialized successfully!"  

### 6A. Create a Custom Analyzer for Itemized Bill Doc Types  

**Cell Purpose:**  

Define and create an analyzer to extract the document title from each itemized bill.  

**Instructions:**  

1. Review the analyzer schema.  
2. Run the cell to create the analyzer.  
3. Confirm successful creation and note the analyzer ID.  

### 6B. Create a Custom Analyzer for Billed Expenses  

**Cell Purpose:**  

Define and create an analyzer to extract all billed expenses as a table.  

**Instructions:**  

1. Review the fields (Expense_Amount, ICD_Code, Date, Description, etc.).  
2. Run the cell to create the analyzer.  
3. Confirm successful creation and note the analyzer ID.  

### 6C. Create a Custom Analyzer for Patient Information  

**Cell Purpose:**  

Define and create an analyzer to extract patient information fields.  

**Instructions:**

1. Review the fields (First Name, Last Name, DOB, Gender, Policy Number).  
2. Run the cell to create the analyzer.  
3. Confirm successful creation and note the analyzer ID.  

### 7. Create an Enhanced Classifier Schema with 3 Custom Analyzers

**Cell Purpose:**  

Combine the classifier and analyzers so each document type uses the appropriate analyzer.  

**Instructions:**

1. Review how each document type is mapped to an analyzer.
2. Run the cell to define the enhanced schema.

### 8. Create the Classifier  

**Cell Purpose:**  

Create the enhanced classifier using the schema from the previous step.  

**Instructions:**  

1. Run the cell to create the classifier.  
2. Confirm successful creation and note the classifier ID.  

### 9. Process Document with Enhanced Classifier  

**Cell Purpose:**  

Classify and analyze the sample PDF bundle.  

**Instructions:**  

1. Run the cell to process the document.  
2. Confirm you see "Enhanced processing completed!"  

### 10. Create a Function to Parse and Display Results  

**Cell Purpose:**  

Define a function to parse and display the analysis results for each document.  

**Instructions:**  

1. Run the cell to define the function.  
2. Use the function to print document analysis results (type, fields, expenses, confidence scores).  

### 11. Create a Function to Give a Summary  

**Cell Purpose:**  

Define a function to summarize the entire bundle (number of documents, pages, field distribution).  

**Instructions:**

1. Run the cell to define the summary function.
2. Use the function to print a summary table and field distribution.

### 12. Lab Summary

**You have accomplished:**  

Creating a classifier and custom analyzers.  
Combining them for intelligent document processing.  
Processing a sample file and extracting structured data.  

## Next Steps  

**Explore further by:**  

Modifying the schema for new document types.  
Creating additional analyzers for audio, video, or image content.  
Integrating with other Azure AI services.  
