import React, { useState } from 'react'

export interface SearchHit {
  job_id: string
  score: number
  metadata: Record<string, string>
}

interface Props {
  onSearch: (query: string) => Promise<SearchHit[]>
}

const SearchPanel: React.FC<Props> = ({ onSearch }) => {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchHit[]>([])

  const handleSearch = async () => {
    const data = await onSearch(query)
    setResults(data)
  }

  return (
    <div style={{ marginTop: '2rem' }}>
      <h3>Search</h3>
      <div style={{ display: 'flex', gap: '0.5rem' }}>
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Find ingested content"
          style={{ flex: 1, padding: '0.5rem 0.75rem' }}
        />
        <button onClick={handleSearch} style={{ padding: '0.5rem 0.75rem' }}>
          Search
        </button>
      </div>
      <ul style={{ listStyle: 'none', padding: 0, marginTop: '1rem' }}>
        {results.map((hit) => (
          <li key={hit.job_id} style={{ marginBottom: '0.75rem' }}>
            <strong>{hit.metadata.name ?? 'Unnamed file'}</strong>
            <div>Score: {hit.score.toFixed(3)}</div>
            <div style={{ color: '#4b5563' }}>{hit.metadata.summary}</div>
          </li>
        ))}
        {results.length === 0 && <p>Run a search to see results.</p>}
      </ul>
    </div>
  )
}

export default SearchPanel
