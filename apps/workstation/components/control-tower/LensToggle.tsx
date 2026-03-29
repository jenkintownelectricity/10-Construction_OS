import { LENS_TYPES, type LensType, useLens } from "../../lib/mirror";

const LENS_OPTIONS: { key: LensType; label: string }[] = [
  { key: LENS_TYPES.BUYER, label: "Buyer" },
  { key: LENS_TYPES.INVESTOR, label: "Investor" },
  { key: LENS_TYPES.ENGINEERING, label: "Engineering" },
];

const LENS_COLORS: Record<LensType, string> = {
  [LENS_TYPES.BUYER]: "#22c55e",
  [LENS_TYPES.INVESTOR]: "#3b82f6",
  [LENS_TYPES.ENGINEERING]: "#a855f7",
  [LENS_TYPES.ADMIN]: "#eab308",
};

export function LensToggle() {
  const { activeLens, setLens, isAdminVisible } = useLens();

  const allOptions = isAdminVisible
    ? [...LENS_OPTIONS, { key: LENS_TYPES.ADMIN, label: "Admin" }]
    : LENS_OPTIONS;

  return (
    <div
      style={{
        display: "flex",
        gap: 4,
        background: "#0f172a",
        borderRadius: 6,
        padding: 3,
        border: "1px solid #1e293b",
      }}
      role="radiogroup"
      aria-label="Lens selector"
    >
      {allOptions.map((opt) => {
        const isActive = activeLens === opt.key;
        const color = LENS_COLORS[opt.key];
        return (
          <button
            key={opt.key}
            role="radio"
            aria-checked={isActive}
            onClick={() => setLens(opt.key)}
            style={{
              padding: "4px 12px",
              fontSize: 11,
              fontFamily: "monospace",
              fontWeight: isActive ? 700 : 400,
              color: isActive ? "#0f172a" : "#94a3b8",
              background: isActive ? color : "transparent",
              border: "none",
              borderRadius: 4,
              cursor: "pointer",
              transition: "all 150ms ease",
              letterSpacing: 0.5,
            }}
          >
            {opt.label}
          </button>
        );
      })}
    </div>
  );
}
