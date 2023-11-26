const fs = require('fs');
const path = require('path');

function writeToPublicDirectory(text) {
    const directoryPath = path.join(__dirname, 'public', 'Creations'); // Path to the target directory
    const filePath = path.join(directoryPath, 'output.txt'); // Path to the output file

    // Create the directory if it doesn't exist
    if (!fs.existsSync(directoryPath)) {
        fs.mkdirSync(directoryPath, { recursive: true });
    }

    // Write the text to the output file
    fs.writeFileSync(filePath, text);

    console.log('File written successfully.');
}

// Example usage:
const textToWrite = 'This is the content that will be written to the file.';
writeToPublicDirectory(textToWrite);
