const API_BASE = 'http://127.0.0.1:5000'

export default function GeneratedImage({ imageUrl }) {
  if (!imageUrl) {
    return (
      <div className="image-card placeholder">
        <div className="placeholder-icon">✦</div>
        <p>Your generated face will appear here</p>
        <span>64 × 64 RGB • DCGAN</span>
      </div>
    )
  }

  const fullUrl = `${API_BASE}${imageUrl}`

  return (
    <div className="image-result">
      <div className="image-card">
        <img src={fullUrl} alt="AI generated synthetic face" />
      </div>
      <a className="download-button" href={fullUrl} download="generated-face.png">
        Download Image
      </a>
    </div>
  )
}
