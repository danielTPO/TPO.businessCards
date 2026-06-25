import { useState } from 'react'
import ConfirmModal from './ConfirmModal'

const FIELDS = [
  {
    key: 'name',
    label: 'Full Name',
    required: true,
    placeholder: 'Alex Rivera',
    full: true,
  },
  {
    key: 'title',
    label: 'Title',
    placeholder: 'Communications Director',
  },
  {
    key: 'email',
    label: 'Email',
    type: 'email',
    required: true,
    placeholder: 'alex@tpo.group',
  },
  {
    key: 'phone',
    label: 'Phone',
    placeholder: '+1 555 000 1234',
  },
  {
    key: 'signal',
    label: 'Signal Handle',
    placeholder: 'alexrivera.01',
  },
  {
    key: 'linkedin',
    label: 'LinkedIn / QR URL',
    placeholder: 'linkedin.com/in/alexrivera',
    hint: 'Encoded as the QR code on the front of the card.',
  },
]

const INITIAL_FORM = {
  name: '',
  title: '',
  email: '',
  phone: '',
  signal: '',
  linkedin: '',
  quantity: 100,
}

function validate(form) {
  const errors = {}
  if (!form.name.trim()) {
    errors.name = 'Full name is required.'
  }
  if (!form.email.trim()) {
    errors.email = 'Email is required.'
  } else if (!form.email.trim().toLowerCase().endsWith('@tpo.group')) {
    errors.email = 'Must be a @tpo.group email address.'
  }
  const qty = Number(form.quantity)
  if (!Number.isInteger(qty) || qty < 50 || qty > 200) {
    errors.quantity = 'Quantity must be between 50 and 200.'
  }
  return errors
}

function parseApiError(data) {
  if (!data?.detail) return 'Submission failed. Please try again.'
  if (typeof data.detail === 'string') return data.detail
  if (Array.isArray(data.detail)) {
    return data.detail.map((e) => e.msg || JSON.stringify(e)).join('; ')
  }
  return 'Submission failed. Please try again.'
}

export default function OrderForm({ onSuccess, onError }) {
  const [form, setForm] = useState(INITIAL_FORM)
  const [errors, setErrors] = useState({})
  const [showConfirm, setShowConfirm] = useState(false)
  const [loading, setLoading] = useState(false)

  function set(key) {
    return (e) => {
      const value = key === 'quantity' ? Number(e.target.value) : e.target.value
      setForm((prev) => ({ ...prev, [key]: value }))
      if (errors[key]) setErrors((prev) => ({ ...prev, [key]: undefined }))
    }
  }

  function handleSubmit(e) {
    e.preventDefault()
    const errs = validate(form)
    if (Object.keys(errs).length) {
      setErrors(errs)
      return
    }
    setErrors({})
    setShowConfirm(true)
  }

  async function handleConfirmedSubmit() {
    setLoading(true)
    try {
      const res = await fetch('/api/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, email: form.email.trim() }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(parseApiError(data))
      setShowConfirm(false)
      onSuccess(data)
      setForm(INITIAL_FORM)
    } catch (err) {
      setShowConfirm(false)
      onError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <form className="order-form" onSubmit={handleSubmit} noValidate>
        {/* ── Card details ──────────────────────────── */}
        <div className="form-section">
          <h2 className="section-title">Card Details</h2>
          <div className="field-grid">
            {FIELDS.map((f) => (
              <div key={f.key} className={`field${f.full ? ' field--full' : ''}`}>
                <label htmlFor={f.key}>
                  {f.label}
                  {f.required && <span className="required">*</span>}
                </label>
                <input
                  id={f.key}
                  type={f.type || 'text'}
                  value={form[f.key]}
                  onChange={set(f.key)}
                  placeholder={f.placeholder}
                  aria-invalid={!!errors[f.key]}
                  aria-describedby={
                    errors[f.key] ? `${f.key}-error` : f.hint ? `${f.key}-hint` : undefined
                  }
                />
                {errors[f.key] && (
                  <span id={`${f.key}-error`} className="field-error" role="alert">
                    {errors[f.key]}
                  </span>
                )}
                {f.hint && !errors[f.key] && (
                  <span id={`${f.key}-hint`} className="field-hint">
                    {f.hint}
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* ── Quantity ─────────────────────────────── */}
        <div className="form-section">
          <h2 className="section-title">Order</h2>
          <div className="field field--narrow">
            <label htmlFor="quantity">
              Quantity<span className="required">*</span>
            </label>
            <input
              id="quantity"
              type="number"
              min="50"
              max="200"
              step="25"
              value={form.quantity}
              onChange={set('quantity')}
              aria-invalid={!!errors.quantity}
              aria-describedby={errors.quantity ? 'quantity-error' : 'quantity-hint'}
            />
            {errors.quantity ? (
              <span id="quantity-error" className="field-error" role="alert">
                {errors.quantity}
              </span>
            ) : (
              <span id="quantity-hint" className="field-hint">
                50–200 cards. Ships to the TPO Group Portland office.
              </span>
            )}
          </div>
        </div>

        <button type="submit" className="submit-btn">
          Submit Order →
        </button>
      </form>

      {showConfirm && (
        <ConfirmModal
          form={form}
          onConfirm={handleConfirmedSubmit}
          onCancel={() => setShowConfirm(false)}
          loading={loading}
        />
      )}
    </>
  )
}
