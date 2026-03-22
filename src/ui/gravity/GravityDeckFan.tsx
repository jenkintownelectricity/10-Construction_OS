/**
 * Construction OS — Gravity Deck Fan-Out
 *
 * Left contextual deck:
 * - Thin idle strip
 * - Mouse proximity fans cards outward
 * - Vertical scroll through card stack
 * - Click card → new gravity object in workspace
 */

import { useCallback, useEffect, useState } from 'react';
import { tokens } from '../theme/tokens';
import { PROXIMITY } from './ProximityConstants';
import { glassMorphCardStyle } from './GlassMorph';
import { adapters } from '../adapters';
import { eventBus } from '../events/EventBus';
import { activeObjectStore } from '../stores/activeObjectStore';
import type { ActiveObjectIdentity } from '../contracts/events';

interface DeckCard {
  id: string;
  name: string;
  type: string;
  object: ActiveObjectIdentity;
}

interface GravityDeckFanProps {
  expanded: boolean;
  proximity: number;
}

export function GravityDeckFan({ expanded, proximity }: GravityDeckFanProps) {
  const [cards, setCards] = useState<DeckCard[]>([]);

  useEffect(() => {
    adapters.truth.getProjectTree().then((result) => {
      const deck: DeckCard[] = [];
      flattenCards(result.data, deck);
      setCards(deck);
    });
  }, []);

  const handleCardClick = useCallback((card: DeckCard) => {
    activeObjectStore.setActiveObject(card.object, 'work', 'mock');
    eventBus.emit('object.selected', {
      object: card.object,
      source: 'work',
      basis: 'mock',
    });
  }, []);

  const width = expanded
    ? PROXIMITY.fanExpandedWidth
    : PROXIMITY.fanIdleWidth + (proximity * (PROXIMITY.fanExpandedWidth * 0.3));

  const easing = PROXIMITY.easing;

  return (
    <div style={{
      position: 'absolute',
      left: 0,
      top: '50px',
      bottom: '40px',
      width: `${width}px`,
      transition: `width ${PROXIMITY.expandDuration}ms ${easing}`,
      overflow: 'hidden',
      display: 'flex',
      flexDirection: 'column',
      zIndex: 90,
      pointerEvents: expanded ? 'auto' : 'none',
    }}>
      {/* Idle strip indicator */}
      {!expanded && proximity > 0 && (
        <div style={{
          position: 'absolute',
          left: 0,
          top: '30%',
          bottom: '30%',
          width: `${PROXIMITY.fanIdleWidth}px`,
          background: `${tokens.color.accentPrimary}${Math.round(proximity * 40).toString(16).padStart(2, '0')}`,
          borderRadius: '0 3px 3px 0',
          transition: `background ${PROXIMITY.expandDuration}ms ${easing}`,
          pointerEvents: 'none',
        }} />
      )}

      {/* Fan cards — visible when expanded */}
      {expanded && (
        <div style={{
          flex: 1,
          overflow: 'auto',
          padding: `${tokens.space.sm} ${tokens.space.sm}`,
          display: 'flex',
          flexDirection: 'column',
          gap: `${PROXIMITY.fanCardGap}px`,
        }}>
          <div style={{
            fontSize: tokens.font.sizeXs,
            color: tokens.color.fgMuted,
            fontWeight: tokens.font.weightSemibold,
            letterSpacing: '0.05em',
            padding: `${tokens.space.xs} ${tokens.space.sm}`,
            marginBottom: tokens.space.xs,
          }}>
            GRAVITY DECK
          </div>
          {cards.map((card) => (
            <FanCard key={card.id} card={card} onClick={handleCardClick} />
          ))}
        </div>
      )}
    </div>
  );
}

function FanCard({ card, onClick }: { card: DeckCard; onClick: (card: DeckCard) => void }) {
  const typeIcon: Record<string, string> = {
    project: '\u25C6',
    zone: '\u25A0',
    document: '\u25A1',
    assembly: '\u25B2',
    element: '\u25CF',
    specification: '\u25C7',
  };

  return (
    <div
      onClick={() => onClick(card)}
      style={{
        ...glassMorphCardStyle,
        padding: `${tokens.space.sm} ${tokens.space.sm}`,
        borderRadius: tokens.radius.sm,
        cursor: 'pointer',
        minHeight: `${PROXIMITY.fanCardHeight}px`,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        transition: `transform ${PROXIMITY.expandDuration}ms ${PROXIMITY.easing}, background ${PROXIMITY.expandDuration}ms ${PROXIMITY.easing}`,
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.background = 'rgba(59,130,246,0.12)';
        e.currentTarget.style.transform = 'translateX(4px)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.background = glassMorphCardStyle.background as string;
        e.currentTarget.style.transform = 'translateX(0)';
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: tokens.space.sm }}>
        <span style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeXs }}>
          {typeIcon[card.type] ?? '\u25CB'}
        </span>
        <span style={{
          fontSize: tokens.font.sizeXs,
          color: tokens.color.fgPrimary,
          fontWeight: tokens.font.weightMedium,
          overflow: 'hidden',
          textOverflow: 'ellipsis',
          whiteSpace: 'nowrap',
        }}>
          {card.name}
        </span>
      </div>
      <div style={{
        fontSize: tokens.font.sizeXs,
        color: tokens.color.fgMuted,
        fontFamily: tokens.font.familyMono,
        marginTop: '2px',
      }}>
        {card.type}
      </div>
    </div>
  );
}

function flattenCards(node: { id: string; name: string; type: string; children?: readonly any[] }, result: DeckCard[]): void {
  result.push({
    id: node.id,
    name: node.name,
    type: node.type,
    object: {
      id: node.id,
      name: node.name,
      type: node.type as ActiveObjectIdentity['type'],
    },
  });
  if (node.children) {
    for (const child of node.children) {
      flattenCards(child, result);
    }
  }
}
