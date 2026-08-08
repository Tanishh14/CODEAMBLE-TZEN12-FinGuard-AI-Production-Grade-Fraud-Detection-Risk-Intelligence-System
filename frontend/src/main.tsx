import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles/index.css'
import { useAuthStore } from './auth/auth.store'

// Initializing auth from localStorage on app starrt
useAuthStore.getState().initializeFromStorage()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
