export default function ConfirmModal({ form, onConfirm, onCancel, loading }) {
  const rows = [
    { label: 'Name',       value: form.name },
    { label: 'Title',      value: form.title || null },
    { label: 'Email',      value: form.email },
    { label: 'Phone',      value: form.phone || null },
    { label: 'Signal',     value: form.signal || null },
    { label: 'QR URL',     value: form.linkedin || null },
    { label: 'Quantity',   value: `${form.quantity} cards` },
    { label: 'Ships to',   value: 'TPO Group — 5 Moulton St 6th FL, Portland ME 04101' },
  ]

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal" onClick={(e) => e.stopPropagation()} role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <h2 id="modal-title" className="modal-title">Confirm your order</h2>
        <p className="modal-subtitle">Please review your details before placing the order.</p>

        <dl className="modal-details">
          {rows.filter((r) => r.value).map((r) => (
            <div key={r.label} className="modal-detail-row">
              <dt>{r.label}</dt>
              <dd>{r.value}</dd>
            </div>
          ))}
        </dl>

        <div className="modal-actions">
          <button className="btn-ghost" onClick={onCancel} disabled={loading}>
            Go Back
          </button>
          <button className="submit-btn" onClick={onConfirm} disabled={loading}>
            {loading ? <span className="spinner" aria-label="Submitting…" /> : 'Place Order →'}
          </button>
        </div>
      </div>
    </div>
  )
}
