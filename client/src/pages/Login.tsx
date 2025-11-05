import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '../lib/api'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    try {
      await login(username, password)
      navigate('/')
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <form onSubmit={onSubmit} className="w-full max-w-sm bg-white p-6 rounded shadow">
        <h1 className="text-xl font-semibold mb-4">Login</h1>
        {error && <div className="text-red-600 text-sm mb-2">{error}</div>}
        <label className="block mb-2">Username</label>
        <input className="w-full border px-3 py-2 mb-4" value={username} onChange={e=>setUsername(e.target.value)} />
        <label className="block mb-2">Password</label>
        <input type="password" className="w-full border px-3 py-2 mb-4" value={password} onChange={e=>setPassword(e.target.value)} />
        <button className="w-full bg-blue-600 text-white py-2 rounded">Sign In</button>
      </form>
    </div>
  )
}


