import { useState } from 'react'

const FIELDS = [
  {
    key: 'name',
    label: 'Full Name',
    required: true,
    placeholder: 'Daniel Landry',
    full: true,
  },
  {
    key: 'title',
    label: 'Title',
    placeholder: 'Intern',
  },
  {
    key: 'email',
    label: 'Email',
    type: 'email',
    required: true,
    placeholder: 'd@tpo.group',
  },
  {
    key: 'phone',
    label: 'Phone',
    placeholder: '+1 207 555 0100',
  },
  {
    key: 'signal',
    label: 'Signal Handle',
    placeholder: 'daniellandry',
  },
  {
    key: 'linkedin',
    label: 'LinkedIn / QR URL',
    placeholder: 'linkedin.com/in/daniellandry',
    hint: 'Encoded as the QR code on the front of the card.',
  },
]

function validate(form) {
  const errors = {}
  if (!form.name.trim()) {
    errors.name = 'Full name is required.'
  }
  if (!form.email.trim()) {
    errors.email = 'Email is required.'
  } else if (!/^[^@]+@[^@]+\.[^@]+$/.test(form.email)) {
    errors.email = 'Enter a valid email address.'
  }
  const qty = Number(form.quantity)
  if (!Number.isInteger(qty) || qty < 50 || qty > 5000) {
    errors.quantity = 'Quantity must be a whole number between 50 and 5,000.'
  }
  return errors
}

export default function OrderForm({ onSuccess, onError }) {
  const [form, setForm] = useState({
    name: '',
    title: '',
    email: '',
    phone: '',
    signal: '',
    linkedin: '',
    quantity: 250,
  })
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)

  function set(key) {
    return (e) => {
      const value = key === 'quantity' ? Number(e.target.value) : e.target.value
      setForm((prev) => ({ ...prev, [key]: value }))
      if (errors[key]) {
        setErrors((prev) => ({ ...prev, [key]: undefined }))
      }
    }
  }

  async function handleSubmit(e) {
    e.preventDefault()
    const errs = validate(form)
    if (Object.keys(errs).length) {
      setErrors(errs)
      return
    }
    setErrors({})
    setLoading(true)
    try {
      const res = await fetch('/api/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.detail || 'Submission failed. Please try again.')
      }
      onSuccess(data)
      setForm({ name: '', title: '', email: '', phone: '', signal: '', linkedin: '', quantity: 250 })
    } catch (err) {
      onError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form className="order-form" onSubmit={handleSubmit} noValidate>
      <div className="form-section">
        <h2 className="section-title">Card Details</h2>
        <div className="field-grid">
          {FIELDS.map((f) => (
            <div
              key={f.key}
              className={`field${f.full ? ' field--full' : ''}`}
            >
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
                  errors[f.key]
                    ? `${f.key}-error`
                    : f.hint
                    ? `${f.key}-hint`
                    : undefined
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
            max="5000"
            step="50"
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
              Cards ship to the TPO Group Portland office.
            </span>
          )}
        </div>
      </div>

      <button type="submit" className="submit-btn" disabled={loading}>
        {loading ? <span className="spinner" aria-label="Submitting…" /> : 'Submit Order →'}
      </button>
    </form>
  )
}
