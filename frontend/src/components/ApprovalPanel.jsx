import { useState } from 'react'
import api from '../api'

function ApprovalPanel({ result, onComplete }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  if (!result?.approval_required) return null

  const handleApproval = async (approved) => {
    setLoading(true)
    setError('')

    try {
      const response = await api.post('/approval/', {
        thread_id: result.thread_id,
        approved,
      })

      onComplete(response.data)
    } catch (err) {
      setError(err.response?.data?.error || 'Approval failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section>
      <h2>Human Approval Required</h2>

      <p>Proposed decision: {result.approval_request.proposed_decision}</p>
      <p>Risk level: {result.approval_request.risk_level}</p>
      <p>
        Recommended position: $
        {result.approval_request.recommended_position_value}
      </p>
      <p>
        Estimated maximum loss: $
        {result.approval_request.estimated_max_loss}
      </p>

      <button disabled={loading} onClick={() => handleApproval(true)}>
        Approve
      </button>

      <button disabled={loading} onClick={() => handleApproval(false)}>
        Reject
      </button>

      {loading && <p>Processing...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </section>
  )
}

export default ApprovalPanel