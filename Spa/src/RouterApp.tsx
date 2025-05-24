import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App';
import SigninOidc from './SigninOidc';
import SignoutCallbackOidc from './SignoutCallbackOidc';

export default function RouterApp() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/signin-oidc" element={<SigninOidc />} />
        <Route path="/signout-callback-oidc" element={<SignoutCallbackOidc />} />
      </Routes>
    </BrowserRouter>
  );
}
