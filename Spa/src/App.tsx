import { useEffect, useState } from 'react'
import { fetchWeatherForecast, type WeatherForecast } from './weather.service'
import { userManager } from './auth.service'
import { User } from 'oidc-client-ts'
import './App.css'

function App() {
  const [weather, setWeather] = useState<WeatherForecast[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    userManager.getUser().then(setUser);
  }, []);

  useEffect(() => {
    if (user && user.access_token) {
      fetchWeatherForecast(user.access_token)
        .then(setWeather)
        .catch(e => setError(e.message))
        .finally(() => setLoading(false));
    }
  }, [user]);

  const login = () => userManager.signinRedirect();
  const logout = () => userManager.signoutRedirect();

  if (!user) {
    return <button onClick={login}>Login</button>;
  }

  return (
    <div style={{ padding: '2em', fontFamily: 'sans-serif' }}>
      <button onClick={logout} style={{ float: 'right' }}>Logout</button>
      <h1>Weather Forecast Demo</h1>
      {loading && <p>Loading...</p>}
      {error && <p style={{color: 'red'}}>Error: {error}</p>}
      {weather && (
        <table style={{margin: '1em 0', borderCollapse: 'collapse', width: '100%'}}>
          <thead>
            <tr>
              <th>Date</th>
              <th>Temp (°C)</th>
              <th>Temp (°F)</th>
              <th>Summary</th>
            </tr>
          </thead>
          <tbody>
            {weather.map((w, i) => (
              <tr key={i}>
                <td>{w.date}</td>
                <td>{w.temperatureC}</td>
                <td>{w.temperatureF}</td>
                <td>{w.summary}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default App
