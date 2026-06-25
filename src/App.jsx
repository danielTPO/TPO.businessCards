import { useState } from 'react'
import OrderForm from './components/OrderForm'
import CardPreview from './components/CardPreview'
import StatusBanner from './components/StatusBanner'
import './styles/global.css'

export default function App() {
  const [status, setStatus] = useState(null)

  return (
    <div>
      <header className="app-header">
        <div className="app-header-inner">
          <p className="eyebrow">TPO Group</p>
          <h1>Business Card Order</h1>
        </div>
      </header>

      <main className="app-main">
        {status && (
          <StatusBanner
            type={status.type}
            message={status.message}
            reference={status.reference}
            onDismiss={() => setStatus(null)}
          />
        )}
        <div className="form-section" style={{ marginBottom: 28 }}>
          <h2 className="section-title">Example Card</h2>
          <CardPreview />
        </div>

        <OrderForm
          onSuccess={(data) =>
            setStatus({
              type: 'success',
              message: 'Your order has been submitted to Cloudprinter and will ship to the Portland office.',
              reference: data.reference,
            })
          }
          onError={(msg) =>
            setStatus({ type: 'error', message: msg })
          }
        />
      </main>
    </div>
  )
}
