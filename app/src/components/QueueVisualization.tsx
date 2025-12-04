import React from 'react'

export interface QueueItem {
  id: string
  status: string
  path: string
}

interface Props {
  queue: QueueItem[]
}

const QueueVisualization: React.FC<Props> = ({ queue }) => {
  return (
    <div style={{ marginTop: '1rem' }}>
      <h3>Ingestion Queue</h3>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {queue.map((item) => (
          <li
            key={item.id}
            style={{
              background: '#f3f4f6',
              padding: '0.5rem 1rem',
              borderRadius: '0.5rem',
              marginBottom: '0.5rem',
              display: 'flex',
              justifyContent: 'space-between',
            }}
          >
            <span>{item.path}</span>
            <strong>{item.status}</strong>
          </li>
        ))}
        {queue.length === 0 && <p>No pending items.</p>}
      </ul>
    </div>
  )
}

export default QueueVisualization
