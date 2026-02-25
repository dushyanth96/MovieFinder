import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { MovieProvider } from './contexts/MovieContext'
import './css/index.css'
import App from './App.jsx'
import { warmupBackend } from './services/backend'

// Silent background warm-up
warmupBackend();

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <MovieProvider>
        <App />
      </MovieProvider>
    </BrowserRouter>
  </StrictMode>,
)
