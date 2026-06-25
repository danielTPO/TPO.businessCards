export default function StatusBanner({ type, message, reference, onDismiss }) {
  return (
    <div className={`status-banner status-banner--${type}`} role="alert">
      <div className="status-banner-body">
        <strong>{type === 'success' ? 'Order submitted' : 'Something went wrong'}</strong>
        <p>{message}</p>
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
