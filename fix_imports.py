#!/usr/bin/env python3
import os
import re

def update_imports_in_file(filepath):
    with open(filepath, 'r') as file:
        content = file.read()
    
    # Update imports from main module
    content = re.sub(r'from main import', r'from src.main import', content)
    content = re.sub(r'import main', r'import src.main as main', content)
    
    # Update imports from textnode module
    content = re.sub(r'from textnode import', r'from src.textnode import', content)
    content = re.sub(r'import textnode', r'import src.textnode as textnode', content)
    
    # Update imports from htmlnode module
    content = re.sub(r'from htmlnode import', r'from src.htmlnode import', content)
    content = re.sub(r'import htmlnode', r'import src.htmlnode as htmlnode', content)
    
    with open(filepath, 'w') as file:
        file.write(content)
    
    print(f"Updated imports in {filepath}")

def main():
    tests_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')
    
    for filename in os.listdir(tests_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            filepath = os.path.join(tests_dir, filename)
            update_imports_in_file(filepath)
    
    print("All test files updated successfully!")

if __name__ == "__main__":
    main()