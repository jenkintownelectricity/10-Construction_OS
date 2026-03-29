import { createContext, useContext, useState, useCallback, type ReactNode } from "react";
import { LENS_TYPES, type LensType, type SessionContext } from "./mirror-state";

interface LensContextValue {
  activeLens: LensType;
  setLens: (lens: LensType) => void;
  session: SessionContext;
  isAdminVisible: boolean;
}

const LensContext = createContext<LensContextValue | null>(null);

export function useLens(): LensContextValue {
  const ctx = useContext(LensContext);
  if (!ctx) {
    throw new Error("useLens must be used within a LensProvider");
  }
  return ctx;
}

interface LensProviderProps {
  children: ReactNode;
  session: SessionContext;
  initialLens?: LensType;
}

export function LensProvider({ children, session, initialLens }: LensProviderProps) {
  const [activeLens, setActiveLens] = useState<LensType>(initialLens ?? LENS_TYPES.BUYER);

  const setLens = useCallback((lens: LensType) => {
    setActiveLens(lens);
  }, []);

  const isAdminVisible = session.role === "ADMIN";

  return (
    <LensContext.Provider value={{ activeLens, setLens, session, isAdminVisible }}>
      {children}
    </LensContext.Provider>
  );
}
