import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dest = os.path.join(BASE, "src", "App.jsx")

content = """\
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Rapporto from './pages/Rapporto'
import Anteprima from './pages/Anteprima'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/rapporto/:id" element={<Rapporto />} />
        <Route path="/rapporto/:id/anteprima" element={<Anteprima />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  )
}
"""

os.makedirs(os.path.dirname(dest), exist_ok=True)
with open(dest, "w", encoding="utf-8") as f:
    f.write(content.strip())
print(f"✅ src/App.jsx scritto in {dest}")
