import React, { useState } from 'react'
import DragDropArea from './components/DragDropArea'
import QueueVisualization, { QueueItem } from './components/QueueVisualization'
import SearchPanel, { SearchHit } from './components/SearchPanel'

const App: React.FC = () => {
  const [queue, setQueue] = useState<QueueItem[]>([])

  const handleFilesDropped = (files: File[]) => {
    const items = files.map((file, index) => ({
      id: `${queue.length + index + 1}`,
      status: 'queued',
      path: file.name
    }))
    setQueue((prev) => [...prev, ...items])
  }

  const handleSearch = async (query: string): Promise<SearchHit[]> => {
    // Placeholder search that reuses queue items as pseudo results
    return queue
      .filter((item) => item.path.toLowerCase().includes(query.toLowerCase()))
      .map((item, idx) => ({
        job_id: item.id,
        score: 1 - idx * 0.1,
        metadata: { name: item.path, summary: 'Queued item awaiting ingestion' }
      }))
  }

  return (
    <div style={{ maxWidth: '960px', margin: '0 auto', padding: '2rem', fontFamily: 'Inter, sans-serif' }}>
      <header style={{ marginBottom: '2rem' }}>
        <h1>File Organizer</h1>
        <p>Drag-and-drop ingestion, queue visibility, and semantic search in a Tauri shell.</p>
      </header>

      <DragDropArea onFilesDropped={handleFilesDropped} />
      <QueueVisualization queue={queue} />
      <SearchPanel onSearch={handleSearch} />
    </div>
  )
}

export default App
