// Static example card — illustrates the printed output layout.
// Uses fixed sample data; not connected to the form.

const BARS = [32, 58, 76, 50, 92, 68, 44, 72, 54]

// QR code finder-pattern SVG (mimics actual QR output)
function QrSvg() {
  return (
    <svg viewBox="0 0 25 25" style={{ width: '100%', height: '100%', display: 'block' }}>
      <rect width="25" height="25" fill="white" />

      {/* Top-left finder */}
      <rect x="0" y="0" width="7" height="7" fill="#06371F" />
      <rect x="1" y="1" width="5" height="5" fill="white" />
      <rect x="2" y="2" width="3" height="3" fill="#06371F" />

      {/* Top-right finder */}
      <rect x="18" y="0" width="7" height="7" fill="#06371F" />
      <rect x="19" y="1" width="5" height="5" fill="white" />
      <rect x="20" y="2" width="3" height="3" fill="#06371F" />

      {/* Bottom-left finder */}
      <rect x="0" y="18" width="7" height="7" fill="#06371F" />
      <rect x="1" y="19" width="5" height="5" fill="white" />
      <rect x="2" y="20" width="3" height="3" fill="#06371F" />

      {/* Timing strip (horizontal) */}
      <rect x="8"  y="6" width="1" height="1" fill="#06371F" />
      <rect x="10" y="6" width="1" height="1" fill="#06371F" />
      <rect x="12" y="6" width="1" height="1" fill="#06371F" />
      <rect x="14" y="6" width="1" height="1" fill="#06371F" />
      <rect x="16" y="6" width="1" height="1" fill="#06371F" />

      {/* Timing strip (vertical) */}
      <rect x="6" y="8"  width="1" height="1" fill="#06371F" />
      <rect x="6" y="10" width="1" height="1" fill="#06371F" />
      <rect x="6" y="12" width="1" height="1" fill="#06371F" />
      <rect x="6" y="14" width="1" height="1" fill="#06371F" />
      <rect x="6" y="16" width="1" height="1" fill="#06371F" />

      {/* Data cells */}
      <rect x="8"  y="8"  width="1" height="1" fill="#06371F" />
      <rect x="10" y="8"  width="1" height="1" fill="#06371F" />
      <rect x="14" y="8"  width="1" height="1" fill="#06371F" />
      <rect x="16" y="8"  width="1" height="1" fill="#06371F" />
      <rect x="8"  y="10" width="1" height="1" fill="#06371F" />
      <rect x="12" y="10" width="1" height="1" fill="#06371F" />
      <rect x="16" y="10" width="1" height="1" fill="#06371F" />
      <rect x="10" y="12" width="1" height="1" fill="#06371F" />
      <rect x="14" y="12" width="1" height="1" fill="#06371F" />
      <rect x="8"  y="14" width="1" height="1" fill="#06371F" />
      <rect x="12" y="14" width="1" height="1" fill="#06371F" />
      <rect x="16" y="14" width="1" height="1" fill="#06371F" />
      <rect x="10" y="16" width="1" height="1" fill="#06371F" />
      <rect x="14" y="16" width="1" height="1" fill="#06371F" />
      <rect x="18" y="8"  width="1" height="1" fill="#06371F" />
      <rect x="20" y="10" width="1" height="1" fill="#06371F" />
      <rect x="22" y="8"  width="1" height="1" fill="#06371F" />
      <rect x="22" y="12" width="1" height="1" fill="#06371F" />
      <rect x="18" y="14" width="1" height="1" fill="#06371F" />
      <rect x="20" y="16" width="1" height="1" fill="#06371F" />
      <rect x="8"  y="18" width="1" height="1" fill="#06371F" />
      <rect x="12" y="18" width="1" height="1" fill="#06371F" />
      <rect x="16" y="18" width="1" height="1" fill="#06371F" />
      <rect x="10" y="20" width="1" height="1" fill="#06371F" />
      <rect x="14" y="22" width="1" height="1" fill="#06371F" />
      <rect x="18" y="20" width="1" height="1" fill="#06371F" />
      <rect x="22" y="18" width="1" height="1" fill="#06371F" />
      <rect x="20" y="22" width="1" height="1" fill="#06371F" />
      <rect x="24" y="20" width="1" height="1" fill="#06371F" />
    </svg>
  )
}

export default function CardPreview() {
  return (
    <div>
      <p style={{ fontSize: 12, color: 'var(--ink-muted)', marginBottom: 16 }}>
        Sample output — your card will match this layout with your details.
      </p>

      <div className="preview-cards">
        {/* ── Front face ──────────────────────────── */}
        <div className="preview-card-wrap">
          <span className="preview-label">Front</span>
          <div className="card-face" style={{ background: 'white' }}>

            {/* Left column: bars logo */}
            <div style={{ width: '41%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'flex-end', gap: '2.5px', width: '76%', height: '52%' }}>
                {BARS.map((h, i) => (
                  <div key={i} style={{ flex: 1, height: `${h}%`, background: '#0E8E54', borderRadius: '1.5px 1.5px 0 0' }} />
                ))}
              </div>
            </div>

            {/* Emerald vertical divider */}
            <div style={{ width: 1, flexShrink: 0, background: '#0E8E54', margin: '10px 0' }} />

            {/* Right column */}
            <div style={{ flex: 1, padding: '12px 8px 16px 10px', display: 'flex', flexDirection: 'column', position: 'relative', overflow: 'hidden' }}>
              <div style={{ fontFamily: 'Georgia, serif', fontSize: 13, fontWeight: 700, color: '#06371F', lineHeight: 1.2 }}>
                Alex Rivera
              </div>
              <div style={{ fontSize: 7.5, color: '#3D5449', marginTop: 2 }}>
                Policy Director
              </div>

              {/* QR code */}
              <div style={{ position: 'absolute', right: 8, top: 42, width: 44, height: 44 }}>
                <QrSvg />
              </div>

              {/* Contact block */}
              <div style={{ position: 'absolute', bottom: 14, left: 10, right: 58, display: 'flex', flexDirection: 'column', gap: 2 }}>
                <div style={{ fontSize: 7.5, color: '#3D5449' }}>+1 555 012 3456</div>
                <div style={{ fontSize: 7.5, color: '#3D5449' }}>alex@tpo.group</div>
                <div style={{ fontSize: 7.5, color: '#3D5449' }}>Signal: alexrivera.01</div>
              </div>
            </div>

            {/* Bottom emerald rule */}
            <div style={{ position: 'absolute', bottom: 5, left: 0, right: 0, height: 1, background: '#0E8E54' }} />
          </div>
        </div>

        {/* ── Back face ───────────────────────────── */}
        <div className="preview-card-wrap">
          <span className="preview-label">Back</span>
          <div
            className="card-face"
            style={{ background: '#0E8E54', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 6 }}
          >
            <div style={{ fontFamily: 'Georgia, serif', fontSize: 18, color: 'white', fontWeight: 600, letterSpacing: '0.01em' }}>
              TPO.group
            </div>
            <div style={{ fontSize: 5.5, color: 'rgba(200,230,215,0.9)', letterSpacing: '0.14em', fontWeight: 600 }}>
              TECHNOLOGY. POLICY. OPERATIONS.
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
