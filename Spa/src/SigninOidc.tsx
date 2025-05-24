import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { userManager } from './auth.service';

export default function SigninOidc() {
  const navigate = useNavigate();
  useEffect(() => {
    userManager.signinRedirectCallback()
      .then(() => {
        navigate('/', { replace: true });
      })
      .catch(() => {
        navigate('/', { replace: true });
      });
  }, [navigate]);
  return <div>Signing in...</div>;
}
