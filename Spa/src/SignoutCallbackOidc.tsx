import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { userManager } from './auth.service';

export default function SignoutCallbackOidc() {
  const navigate = useNavigate();
  useEffect(() => {
    userManager.signoutRedirectCallback()
      .then(() => {
        navigate('/', { replace: true });
      })
      .catch(() => {
        navigate('/', { replace: true });
      });
  }, [navigate]);
  return <div>Signing out...</div>;
}
