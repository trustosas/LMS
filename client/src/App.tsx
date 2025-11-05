import { Navigate, Route, Routes } from 'react-router-dom'
import Login from './pages/Login'
import Catalog from './pages/Catalog'
import BorrowDesk from './pages/BorrowDesk'

function isAuthed() {
  return !!localStorage.getItem('access')
}

function Protected({ children }: { children: JSX.Element }) {
  if (!isAuthed()) return <Navigate to="/login" replace />
  return children
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<Protected><Catalog /></Protected>} />
      <Route path="/borrow" element={<Protected><BorrowDesk /></Protected>} />
    </Routes>
  )
}


