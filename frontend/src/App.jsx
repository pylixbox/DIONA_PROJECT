import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [logs, setLogs] = useState([]);

  const fetchData = () => {
    axios.get('http://localhost:5000/api/alerts')
      .then(res => setLogs(res.data))
      .catch(err => console.log("Backend offline"));
  };

  useEffect(() => {
    const interval = setInterval(fetchData, 5000); // Polling every 5s
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '40px', backgroundColor: '#1a202c', color: 'white', minHeight: '100vh' }}>
      <h1>DIONA Security Operations Center</h1>
      <table width="100%" style={{ borderCollapse: 'collapse', marginTop: '20px' }}>
        <thead>
          <tr style={{ backgroundColor: '#2d3748' }}>
            <th>ID</th><th>Type</th><th>Attacker IP</th><th>Time</th>
          </tr>
        </thead>
        <tbody>
          {logs.map(log => (
            <tr key={log.id} style={{ borderBottom: '1px solid #4a5568' }}>
              <td>{log.id}</td>
              <td style={{ color: '#f56565', fontWeight: 'bold' }}>{log.attack_type}</td>
              <td>{log.attacker_ip}</td>
              <td>{log.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
export default App;