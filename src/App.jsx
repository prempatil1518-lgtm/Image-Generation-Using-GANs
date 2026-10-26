import { useState } from 'react'
import GenerateButton from './components/GenerateButton'
import GeneratedImage from './components/GeneratedImage'

const API_BASE = 'http://127.0.0.1:5101'

export default function App() {
  const [imageUrl, setImageUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function generateImage() {
    setLoading(true)
    setError('')

    try {
      const response = await fetch(`${API_BASE}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      })

      const data = await response.json()
      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Unable to generate image.')
      }

      setImageUrl(`${API_BASE}${data.image_url}?t=${Date.now()}`)
    } catch (err) {
      setError(err.message || 'Unable to generate image. Please check the backend.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="app-shell">
      <section className="hero">
        <div className="badge">PYTORCH • DCGAN</div>
        <h1>AI Face Generator</h1>
        <p>Generate a new synthetic face using your trained GAN model.</p>

        <GenerateButton onClick={generateImage} loading={loading} />

        {error && <div className="error">{error}</div>}

        <div className="output-section">
          <div className="section-label">GENERATED FACE</div>
          <GeneratedImage imageUrl={imageUrl} />
        </div>
      </section>

      <footer>
        <span>Trained DCGAN</span>
        <span>64 × 64 RGB</span>
        <span>Latent Vector: 100</span>
      </footer>
    </main>
  )
}
