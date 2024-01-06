import React, { useEffect, useState } from 'react';
import axios from 'axios'; // You need to install axios: npm install axios

function Sidebar() {
    const [files, setFiles] = useState([]);

    useEffect(() => {
        // Fetch the list of files from the server
        axios.get('/creations')
            .then(response => {
                setFiles(response.data);
            })
            .catch(error => {
                console.error('Error fetching files:', error);
            });
    }, []);

    const handleLinkClick = (event) => {
        console.log(event.target.innerText);
        // return (
        //     <div>
        //         <a href={`/creations/${file}`} download>{file}</a>
        //     </div>)
    }

    return (
        <div className="sidebar">
            <h2>Download a file</h2>
            <ul>
                {files.map((file, index) => (
                    <li onClick={handleLinkClick} key={index}>
                        {file}
                        {/* <a href={`/creations/${file}`} download>{file}</a> */}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Sidebar;
