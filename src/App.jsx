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