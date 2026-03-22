/**
 * Construction OS — Application Root
 *
 * Primary shell: Construction Atlas layout with sidebar navigation.
 * The Workstation cockpit and Shop Drawings viewer are embedded as
 * pages within the Atlas layout (Tools and Viewer nav items).
 */

import { useEffect } from 'react';
import { GlobalStyles } from './ui/theme/GlobalStyles';
import { AtlasLayout } from './ui/atlas/AtlasLayout';
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
        <AtlasLayout />
      </InteractionProvider>
    </>
  );
}
