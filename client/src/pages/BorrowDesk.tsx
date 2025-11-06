import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../lib/api'

type Record = {
  id: number
  borrower: number
  book: number
  borrow_date: string
  due_date: string
  return_date?: string
}

export default function BorrowDesk() {
  const [records, setRecords] = useState<Record[]>([])
  const [borrowerId, setBorrowerId] = useState('')
  const [bookId, setBookId] = useState('')
  const [error, setError] = useState('')

  async function load() {
    const { data } = await api.get('borrow-records')
    setRecords(data.results ?? data)
  }

  useEffect(() => { load() }, [])

  async function borrow() {
    setError('')
    try {
      await api.post('borrow', { borrower_id: Number(borrowerId), book_id: Number(bookId) })
      setBorrowerId(''); setBookId(''); await load()
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Borrow failed.')
    }
  }

  async function returnBook(id: number) {
    await api.post('return', { borrow_id: id })
    await load()
  }

  return (
    <div className="p-4 max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-semibold">Borrow Desk</h1>
        <div className="space-x-2">
          <Link to="/reports" className="px-3 py-2 bg-purple-600 text-white rounded">Reports</Link>
          <Link to="/" className="px-3 py-2 border rounded">Back to Catalog</Link>
        </div>
      </div>
      {error && <div className="text-red-600 mb-3">{error}</div>}
      <div className="flex gap-2 mb-4">
        <input placeholder="Member ID" className="border px-3 py-2" value={borrowerId} onChange={e=>setBorrowerId(e.target.value)} />
        <input placeholder="Book ID" className="border px-3 py-2" value={bookId} onChange={e=>setBookId(e.target.value)} />
        <button onClick={borrow} className="px-3 py-2 bg-blue-600 text-white rounded">Borrow</button>
      </div>
      <table className="w-full border">
        <thead className="bg-gray-50">
          <tr>
            <th className="text-left p-2 border">ID</th>
            <th className="text-left p-2 border">Borrower</th>
            <th className="text-left p-2 border">Book</th>
            <th className="text-left p-2 border">Borrowed</th>
            <th className="text-left p-2 border">Due</th>
            <th className="text-left p-2 border">Returned</th>
            <th className="text-left p-2 border"></th>
          </tr>
        </thead>
        <tbody>
          {records.map(r => (
            <tr key={r.id}>
              <td className="p-2 border">{r.id}</td>
              <td className="p-2 border">{r.borrower}</td>
              <td className="p-2 border">{r.book}</td>
              <td className="p-2 border">{r.borrow_date}</td>
              <td className="p-2 border">{r.due_date}</td>
              <td className="p-2 border">{r.return_date || '-'}</td>
              <td className="p-2 border">{!r.return_date && <button onClick={()=>returnBook(r.id)} className="px-2 py-1 bg-green-600 text-white rounded">Return</button>}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}


