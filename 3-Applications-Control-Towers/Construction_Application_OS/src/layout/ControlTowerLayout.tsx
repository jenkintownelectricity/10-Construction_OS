/**
 * Construction OS — Control Tower Layout
 * Wave C1 + VTI Absorption + Manufacturer Hub — Primary application shell with grouped sidebar
 * navigation and routed content area for all absorbed control tower surfaces.
 */

import { useState } from 'react';
import { tokens } from '../ui/theme/tokens';
import { ConstructionSidebar } from './ConstructionSidebar';
import type { ControlTowerRoute } from './controlTowerTypes';

// Core
import { ConstructionDashboard } from '../pages/dashboard/ConstructionDashboard';
import { MirrorBuilderPage } from '../pages/mirror-builder/MirrorBuilderPage';

// Foundry
import { ConstructionFoundry } from '../pages/foundry/ConstructionFoundry';
import { BirthPlannerPage } from '../pages/birth-planner/BirthPlannerPage';
import { KernelsPage } from '../pages/kernels/KernelsPage';

// Atlas
import { AtlasPage } from '../pages/atlas/AtlasPage';
import { TopologyPage } from '../pages/topology/TopologyPage';
import { AssembliesPage } from '../pages/assemblies/AssembliesPage';

// Runtime
import { RuntimePage } from '../pages/runtime/RuntimePage';
import { EnginesPage } from '../pages/engines/EnginesPage';
import { SignalsPage } from '../pages/signals/SignalsPage';
import { CapabilitiesPage } from '../pages/capabilities/CapabilitiesPage';

// Governance
import { GovernancePage } from '../pages/governance/GovernancePage';
import { ContractsPage } from '../pages/contracts/ContractsPage';
import { DoctrinePage } from '../pages/doctrine/DoctrinePage';
import { TruthSpine } from '../pages/spine/TruthSpine';

// Registry
import { RegistryPage } from '../pages/registry/RegistryPage';
import { ReceiptsPage } from '../pages/receipts/ReceiptsPage';
import { MirrorsPage } from '../pages/mirrors/MirrorsPage';

// Platform
import { ViewerPage } from '../pages/viewer/ViewerPage';
import { PlansPage } from '../pages/plans/PlansPage';
import { MaterialsPage } from '../pages/materials/MaterialsPage';
import { SpecificationsPage } from '../pages/specifications/SpecificationsPage';
import { ChemistryPage } from '../pages/chemistry/ChemistryPage';
import { ScopePage } from '../pages/scope/ScopePage';
import { PatternLanguagePage } from '../pages/patterns/PatternLanguagePage';
import { BarrettPMMAGeneratorPage } from '../pages/pmma-generator/BarrettPMMAGeneratorPage';
import { ManufacturerHubPage } from '../pages/manufacturers/ManufacturerHubPage';

// Admin
import { BrandingPage } from '../pages/branding/BrandingPage';
import { AdminPage } from '../pages/admin/AdminPage';

const t = tokens;

/** Routes that use full-viewport layout (no padding, no scroll). */
const FULL_VIEWPORT_ROUTES: ControlTowerRoute[] = ['mirror-builder', 'manufacturers'];

function renderPage(route: ControlTowerRoute) {
  switch (route) {
    // Core
    case 'dashboard':
      return <ConstructionDashboard />;
    case 'mirror-builder':
      return <MirrorBuilderPage />;

    // Foundry
    case 'foundry':
      return <ConstructionFoundry />;
    case 'birth-planner':
      return <BirthPlannerPage />;
    case 'kernels':
      return <KernelsPage />;

    // Atlas
    case 'atlas':
      return <AtlasPage />;
    case 'topology':
      return <TopologyPage />;
    case 'assemblies':
      return <AssembliesPage />;

    // Runtime
    case 'runtime':
      return <RuntimePage />;
    case 'engines':
      return <EnginesPage />;
    case 'signals':
      return <SignalsPage />;
    case 'capabilities':
      return <CapabilitiesPage />;

    // Governance
    case 'governance':
      return <GovernancePage />;
    case 'contracts':
      return <ContractsPage />;
    case 'doctrine':
      return <DoctrinePage />;
    case 'truth-spine':
      return <TruthSpine />;

    // Registry
    case 'registry':
      return <RegistryPage />;
    case 'receipts':
      return <ReceiptsPage />;
    case 'mirrors':
      return <MirrorsPage />;

    // Platform
    case 'viewer':
      return <ViewerPage />;
    case 'plans':
      return <PlansPage />;
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
    case 'pmma-generator':
      return <BarrettPMMAGeneratorPage />;
    case 'manufacturers':
      return <ManufacturerHubPage />;

    // Admin
    case 'branding':
      return <BrandingPage />;
    case 'admin':
      return <AdminPage />;

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
