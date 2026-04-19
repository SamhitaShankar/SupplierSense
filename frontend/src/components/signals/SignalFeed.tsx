import { useRunStore } from "../../store/runStore";
import { SignalCard } from "./SignalCard";

export const SignalFeed = () => {
  const state = useRunStore((s) => s.state);
  const signals = state?.raw_signals ?? [];

  return (
    <section className="signal-feed-panel">
      <div className="panel-header">
        <h2>Signal Feed</h2>
        <span className="signal-count">{signals.length} signals</span>
      </div>

      {signals.length === 0 ? (
        <div className="empty-panel">
          No signals yet. Start a run to populate the feed.
        </div>
      ) : (
        <div className="signal-feed-list">
          {signals.map((signal) => (
            <SignalCard key={signal.id} signal={signal} />
          ))}
        </div>
      )}
    </section>
  );
};