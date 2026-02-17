import './css/App.css'
import Home from './pages/Home';
import LoginModal from './components/LoginModal';
import { Routes, Route } from 'react-router-dom';
import Favorites from './pages/Favorites';
import NavBar from './components/NavBar';
import { useMovieContext } from './contexts/MovieContext';
import ProtectedRoute from './components/ProtectedRoute';
function App() {
  const { showLoginModal } = useMovieContext();

  return (
    <>
      <NavBar />

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/favorites" element={<ProtectedRoute><Favorites /></ProtectedRoute>} />
        </Routes>
      </main>

      {/* Global Login Modal */}
      {showLoginModal && <LoginModal />}
    </>
  )
}

export default App
