/**
 * Construction OS — Application Root
 *
 * Two operating surfaces:
 * 1. Workstation — multi-panel cockpit (Dockview + gravity)
 * 2. Shop Drawings — legacy document workspace layout (ported from OMNI-VIEW)
 *
 * View mode is switchable. Both surfaces share the same event bus,
 * adapter contracts, and runtime/generator seams.
 */

import { useCallback, useEffect, useState } from 'react';
import { GlobalStyles } from './ui/theme/GlobalStyles';
import { WorkspaceShell } from './ui/workspace/WorkspaceShell';
import { ShopDrawingsShell } from './ui/shop-drawings/ShopDrawingsShell';
import { InteractionProvider } from './ui/providers/InteractionProvider';

type ViewMode = 'workstation' | 'shop-drawings';

export function App() {
  const [viewMode, setViewMode] = useState<ViewMode>('workstation');

  // Set readable density mode on mount
  useEffect(() => {
    document.body.classList.remove('compact');
    document.body.classList.add('readable');
  }, []);

  const switchToWorkstation = useCallback(() => setViewMode('workstation'), []);
  const switchToShopDrawings = useCallback(() => setViewMode('shop-drawings'), []);

  return (
    <>
      <GlobalStyles />
      <InteractionProvider>
        {viewMode === 'workstation' ? (
          <WorkspaceShell onSwitchToShopDrawings={switchToShopDrawings} />
        ) : (
          <ShopDrawingsShell onSwitchToWorkstation={switchToWorkstation} />
        )}
      </InteractionProvider>
    </>
  );
}
