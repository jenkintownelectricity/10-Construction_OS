/**
 * Construction OS — Application Root
 *
 * Wave C1: Control Tower layout is the primary shell.
 * The original Atlas layout is preserved and accessible via the Atlas route.
 */

import { useEffect } from 'react';
import { GlobalStyles } from './ui/theme/GlobalStyles';
import { ControlTowerLayout } from './layout/ControlTowerLayout';
import { InteractionProvider } from './ui/providers/InteractionProvider';

export function App() {
  useEffect(() => {
    document.body.classList.remove('compact');
    document.body.classList.add('readable');
  }, []);

  return (
    <>
      <GlobalStyles />
      <InteractionProvider>
        <ControlTowerLayout />
      </InteractionProvider>
    </>
  );
}
