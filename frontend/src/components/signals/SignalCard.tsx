import type { SignalEvent } from "../../store/runStore";

type SignalCardProps = {
  signal: SignalEvent;
};

const getSeverityPercent = (severity: number) => {
  const clamped = Math.max(0, Math.min(1, severity));
  return `${clamped * 100}%`;
};

const getSeverityLabel = (severity: number) => {
  if (severity >= 0.75) return "High";
  if (severity >= 0.4) return "Medium";
  return "Low";
};

export const SignalCard = ({ signal }: SignalCardProps) => {
  return (
    <div className="signal-card">
      <div className="signal-card-header">
        <span className="signal-type">{signal.type}</span>
        <span className="signal-severity-label">
          {getSeverityLabel(signal.severity)}
        </span>
      </div>

      <div className="severity-bar-container">
        <div
          className="severity-bar-fill"
          style={{ width: getSeverityPercent(signal.severity) }}
        />
      </div>

      <p className="signal-raw-text">{signal.raw_text}</p>

      <div className="signal-meta">
        <div><strong>Source:</strong> {signal.source}</div>
        <div><strong>Region:</strong> {signal.affected_region}</div>
        <div><strong>Time:</strong> {signal.timestamp}</div>
      </div>

      <div className="signal-tags">
        {signal.affected_commodities?.map((commodity) => (
          <span key={commodity} className="commodity-tag">
            {commodity}
          </span>
        ))}
      </div>
    </div>
  );
};