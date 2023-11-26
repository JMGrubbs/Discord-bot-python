const express = require('express');
const path = require('path');
const app = express();

// Serve static files from the 'public/creations' directory
app.use('/creations', express.static(path.join(__dirname, 'public/creations')));

// Start the server on port 3001 (or any other port you prefer)
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
