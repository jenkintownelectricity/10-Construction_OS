/**
 * Construction OS — Application Root
 *
 * Mounts the workspace shell at the /workspace route.
 * Preserves existing paths (this repo had no prior routes).
 * The workspace is the primary operating surface — not a page.
 *
 * Sets readable density mode as default for desktop.
 */

import { useEffect } from 'react';
import { GlobalStyles } from './ui/theme/GlobalStyles';
import { WorkspaceShell } from './ui/workspace/WorkspaceShell';
import { InteractionProvider } from './ui/providers/InteractionProvider';

export function App() {
  // Set readable density mode on mount
  useEffect(() => {
    document.body.classList.remove('compact');
    document.body.classList.add('readable');
  }, []);

  return (
    <>
      <GlobalStyles />
      <InteractionProvider>
        <WorkspaceShell />
      </InteractionProvider>
    </>
  );
}
