import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../lib/api'

type CirculationSummary = {
  since: string
  total_borrowed: number
  total_returned: number
}

type TopBorrowedBook = {
  book__id: number
  book__title: string
  book__author: string
  times: number
}

export default function Reports() {
  const [summary, setSummary] = useState<CirculationSummary | null>(null)
  const [topBorrowed, setTopBorrowed] = useState<TopBorrowedBook[]>([])
  const [range, setRange] = useState<'day' | 'week' | 'month'>('week')
  const [loading, setLoading] = useState(true)

  async function loadReports() {
    setLoading(true)
    try {
      const [summaryRes, topRes] = await Promise.all([
        api.get('reports/circulation-summary', { params: { range } }),
        api.get('reports/top-borrowed', { params: { limit: 10 } })
      ])
      setSummary(summaryRes.data)
      setTopBorrowed(topRes.data)
    } catch (e: any) {
      console.error('Failed to load reports:', e)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadReports()
  }, [range])

  return (
    <div className="p-4 max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-semibold">Reports</h1>
        <Link to="/" className="px-3 py-2 border rounded">Back to Catalog</Link>
      </div>

      {loading ? (
        <div className="text-center py-8">Loading reports...</div>
      ) : (
        <>
          {/* Circulation Summary */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-xl font-semibold">Circulation Summary</h2>
              <div className="flex gap-2">
                <button
                  onClick={() => setRange('day')}
                  className={`px-3 py-1 border rounded ${range === 'day' ? 'bg-blue-600 text-white' : ''}`}
                >
                  Day
                </button>
                <button
                  onClick={() => setRange('week')}
                  className={`px-3 py-1 border rounded ${range === 'week' ? 'bg-blue-600 text-white' : ''}`}
                >
                  Week
                </button>
                <button
                  onClick={() => setRange('month')}
                  className={`px-3 py-1 border rounded ${range === 'month' ? 'bg-blue-600 text-white' : ''}`}
                >
                  Month
                </button>
              </div>
            </div>
            {summary && (
              <div className="bg-gray-50 p-4 rounded border">
                <p className="text-sm text-gray-600 mb-3">Since: {new Date(summary.since).toLocaleDateString()}</p>
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-white p-4 rounded border">
                    <div className="text-sm text-gray-600">Total Borrowed</div>
                    <div className="text-2xl font-bold">{summary.total_borrowed}</div>
                  </div>
                  <div className="bg-white p-4 rounded border">
                    <div className="text-sm text-gray-600">Total Returned</div>
                    <div className="text-2xl font-bold">{summary.total_returned}</div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Top Borrowed Books */}
          <div>
            <h2 className="text-xl font-semibold mb-3">Top Borrowed Books</h2>
            {topBorrowed.length > 0 ? (
              <table className="w-full border">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="text-left p-2 border">Rank</th>
                    <th className="text-left p-2 border">Title</th>
                    <th className="text-left p-2 border">Author</th>
                    <th className="text-left p-2 border">Times Borrowed</th>
                  </tr>
                </thead>
                <tbody>
                  {topBorrowed.map((book, index) => (
                    <tr key={book.book__id}>
                      <td className="p-2 border">{index + 1}</td>
                      <td className="p-2 border">{book.book__title}</td>
                      <td className="p-2 border">{book.book__author}</td>
                      <td className="p-2 border">{book.times}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className="text-center py-8 text-gray-500">No borrowing data available.</div>
            )}
          </div>
        </>
      )}
    </div>
  )
}


