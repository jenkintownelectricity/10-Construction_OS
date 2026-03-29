/**
 * Mirror Builder Page — Shell integration wrapper.
 *
 * Mounts the Multi-Lens Mirror Builder into the Control Tower layout.
 * Provides a development session stub until a production session provider
 * is wired upstream.
 *
 * This page does NOT create a duplicate workstation shell.
 * It renders MirrorBuilder within the existing ControlTowerLayout viewport.
 */

import { MirrorBuilder } from '../../../apps/workstation/components/control-tower/MirrorBuilder';
import type { SessionContext } from '../../../apps/workstation/lib/mirror/mirror-state';

/**
 * Development session stub.
 * In production, this should be replaced with the real session provider
 * from the upstream authentication layer.
 *
 * Set to ADMIN for development so the Admin Mirror is accessible.
 */
const DEV_SESSION: SessionContext = {
  role: 'ADMIN',
};

export function MirrorBuilderPage() {
  return (
    <div style={{ height: '100%', width: '100%' }}>
      <MirrorBuilder session={DEV_SESSION} />
    </div>
  );
}
