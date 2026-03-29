/**
 * Construction OS — Control Tower Layout
 * Wave C1 — Primary application shell with construction-native sidebar
 * and routed content area. Extends existing app cleanly.
 */

import { useState } from 'react';
import { tokens } from '../ui/theme/tokens';
import { ConstructionSidebar } from './ConstructionSidebar';
import type { ControlTowerRoute } from './controlTowerTypes';

// Pages
import { ConstructionDashboard } from '../pages/dashboard/ConstructionDashboard';
import { ConstructionFoundry } from '../pages/foundry/ConstructionFoundry';
import { TruthSpine } from '../pages/spine/TruthSpine';
import { AtlasPage } from '../pages/atlas/AtlasPage';
import { AssembliesPage } from '../pages/assemblies/AssembliesPage';
import { MaterialsPage } from '../pages/materials/MaterialsPage';
import { SpecificationsPage } from '../pages/specifications/SpecificationsPage';
import { ChemistryPage } from '../pages/chemistry/ChemistryPage';
import { ScopePage } from '../pages/scope/ScopePage';
import { PatternLanguagePage } from '../pages/patterns/PatternLanguagePage';
import { RuntimePage } from '../pages/runtime/RuntimePage';
import { RegistryPage } from '../pages/registry/RegistryPage';
import { SignalsPage } from '../pages/signals/SignalsPage';
import { ReceiptsPage } from '../pages/receipts/ReceiptsPage';
import { BrandingPage } from '../pages/branding/BrandingPage';
import { MirrorBuilderPage } from '../pages/mirror-builder/MirrorBuilderPage';

const t = tokens;

/** Routes that use full-viewport layout (no padding, no scroll). */
const FULL_VIEWPORT_ROUTES: ControlTowerRoute[] = ['mirror-builder'];

function renderPage(route: ControlTowerRoute) {
  switch (route) {
    case 'dashboard':
      return <ConstructionDashboard />;
    case 'mirror-builder':
      return <MirrorBuilderPage />;
    case 'foundry':
      return <ConstructionFoundry />;
    case 'truth-spine':
      return <TruthSpine />;
    case 'atlas':
      return <AtlasPage />;
    case 'assemblies':
      return <AssembliesPage />;
    case 'materials':
      return <MaterialsPage />;
    case 'specifications':
      return <SpecificationsPage />;
    case 'chemistry':
      return <ChemistryPage />;
    case 'scope':
      return <ScopePage />;
    case 'patterns':
      return <PatternLanguagePage />;
    case 'runtime':
      return <RuntimePage />;
    case 'registry':
      return <RegistryPage />;
    case 'signals':
      return <SignalsPage />;
    case 'receipts':
      return <ReceiptsPage />;
    case 'branding':
      return <BrandingPage />;
    default:
      return <ConstructionDashboard />;
  }
}

export function ControlTowerLayout() {
  const [activeRoute, setActiveRoute] = useState<ControlTowerRoute>('dashboard');

  const isFullViewport = FULL_VIEWPORT_ROUTES.includes(activeRoute);

  return (
    <div
      style={{
        display: 'flex',
        height: '100%',
        width: '100%',
        fontFamily: t.font.family,
        overflow: 'hidden',
        background: t.color.bgBase,
        color: t.color.fgPrimary,
      }}
    >
      <ConstructionSidebar activeRoute={activeRoute} onNavigate={setActiveRoute} />
      <main
        style={{
          flex: 1,
          overflow: isFullViewport ? 'hidden' : 'auto',
          padding: isFullViewport ? 0 : '24px 32px',
          background: t.color.bgBase,
        }}
      >
        {renderPage(activeRoute)}
      </main>
    </div>
  );
}
