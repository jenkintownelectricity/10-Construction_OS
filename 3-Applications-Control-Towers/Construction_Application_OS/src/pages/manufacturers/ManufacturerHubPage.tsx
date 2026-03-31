/**
 * Manufacturer Hub — Page Shell
 * Wave 1 UI Surface
 *
 * Three-column layout:
 *   Left rail: Manufacturer sidebar
 *   Center workspace: Mode-dependent main panels (WORK | SYSTEM)
 *   Right rail: Governance / Action / Signals
 *
 * Dual-surface mode:
 *   WORK = light office surface for submittal/admin/review
 *   SYSTEM = dark visualization surface for system reasoning
 *
 * All data is observer-derived projection. No canonical truth is
 * created or mutated by this UI surface.
 */

import { useState } from 'react';
import { tokens } from '../../ui/theme/tokens';
import type { ManufacturerHubMode } from '../../lib/manufacturers/manufacturerHubTypes';
import { DEFAULT_HUB_MODE, getSurfaceTokens } from '../../lib/manufacturers/manufacturerHubMode';
import { MANUFACTURER_HUB_PROJECTION } from '../../lib/manufacturers/manufacturerHubObserverProjection';
import type { UISignal } from '../../lib/manufacturers/manufacturerHubTypes';

// WORK mode panels
import { ManufacturerModeSwitch } from './components/ManufacturerModeSwitch';
import { ManufacturerSidebar } from './components/ManufacturerSidebar';
import { ManufacturerHeader } from './components/ManufacturerHeader';
import { ManufacturerOverviewPanel } from './components/ManufacturerOverviewPanel';
import { ManufacturerProductsPanel } from './components/ManufacturerProductsPanel';
import { ManufacturerSystemsPanel } from './components/ManufacturerSystemsPanel';

// SYSTEM mode panels
import { SystemInspectorPanel } from './components/SystemInspectorPanel';
import { CertificationPanel } from './components/CertificationPanel';
import { ConditionCompatibilityPanel } from './components/ConditionCompatibilityPanel';
import { RuleChecklistPanel } from './components/RuleChecklistPanel';
import { ProductStackPanel } from './components/ProductStackPanel';

// Governance / Action / Signals
import { GovernanceActionRail } from './components/GovernanceActionRail';
import { ManufacturerSignalsPanel } from './components/ManufacturerSignalsPanel';

const t = tokens;
const projection = MANUFACTURER_HUB_PROJECTION;

export function ManufacturerHubPage() {
  const [mode, setMode] = useState<ManufacturerHubMode>(DEFAULT_HUB_MODE);
  const [selectedManufacturerId, setSelectedManufacturerId] = useState<string>('barrett');
  const [selectedSystemId, setSelectedSystemId] = useState<string | null>('barrett-hyppocoat-trafficable');
  const [signals, setSignals] = useState<UISignal[]>([
    { type: 'MANUFACTURER_SELECTED', label: 'Barrett Company selected', active: true },
    { type: 'MODE_CHANGED', label: `Mode: WORK`, active: true },
    { type: 'SYSTEM_SELECTED', label: 'HyppoCoat Trafficable System selected', active: true },
    { type: 'CERTIFICATION_VIEWED', label: 'Certification panel viewed', active: false },
    { type: 'PRODUCT_VIEWED', label: 'Product detail viewed', active: false },
  ]);

  const surface = getSurfaceTokens(mode);
  const manufacturer = projection.manufacturers.find(m => m.id === selectedManufacturerId);
  const products = projection.products.filter(p => p.manufacturerId === selectedManufacturerId);
  const systems = projection.systems.filter(s => s.manufacturerId === selectedManufacturerId);
  const selectedSystem = selectedSystemId ? projection.systems.find(s => s.id === selectedSystemId) : null;
  const systemCertifications = selectedSystem
    ? projection.certifications.filter(c => c.systemId === selectedSystem.id)
    : [];
  const systemConditions = selectedSystem
    ? projection.conditionsSummary.filter(c => c.systemId === selectedSystem.id)
    : [];
  const systemRules = selectedSystem
    ? projection.rulesSummary.filter(r => r.systemId === selectedSystem.id)
    : [];
  const systemProducts = selectedSystem
    ? projection.products.filter(p => selectedSystem.productIds.includes(p.id))
    : [];
  const governance = projection.governanceStatus[selectedManufacturerId];

  const handleSelectManufacturer = (id: string) => {
    setSelectedManufacturerId(id);
    const mfgSystems = projection.systems.filter(s => s.manufacturerId === id);
    setSelectedSystemId(mfgSystems.length > 0 ? mfgSystems[0].id : null);
    const mfg = projection.manufacturers.find(m => m.id === id);
    setSignals(prev => prev.map(s =>
      s.type === 'MANUFACTURER_SELECTED'
        ? { ...s, label: `${mfg?.name || id} selected`, active: true }
        : s
    ));
  };

  const handleSelectSystem = (id: string) => {
    setSelectedSystemId(id);
    const sys = projection.systems.find(s => s.id === id);
    setSignals(prev => prev.map(s =>
      s.type === 'SYSTEM_SELECTED'
        ? { ...s, label: `${sys?.name || id} selected`, active: true }
        : s
    ));
  };

  const handleModeChange = (newMode: ManufacturerHubMode) => {
    setMode(newMode);
    setSignals(prev => prev.map(s =>
      s.type === 'MODE_CHANGED'
        ? { ...s, label: `Mode: ${newMode.toUpperCase()}`, active: true }
        : s
    ));
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      width: '100%',
      overflow: 'hidden',
      background: surface.bg,
      color: surface.fg,
      fontFamily: t.font.family,
    }}>
      {/* Top bar with title and mode switch */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '16px 24px',
        borderBottom: `1px solid ${surface.border}`,
        background: surface.bgElevated,
        flexShrink: 0,
      }}>
        <div>
          <h1 style={{
            margin: 0,
            fontSize: t.font.sizeXl,
            fontWeight: Number(t.font.weightBold),
            lineHeight: t.font.lineTight,
            color: surface.fg,
          }}>
            Manufacturer Hub
          </h1>
          <p style={{
            margin: '4px 0 0',
            fontSize: t.font.sizeXs,
            color: surface.fgSecondary,
          }}>
            Manufacturer truth, systems, certifications, and condition compatibility
          </p>
        </div>
        <ManufacturerModeSwitch mode={mode} onModeChange={handleModeChange} surface={surface} />
      </div>

      {/* Three-column layout */}
      <div style={{
        display: 'flex',
        flex: 1,
        overflow: 'hidden',
      }}>
        {/* Left rail: Manufacturer sidebar */}
        <ManufacturerSidebar
          manufacturers={projection.manufacturers}
          selectedId={selectedManufacturerId}
          onSelect={handleSelectManufacturer}
          surface={surface}
        />

        {/* Center workspace: mode-dependent panels */}
        <div style={{
          flex: 1,
          overflow: 'auto',
          padding: '20px',
          display: 'flex',
          flexDirection: 'column',
          gap: '16px',
        }}>
          {manufacturer && (
            <ManufacturerHeader manufacturer={manufacturer} mode={mode} surface={surface} />
          )}

          {mode === 'work' ? (
            /* WORK MODE: Office surface panels */
            <>
              {manufacturer && (
                <ManufacturerOverviewPanel manufacturer={manufacturer} surface={surface} />
              )}
              <ManufacturerProductsPanel products={products} surface={surface} />
              <ManufacturerSystemsPanel
                systems={systems}
                certifications={projection.certifications}
                selectedSystemId={selectedSystemId}
                onSelectSystem={handleSelectSystem}
                surface={surface}
              />
            </>
          ) : (
            /* SYSTEM MODE: Dark visualization panels */
            <>
              {selectedSystem && (
                <>
                  <SystemInspectorPanel
                    system={selectedSystem}
                    manufacturer={manufacturer!}
                    surface={surface}
                  />
                  <ProductStackPanel products={systemProducts} surface={surface} />
                  <CertificationPanel certifications={systemCertifications} surface={surface} />
                  <ConditionCompatibilityPanel conditions={systemConditions} surface={surface} />
                  <RuleChecklistPanel rules={systemRules} surface={surface} />
                </>
              )}
              {!selectedSystem && manufacturer?.seedStatus === 'scaffold' && (
                <div style={{
                  padding: '32px',
                  textAlign: 'center',
                  color: surface.fgMuted,
                  fontSize: t.font.sizeSm,
                }}>
                  No systems available — manufacturer is scaffold only, not yet seeded in registry
                </div>
              )}
            </>
          )}
        </div>

        {/* Right rail: Governance / Action / Signals */}
        <div style={{
          width: 280,
          minWidth: 280,
          borderLeft: `1px solid ${surface.border}`,
          overflow: 'auto',
          display: 'flex',
          flexDirection: 'column',
          background: mode === 'work' ? surface.bgPanel : surface.bgElevated,
        }}>
          {governance && (
            <GovernanceActionRail
              governance={governance}
              actions={projection.actions}
              mode={mode}
              onModeChange={handleModeChange}
              surface={surface}
            />
          )}
          <ManufacturerSignalsPanel signals={signals} surface={surface} />
        </div>
      </div>
    </div>
  );
}
