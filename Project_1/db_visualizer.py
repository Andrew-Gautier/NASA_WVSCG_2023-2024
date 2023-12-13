import matplotlib.pyplot as plt
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from db_loader import Folder, SourceCodeFile, Manifest, Vulnerability, sessionmaker, engine

# Your code to load the database schema from db_loader.py


# List of file extensions
extensions = ['.c', '.java', '.cpp', '.php', '.cs']

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

for ext in extensions:
    # Query the lengths and content of the files
    files = session.query(
        func.length(SourceCodeFile.file_content),
        SourceCodeFile.file_content
    ).filter(SourceCodeFile.file_extension == ext).all()

    # Convert the result to a list of lengths and line counts
    lengths = [file[0] for file in files]
    line_counts = [file[1].count('\n') for file in files]

    # Create a histogram of the lengths
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.hist(lengths, bins=50)
    plt.title(f'Histogram of the Length of {ext} Files')
    plt.xlabel('Length')
    plt.ylabel('Frequency')

    # Create a histogram of the line counts
    plt.subplot(1, 2, 2)
    plt.hist(line_counts, bins=50)
    plt.title(f'Histogram of Line Counts of {ext} Files')
    plt.xlabel('Line Count')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.show()

# Close the session
session.close()