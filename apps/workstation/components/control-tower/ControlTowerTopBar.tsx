import { LensToggle } from "./LensToggle";

export function ControlTowerTopBar() {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "8px 16px",
        borderBottom: "1px solid #1e293b",
        background: "#0f172a",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <span
          style={{
            fontSize: 13,
            fontWeight: 700,
            fontFamily: "monospace",
            color: "#e2e8f0",
            letterSpacing: 1,
            textTransform: "uppercase",
          }}
        >
          Control Tower
        </span>
        <span
          style={{
            fontSize: 10,
            color: "#64748b",
            fontFamily: "monospace",
          }}
        >
          Multi-Lens Mirror Builder
        </span>
      </div>

      {/* Lens toggle positioned right side of main header row */}
      <LensToggle />
    </div>
  );
}
