/**
 * Construction OS — Application Root
 *
 * Mounts the workspace shell at the /workspace route.
 * Preserves existing paths (this repo had no prior routes).
 * The workspace is the primary operating surface — not a page.
 */

import { GlobalStyles } from './ui/theme/GlobalStyles';
import { WorkspaceShell } from './ui/workspace/WorkspaceShell';

export function App() {
  return (
    <>
      <GlobalStyles />
      <WorkspaceShell />
    </>
  );
}
