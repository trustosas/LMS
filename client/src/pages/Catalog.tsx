import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, logout } from '../lib/api'

type Book = {
  id: number
  title: string
  author: string
  isbn: string
  copies_available: number
  copies_total: number
  status: string
}

export default function Catalog() {
  const [books, setBooks] = useState<Book[]>([])
  const [q, setQ] = useState('')
  const [editingId, setEditingId] = useState<number | null>(null)
  const [form, setForm] = useState({ title: '', author: '', isbn: '', copies_total: 1 })
  const [me, setMe] = useState<{ id: number; username: string; role: string } | null>(null)
  const [meLoaded, setMeLoaded] = useState(false)
  const [activeBorrowBookId, setActiveBorrowBookId] = useState<number | null>(null)
  const isStaff = useMemo(() => {
    const role = (me?.role || '').toString().trim().toUpperCase()
    return role === 'ADMIN' || role === 'LIBRARIAN'
  }, [me])

  async function load() {
    const { data } = await api.get('books', { params: q ? { search: q } : {} })
    setBooks(data.results ?? data)
  }

  async function loadActiveBorrow() {
    try {
      const { data } = await api.get('my-active-borrow')
      // API returns either the borrow record (with 'book' field as book ID) or {"book_id": null}
      if (data.book_id === null) {
        setActiveBorrowBookId(null)
      } else {
        // data.book is the book ID when there's an active borrow
        setActiveBorrowBookId(data.book || null)
      }
    } catch {
      setActiveBorrowBookId(null)
    }
  }

  useEffect(() => {
    load()
    api.get('auth/me').then(r => {
      setMe(r.data)
      setMeLoaded(true)
      // Load active borrow for non-staff users
      const role = (r.data?.role || '').toString().trim().toUpperCase()
      if (role !== 'ADMIN' && role !== 'LIBRARIAN') {
        setTimeout(() => loadActiveBorrow(), 100)
      }
    }).catch(() => {
      setMe(null)
      setMeLoaded(true)
    })
  }, [])

  function loadBookIntoForm(b: Book) {
    setEditingId(b.id)
    setForm({ title: b.title, author: b.author, isbn: b.isbn, copies_total: b.copies_total })
  }

  async function saveBook() {
    if (editingId) {
      await api.patch(`books/${editingId}`, {
        title: form.title,
        author: form.author,
        // isbn left unchanged during edit; enable if needed
        copies_total: Number(form.copies_total),
      })
    } else {
      await api.post('books', {
        title: form.title,
        author: form.author,
        isbn: form.isbn,
        copies_total: Number(form.copies_total),
      })
    }
    setEditingId(null)
    setForm({ title: '', author: '', isbn: '', copies_total: 1 })
    await load()
  }

  function cancelEdit() {
    setEditingId(null)
    setForm({ title: '', author: '', isbn: '', copies_total: 1 })
  }

  async function borrowBook(bookId: number) {
    if (!me) return
    try {
      await api.post('borrow', { borrower_id: me.id, book_id: bookId })
      await load()
      await loadActiveBorrow()
    } catch (e: any) {
      alert(e?.response?.data?.detail || 'Borrow failed.')
    }
  }

  return (
    <div className="p-4 max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-semibold">Catalog</h1>
        <div className="space-x-2">
          {me && <span className="text-sm text-gray-600">Signed in as <span className="font-medium">{me.username}</span> ({me.role})</span>}
          {meLoaded && isStaff ? (
            <>
              <Link to="/borrow" className="px-3 py-2 bg-blue-600 text-white rounded">Borrow Desk</Link>
              <Link to="/reports" className="px-3 py-2 bg-purple-600 text-white rounded">Reports</Link>
            </>
          ) : null}
          <button onClick={()=>{logout(); location.href='/login'}} className="px-3 py-2 border rounded">Logout</button>
        </div>
      </div>
      <div className="mb-3 flex gap-2">
        <input placeholder="Search title/author/ISBN" value={q} onChange={e=>setQ(e.target.value)} className="border px-3 py-2 flex-1" />
        <button onClick={load} className="px-3 py-2 bg-gray-800 text-white rounded">Search</button>
      </div>
      {meLoaded && isStaff ? (
        <div className="mb-6 p-3 border rounded grid grid-cols-1 md:grid-cols-5 gap-2 items-end">
          <input className="border px-3 py-2" placeholder="Title" value={form.title} onChange={e=>setForm({...form, title: e.target.value})} />
          <input className="border px-3 py-2" placeholder="Author" value={form.author} onChange={e=>setForm({...form, author: e.target.value})} />
          <input className="border px-3 py-2" placeholder="ISBN" value={form.isbn} onChange={e=>setForm({...form, isbn: e.target.value})} disabled={!!editingId} />
          <input type="number" min={1} className="border px-3 py-2" placeholder="Copies" value={form.copies_total} onChange={e=>setForm({...form, copies_total: Number(e.target.value)})} />
          <div className="flex gap-2">
            <button onClick={saveBook} className="px-3 py-2 bg-green-700 text-white rounded">{editingId ? 'Save Changes' : 'Add Book'}</button>
            {editingId && <button onClick={cancelEdit} className="px-3 py-2 border rounded">Cancel</button>}
          </div>
        </div>
      ) : null}
      <table className="w-full border">
        <thead className="bg-gray-50">
          <tr>
            <th className="text-left p-2 border">Title</th>
            <th className="text-left p-2 border">Author</th>
            <th className="text-left p-2 border">ISBN</th>
            <th className="text-left p-2 border">Available</th>
            <th className="text-left p-2 border">Total</th>
            <th className="text-left p-2 border">Status</th>
            <th className="text-left p-2 border">Actions</th>
          </tr>
        </thead>
        <tbody>
          {books.map(b => (
            <tr key={b.id}>
              <td className="p-2 border">{b.title}</td>
              <td className="p-2 border">{b.author}</td>
              <td className="p-2 border">{b.isbn}</td>
              <td className="p-2 border">{b.copies_available}</td>
              <td className="p-2 border">{b.copies_total}</td>
              <td className="p-2 border">{b.status}</td>
              <td className="p-2 border">
                {meLoaded && (
                  isStaff ? (
                    <button onClick={()=>loadBookIntoForm(b)} className="px-2 py-1 border rounded">Edit</button>
                  ) : (
                    activeBorrowBookId === b.id ? (
                      <button 
                        disabled 
                        className="px-2 py-1 border rounded bg-gray-300 text-gray-600 cursor-not-allowed"
                      >
                        Borrowed
                      </button>
                    ) : (
                      <button 
                        disabled={b.copies_available <= 0 || activeBorrowBookId !== null} 
                        onClick={()=>borrowBook(b.id)} 
                        className="px-2 py-1 border rounded disabled:opacity-50"
                      >
                        Borrow
                      </button>
                    )
                  )
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}


