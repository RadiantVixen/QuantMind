import { useState } from 'react'
import { submitApproval } from '../api'
import { usd } from '../format'

function ApprovalPanel({ result, onComplete }) {
  const [pending, setPending] = useState(null)
  const [error, setError] = useState('')

  if (!result?.approval_required) return null
  const req = result.approval_request ?? {}

  const decide = async (approved) => {
    setPending(approved ? 'approve' : 'reject')
    setError('')
    try {
      onComplete(await submitApproval(result.thread_id, approved))
    } catch (err) {
      setError(err.message)
    } finally {
      setPending(null)
    }
  }

  return (
    <section className="card approval-card">
      <div className="approval-text">
        <div className="approval-title">
          <span className="pulse" /> Human approval required
        </div>
        <p className="muted">
          The agents propose <strong>{req.proposed_decision}</strong> with a{' '}
          {usd(req.recommended_position_value)} position (max loss {usd(req.estimated_max_loss)}). Review
          the analysis below before you approve.
        </p>
        {error && <p className="error-text">{error}</p>}
      </div>
      <div className="approval-actions">
        <button className="btn btn-ghost" disabled={!!pending} onClick={() => decide(false)}>
          {pending === 'reject' ? <span className="spinner" /> : 'Reject'}
        </button>
        <button className="btn btn-primary" disabled={!!pending} onClick={() => decide(true)}>
          {pending === 'approve' ? <span className="spinner" /> : 'Approve'}
        </button>
      </div>
    </section>
  )
}

export default ApprovalPanel
