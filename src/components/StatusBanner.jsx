export default function StatusBanner({ type, message, reference, onDismiss }) {
  return (
    <div className={`status-banner status-banner--${type}`} role="alert">
      <div className="status-banner-body">
        <strong>{type === 'success' ? 'Order submitted' : 'Something went wrong'}</strong>
        {message.includes('\n') ? (
          <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit', fontSize: 13, margin: '4px 0 0', lineHeight: 1.5 }}>{message}</pre>
        ) : (
          <p>{message}</p>
        )}
        {reference && (
          <p className="status-ref">
            Reference: <code>{reference}</code>
          </p>
        )}
      </div>
      <button
        className="status-dismiss"
        onClick={onDismiss}
        aria-label="Dismiss notification"
      >
        ×
      </button>
    </div>
  )
}
