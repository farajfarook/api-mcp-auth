export interface WeatherForecast {
  date: string; // ISO string
  temperatureC: number;
  temperatureF: number;
  summary: string | null;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

export async function fetchWeatherForecast(): Promise<WeatherForecast[]> {
  const res = await fetch(`${API_BASE_URL}/weatherforecast`);
  if (!res.ok) throw new Error('API error');
  return res.json();
}
