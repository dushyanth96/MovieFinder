import { useEffect } from "react";
import { useMovieContext } from "../contexts/MovieContext";

const ProtectedRoute = ({ children }) => {
  const { user, setShowLoginModal } = useMovieContext();

  useEffect(() => {
    if (!user) {
      setShowLoginModal(true);
    }
  }, [user, setShowLoginModal]);

  if (!user) {
    return null;
  }

  return children;
};

export default ProtectedRoute;
