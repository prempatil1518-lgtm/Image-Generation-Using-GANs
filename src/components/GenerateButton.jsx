export default function GenerateButton({ onClick, loading }) {
  return (
    <button className="generate-button" onClick={onClick} disabled={loading}>
      {loading ? <><span className="spinner" /> Generating...</> : 'Generate Image'}
    </button>
  )
}
