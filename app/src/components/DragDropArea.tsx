import React, { useCallback, useState } from 'react'

interface Props {
  onFilesDropped: (files: File[]) => void
}

const DragDropArea: React.FC<Props> = ({ onFilesDropped }) => {
  const [isActive, setActive] = useState(false)

  const handleDrop = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault()
      setActive(false)
      const files = Array.from(event.dataTransfer.files)
      onFilesDropped(files)
    },
    [onFilesDropped]
  )

  return (
    <div
      onDragOver={(event) => {
        event.preventDefault()
        setActive(true)
      }}
      onDragLeave={() => setActive(false)}
      onDrop={handleDrop}
      style={{
        border: isActive ? '2px dashed #4f46e5' : '2px dashed #d1d5db',
        padding: '2rem',
        borderRadius: '0.75rem',
        textAlign: 'center',
        background: isActive ? '#eef2ff' : '#f9fafb'
      }}
    >
      <p>Drag and drop files to enqueue them for ingestion.</p>
    </div>
  )
}

export default DragDropArea
