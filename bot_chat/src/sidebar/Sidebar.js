import React, { useEffect, useState } from 'react';
import { get_agents, select_proxy_agent } from '../api/fastapi/agents';
import { get_creations } from '../api/fastapi/files';

function Sidebar() {
    const [files, setFiles] = useState([]);
    const [agents, setAgents] = useState({});
    const [agentKeys, setAgentsKeys] = useState([]);

    useState(async () => {
        let creations_response = await get_creations();
        let agents_response = await get_agents();

        setFiles(creations_response);
        setAgents(agents_response);
        setAgentsKeys(Object.keys(agents_response));
    }, []);

    const handle_agent_click = async (event) => {
        const agent_key_index = event.currentTarget.getAttribute('id');
        let clicked_agent = agents[agentKeys[agent_key_index]];
        await select_proxy_agent(clicked_agent.id);
    };

    const handleLinkClick = (event) => {
        // return (
        //     <div>
        //         <a href={`/creations/${file}`} download>{file}</a>
        //     </div>)
    }

    return (
        <div className="sidebar">
            <h2>Agents</h2>
            <ul>
                {agentKeys.map((agent_key, index) => (
                    <li id={index} onClick={handle_agent_click} key={index}>
                        {agents[agent_key].name}
                    </li>
                ))}
            </ul>
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
